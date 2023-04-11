import pygame
import pygbase

from data.modules.level import Level
from data.modules.player import Player
from data.modules.tile import Tile


class Game(pygbase.GameState):
	level_size = (14, 14)

	def __init__(self):
		super().__init__(1)

		self.quit_timer = pygbase.Timer(10, False, False)

		self.camera = pygbase.Camera()

		self.tile_particles = pygbase.ParticleManager()

		self.level = Level(Game.level_size, self.tile_particles)

		self.player = Player((60, 60))

		self.void_particles = pygbase.ParticleManager()
		self.void_particles.add_spawner(pygbase.CircleSpawner(
			(Game.level_size[0] * Tile.SIZE / 2, Game.level_size[1] * Tile.SIZE / 2),
			0.1,
			10,
			(Game.level_size[0] * Tile.SIZE),
			True,
			"void",
			self.void_particles
		))

	def update(self, delta: float):
		self.quit_timer.tick(delta)

		self.void_particles.update(delta)
		self.tile_particles.update(delta)

		self.level.update(delta)
		self.player.update(delta)

		self.camera.lerp_to_target(self.player.pos - pygame.Vector2(400, 400), 2 * delta)

		if pygbase.InputManager.keys_down[pygame.K_ESCAPE]:
			pygbase.EventManager.post_event(pygame.QUIT)

	# if self.quit_timer.done():
	# 	pygbase.EventManager.post_event(pygame.QUIT)

	def draw(self, screen: pygame.Surface):
		screen.fill("black")
		self.void_particles.draw(screen, self.camera)
		self.level.draw(screen, self.camera)
		self.player.draw(screen, self.camera)
		self.tile_particles.draw(screen, self.camera)
