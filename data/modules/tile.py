import pygame
import pygbase


class Tile:
	TILE_SCALE = 6
	FRONT_SIZE = 6 * TILE_SCALE
	SIZE = 16 * TILE_SCALE

	def __init__(self, tile_pos: tuple[int, int]):
		pygbase.Common.set_value("tile_size", Tile.SIZE)
		pygbase.Common.set_value("tile_front_size", Tile.FRONT_SIZE)

		self.tile_pos = tile_pos
		self.pos = self.tile_pos[0] * Tile.SIZE, self.tile_pos[1] * Tile.SIZE

		self.state = 0

		self.sprite_sheet: pygbase.SpriteSheet = pygbase.ResourceManager.get_resource(1, "tiles")

		self.front_rect = pygame.Rect(
			self.pos[0],
			self.pos[1] + Tile.SIZE,
			Tile.SIZE,
			Tile.FRONT_SIZE
		)

		self.top_rect = pygame.Rect(
			self.pos, (Tile.SIZE, Tile.SIZE)
		)

	def decay(self) -> bool:
		self.state += 1

		return self.state >= 3

	def draw(self, screen: pygame.Surface, camera: pygbase.Camera):
		self.sprite_sheet.get_image(self.state).draw(screen, camera.world_to_screen(self.pos))
