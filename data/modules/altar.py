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

	def update(self, delta):
		self.animation.change_frame(delta * 4)

	def draw_shadow(self, screen: pygame.Surface, camera: pygbase.Camera):
		self.shadow.draw(screen, camera, self.pos)

	def draw(self, screen: pygame.Surface, camera: pygbase.Camera):
		self.animation.draw_at_pos(screen, self.pos, camera, draw_pos="midbottom")
