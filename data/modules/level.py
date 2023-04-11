import random

import pygame
import pygbase

from data.modules.tile import Tile
from data.modules.utils import generate_2d_list


class Level:
	def __init__(self, size: tuple[int, int], particle_manager: pygbase.ParticleManager):
		self.size = size

		self.tiles: list[list[Tile | None]] = generate_2d_list(self.size[1], self.size[0])
		self.edge_tiles: set[Tile] = set()

		self.gen_tiles(particle_manager)

		self.decay_timer = pygbase.Timer(0.1, False, True)

	def gen_tiles(self, particle_manager: pygbase.ParticleManager):
		for row in range(self.size[1]):
			for col in range(self.size[0]):
				tile = Tile((col, row), particle_manager)

				self.tiles[row][col] = tile

				if row == 0 or row == self.size[1] - 1 or col == 0 or col == self.size[0] - 1:
					self.edge_tiles.add(tile)

	def decay_tile(self):
		if len(self.edge_tiles) > 0:
			tile: Tile = random.choice(list(self.edge_tiles))
			tile_pos = tile.tile_pos

			dirs = [(-1, -1), (1, -1), (-1, 1), (1, 1)]

			if tile.decay():
				self.edge_tiles.remove(tile)
				self.tiles[tile_pos[1]][tile_pos[0]] = None

				for direction in dirs:
					new_pos = tile_pos[0] + direction[0], tile_pos[1] + direction[1]

					if new_pos[0] < 0 or new_pos[0] >= self.size[0] or new_pos[1] < 0 or new_pos[1] >= self.size[1]:
						continue

					new_tile = self.tiles[new_pos[1]][new_pos[0]]
					if new_tile is not None:
						self.edge_tiles.add(new_tile)

	def update(self, delta):
		self.decay_timer.tick(delta)

		if self.decay_timer.done():
			self.decay_tile()

	def draw(self, screen: pygame.Surface, camera: pygbase.Camera):
		for row in self.tiles:
			for tile in row:
				if tile is not None:
					tile.draw(screen, camera)
