import pygame
import pygbase

from data.modules.shadow import Shadow


class Egg:
	def __init__(self, pos):
		self.animations = pygbase.AnimationManager([
			("idle", pygbase.Animation("egg", 0, 2), 2),
		], "idle")
		self.shadow = Shadow(self.animations.get_current_image().get_image().get_width(), (1.4, 0.5), 0.1)

		self.pos = pygame.Vector2(pos)

	def update(self, delta: float):
		self.animations.update(delta)

	def draw_shadow(self, screen: pygame.Surface, camera: pygbase.Camera):
		self.shadow.draw(screen, camera, self.pos)

	def draw(self, screen: pygame.Surface, camera: pygbase.Camera):
		self.animations.draw_at_pos(screen, self.pos, camera, draw_pos="midbottom")
