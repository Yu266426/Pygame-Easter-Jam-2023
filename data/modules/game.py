import random
from typing import Optional

import pygame
import pygbase

from data.modules.altar import Altar
from data.modules.egg import Egg
from data.modules.end import End
from data.modules.files import music_path
from data.modules.level import Level
from data.modules.player import Player
from data.modules.tile import Tile


class Game(pygbase.GameState, name="game"):
	level_size = (16, 16)

	def __init__(self):
		super().__init__()

		self.camera = pygbase.Camera((Game.level_size[0] * Tile.SIZE / 2 - 400, Game.level_size[1] * Tile.SIZE / 2 - 400 + 60))

		self.void_particles = pygbase.ParticleManager()
		self.void_particles.add_spawner(pygbase.CircleSpawner(
			(Game.level_size[0] * Tile.SIZE / 2, Game.level_size[1] * Tile.SIZE / 2),
			0.1,
			20,
			(Game.level_size[0] * Tile.SIZE),
			True,
			"void",
			self.void_particles
		))

		self.particles = pygbase.ParticleManager()
		self.egg_particle_settings = pygbase.Common.get_particle_setting("everything")

		self.rendered_entities: list = []

		self.level = Level(Game.level_size, self.particles)
		# self.altar = Altar((Game.level_size[0] / 2 * Tile.SIZE, Game.level_size[1] / 2 * Tile.SIZE), self.particles)
		# self.rendered_entities.append(self.altar)

		self.egg: Optional[Egg] = None

		self.player = Player((Game.level_size[0] * Tile.SIZE / 2, Game.level_size[1] * Tile.SIZE / 2 + 60), self.level)
		self.rendered_entities.append(self.player)

		self.death_timer = pygbase.Timer(2, True, False)
		self.dead = False

		self.run_time = 0
		self.collected_eggs = 0

		# pygame.mixer.music.load(music_path / "music.wav")
		# pygame.mixer.music.set_volume(0.1)
		# pygame.mixer.music.play(-1)

		self.egg_pickup_sound: pygame.mixer.Sound = pygbase.ResourceManager.get_resource(3, "pickup")

	def spawn_egg(self, attempts=10):
		for _ in range(attempts):
			spawn_pos = random.randrange(0, Game.level_size[0] * Tile.SIZE), random.randrange(0, Game.level_size[1] * Tile.SIZE)
			if self.level.get_tile(spawn_pos) is not None:
				self.egg = Egg(spawn_pos, self.particles)
				self.rendered_entities.append(self.egg)
				break

	def egg_update(self, delta):
		self.egg.update(delta)

		if not self.egg.falling_off and self.level.get_tile(self.egg.pos) is None:
			self.egg.fall()
			self.level.inject_falling_entity(self.egg, int(self.egg.pos.y // Tile.SIZE))
			self.rendered_entities.remove(self.egg)

		if not self.egg.alive:
			if not self.egg.falling_off:
				self.rendered_entities.remove(self.egg)
			else:
				self.level.remove_falling_entity(self.egg)

			self.egg = None
		elif self.egg.on_ground and not self.player.is_jumping and self.egg.pos.distance_to(self.player.pos) < 35:
			for _ in range(random.randint(50, 100)):
				spawn_offset = pygame.Vector2(random.uniform(-30, 30), random.uniform(-30, 30))
				self.particles.add_particle(
					self.egg.pos + spawn_offset,
					self.egg_particle_settings,
					spawn_offset * 20
				)

			self.level.start_regen()

			if self.egg in self.rendered_entities:
				self.rendered_entities.remove(self.egg)
			self.egg = None

			self.collected_eggs += 1
			self.egg_pickup_sound.play()

	def player_update(self, delta):
		self.player.update(delta)
		if not self.player.falling_off and not self.player.is_jumping:
			on_tile = False
			buffer = 30

			if self.level.get_tile(self.player.pos + (buffer, buffer)) is not None:
				on_tile = True
			if self.level.get_tile(self.player.pos + (-buffer, buffer)) is not None:
				on_tile = True
			if self.level.get_tile(self.player.pos + (buffer, -buffer)) is not None:
				on_tile = True
			if self.level.get_tile(self.player.pos + (-buffer, -buffer)) is not None:
				on_tile = True

			if not on_tile:
				self.player.fall()
				self.level.inject_falling_entity(self.player, int(self.player.pos.y // Tile.SIZE))
				self.rendered_entities.remove(self.player)
				self.death_timer.start()

		if not self.dead and self.player.falling_off and self.death_timer.done():
			self.set_next_state(pygbase.FadeTransition(self, End(self.run_time, self.collected_eggs), 3, (0, 0, 0)))
			self.dead = True

	def update(self, delta: float):
		if not self.dead:
			self.run_time += delta

		self.death_timer.tick(delta)

		if self.egg is None:
			self.spawn_egg()

		self.void_particles.update(delta)
		self.particles.update(delta)

		self.level.update(delta)

		# self.altar.update(delta)

		if self.egg is not None:
			self.egg_update(delta)

		self.player_update(delta)

		self.camera.lerp_to_target(self.player.pos - pygame.Vector2(400, 400), 2 * delta)

		if pygbase.InputManager.keys_down[pygame.K_ESCAPE]:
			pygbase.EventManager.post_event(pygame.QUIT)

		if pygbase.InputManager.keys_pressed[pygame.K_r]:
			self.level.decay_tile()

	def draw(self, screen: pygame.Surface):
		screen.fill("black")
		self.void_particles.draw(screen, self.camera)

		self.level.draw(screen, self.camera)

		for entity in self.rendered_entities:
			entity.draw_shadow(screen, self.camera)

		for entity in sorted(self.rendered_entities, key=lambda e: e.pos.y):
			entity.draw(screen, self.camera)

		self.particles.draw(screen, self.camera)
