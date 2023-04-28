import math

import pygame
import pygbase

from data.modules.shadow import Shadow


class Altar:
	def __init__(self, pos, particle_manager: pygbase.ParticleManager):
		self.animation = pygbase.Animation("altar", 0, 4, True)

		self.pos = pygame.Vector2(pos)

		self.shadow = Shadow(100, (1, 0.4), 0.3)

		particle_manager.add_spawner(pygbase.CircleSpawner(self.pos + (70, -130), 0.05, 5, 30, True, "fire", particle_manager))
		particle_manager.add_spawner(pygbase.CircleSpawner(self.pos + (-70, -130), 0.05, 5, 30, True, "fire", particle_manager))

		self.base_ring = pygame.Surface((400, 400), flags=pygame.SRCALPHA)
		pygame.draw.circle(self.base_ring, (253, 253, 150), (200, 200), 200, width=10)

		self.base_ring = pygame.transform.scale_by(self.base_ring, (1, 0.9))

		self.ring = self.base_ring.copy()

	def update(self, delta):
		self.animation.change_frame(delta * 4)

		self.ring = pygame.transform.scale_by(self.base_ring, 1 + (math.sin((pygame.time.get_ticks() / 1000)) + 1) / 15)

	def draw_shadow(self, screen: pygame.Surface, camera: pygbase.Camera):
		self.shadow.draw(screen, camera, self.pos)

		screen.blit(self.ring, self.ring.get_rect(center=camera.world_to_screen(self.pos + pygame.Vector2(0, -50))))

	def draw(self, screen: pygame.Surface, camera: pygbase.Camera):
		self.animation.draw_at_pos(screen, self.pos, camera, draw_pos="midbottom")
