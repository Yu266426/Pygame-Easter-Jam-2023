import random
from collections import deque

import pygame
import pygbase

from data.modules.tile import Tile
from data.modules.utils import generate_2d_list


class Level:
	def __init__(self, size: tuple[int, int], particle_manager: pygbase.ParticleManager):
		self.size = size

		self.tiles: list[list[Tile | None]] = generate_2d_list(self.size[1], self.size[0])
		self.edge_pos: set[tuple] = set()

		self.particle_manager = particle_manager
		self.gen_tiles()

		self.decay_timer = pygbase.Timer(0.1, False, True)

		self.falling_entities: dict[int, list] = {}

		self.regen = 0
		self.regen_cooldown = pygbase.Timer(0.04, True, False)
		self.regen_particle_settings = pygbase.Common.get_particle_setting("everything")
		self.pos_queue = deque()
		self.visited_pos = set()

	def gen_tiles(self):
		for row in range(self.size[1]):
			for col in range(self.size[0]):
				tile = Tile((col, row), self.particle_manager)

				self.tiles[row][col] = tile

				if row == 0 or row == self.size[1] - 1 or col == 0 or col == self.size[0] - 1:
					self.edge_pos.add((col, row))

	def decay_tile(self):
		if len(self.edge_pos) > 0:
			directions = (
				(1, 0),
				(-1, 0),
				(0, 1),
				(0, -1)
			)

			tile_pos = random.choice(list(self.edge_pos))
			tile = self.tiles[tile_pos[1]][tile_pos[0]]

			if tile is not None:
				if tile.decay():
					self.edge_pos.remove(tile_pos)
					self.tiles[tile_pos[1]][tile_pos[0]] = None

					for direction in directions:
						new_pos = tile_pos[0] + direction[0], tile_pos[1] + direction[1]

						if new_pos[0] < 0 or new_pos[0] >= self.size[0] or new_pos[1] < 0 or new_pos[1] >= self.size[1]:
							continue

						new_tile = self.tiles[new_pos[1]][new_pos[0]]
						if new_tile is not None:
							self.edge_pos.add(new_pos)
			else:
				self.edge_pos.remove(tile_pos)

	def start_regen(self, amount=24):
		if len(self.edge_pos) > 0:
			tile_pos = random.choice(list(self.edge_pos))
		else:
			tile_pos = random.randrange(0, self.size[0]), random.randrange(0, self.size[1])

		self.pos_queue.append(tile_pos)
		self.visited_pos.add(tile_pos)
		self.regen = amount

		self.regen_cooldown.start()

	def regen_tile(self):
		if self.regen > 0:
			directions = (
				(1, 0),
				(-1, 0),
				(0, 1),
				(0, -1)
			)

			pos = self.pos_queue.popleft()
			self.visited_pos.add(pos)

			# if self.get_tile(pos, tile_pos=True) is not None:
			# 	return

			if self.tiles[pos[1]][pos[0]] is None:
				self.tiles[pos[1]][pos[0]] = Tile(pos, self.particle_manager)
			else:
				self.tiles[pos[1]][pos[0]].reset()

			for _ in range(random.randint(50, 100)):
				self.particle_manager.add_particle(
					((pos[0] + 0.5) * Tile.SIZE + random.uniform(-40, 40), (pos[1] + 0.5) * Tile.SIZE + random.uniform(-40, 40)),
					self.regen_particle_settings
				)

			for direction in directions:
				new_pos = pos[0] + direction[0], pos[1] + direction[1]

				if new_pos[0] < 0 or new_pos[0] >= self.size[0] or new_pos[1] < 0 or new_pos[1] >= self.size[1]:
					continue

				if new_pos in self.visited_pos:
					continue

				self.pos_queue.append(new_pos)

			self.regen -= 1
			self.regen_cooldown.start()

			if self.regen <= 0:
				self.pos_queue.clear()

				for pos in self.visited_pos:
					if self.is_edge(pos):
						self.edge_pos.add(pos)
					else:
						if pos in self.edge_pos:
							self.edge_pos.remove(pos)
				self.visited_pos.clear()

	def get_tile(self, pos: pygame.Vector2 | tuple, tile_pos: bool = False):
		if tile_pos:
			tile_pos = pos
		else:
			tile_pos = int(pos[0] // Tile.SIZE), int(pos[1] // Tile.SIZE)

		if tile_pos[0] < 0 or tile_pos[0] >= self.size[0] or tile_pos[1] < 0 or tile_pos[1] >= self.size[1]:
			return None

		return self.tiles[tile_pos[1]][tile_pos[0]]

	def is_edge(self, pos: tuple):
		directions = (
			(1, 0),
			(-1, 0),
			(0, 1),
			(0, -1)
		)

		for direction in directions:
			new_pos = pos[0] + direction[0], pos[1] + direction[1]

			if self.get_tile(new_pos, tile_pos=True) is None:
				return True
		return False

	def inject_falling_entity(self, entity, y_level):
		if y_level not in self.falling_entities:
			self.falling_entities[y_level] = []

		self.falling_entities[y_level].append(entity)

	def remove_falling_entity(self, entity):
		for y_level, falling_row in self.falling_entities.items():
			for falling_entity in falling_row:
				if falling_entity is entity:
					self.falling_entities[y_level].remove(entity)

	def update(self, delta):
		self.decay_timer.tick(delta)

		if self.decay_timer.done():
			self.decay_tile()

		self.regen_cooldown.tick(delta)
		if self.regen_cooldown.done():
			self.regen_tile()

	def draw(self, screen: pygame.Surface, camera: pygbase.Camera):
		if -1 in self.falling_entities:
			for entity in self.falling_entities[-1]:
				entity.draw(screen, camera)

		for row_index, row in enumerate(self.tiles):
			for tile in row:
				if tile is not None:
					tile.draw(screen, camera)

			if row_index in self.falling_entities:
				for entity in self.falling_entities[row_index]:
					entity.draw(screen, camera)

		if self.size[1] in self.falling_entities:
			for entity in self.falling_entities[self.size[1]]:
				entity.draw(screen, camera)

# for pos in self.edge_pos:
# 	pygame.draw.rect(screen, "blue", pygame.Rect(camera.world_to_screen((pos[0] * Tile.SIZE, pos[1] * Tile.SIZE)), (Tile.SIZE, Tile.SIZE)))
