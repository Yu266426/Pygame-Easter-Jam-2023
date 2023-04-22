import pygame
import pygbase


class Tile:
	TILE_SCALE = 6
	FRONT_SIZE = 6 * TILE_SCALE
	SIZE = 16 * TILE_SCALE

	def __init__(self, tile_pos: tuple[int, int], particle_manager: pygbase.ParticleManager):
		pygbase.Common.set_value("tile_size", Tile.SIZE)
		pygbase.Common.set_value("tile_front_size", Tile.FRONT_SIZE)

		self.tile_pos = tile_pos
		self.pos = self.tile_pos[0] * Tile.SIZE, self.tile_pos[1] * Tile.SIZE

		self.state = 0

		self.sprite_sheet: pygbase.SpriteSheet = pygbase.ResourceManager.get_resource(pygbase.Common.get_resource_type("sprite_sheet"), "tiles")

		self.front_rect = pygame.Rect(
			self.pos[0],
			self.pos[1] + Tile.SIZE,
			Tile.SIZE,
			Tile.FRONT_SIZE
		)

		self.top_rect = pygame.Rect(
			self.pos, (Tile.SIZE, Tile.SIZE)
		)

		self.particle_spawner_1: pygbase.RectSpawner = particle_manager.add_spawner(pygbase.RectSpawner(self.pos, 0.5, 5, self.top_rect.size, False, "decay1", particle_manager))
		self.particle_spawner_2: pygbase.RectSpawner = particle_manager.add_spawner(pygbase.RectSpawner(self.pos, 0.2, 10, self.top_rect.size, False, "decay2", particle_manager))

	def decay(self) -> bool:
		self.state += 1

		self.particle_spawner_1.active = False
		self.particle_spawner_2.active = False

		if self.state == 1:
			self.particle_spawner_1.active = True
		elif self.state == 2:
			self.particle_spawner_2.active = True

		return self.state >= 3

	def reset(self):
		self.state = 0
		self.particle_spawner_1.active = False
		self.particle_spawner_2.active = False

	def draw(self, screen: pygame.Surface, camera: pygbase.Camera):
		self.sprite_sheet.get_image(self.state).draw(screen, camera.world_to_screen(self.pos))
