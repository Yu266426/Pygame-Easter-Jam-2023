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

		self.fall_speed = 20
		self.y_velocity = 0
		self.height = 2000

		self.on_ground = False

		self.falling_off = False
		self.alive = True

	def fall(self):
		self.falling_off = True

	def update(self, delta: float):
		self.animations.update(delta)

		if not self.falling_off:
			if self.height > 0:
				self.y_velocity += self.fall_speed * delta
				self.height -= self.y_velocity + (self.fall_speed * delta ** 2) / 2
			else:
				self.height = 0
				self.y_velocity = 0
				self.on_ground = True
		else:
			self.y_velocity += self.fall_speed * delta
			self.height -= self.y_velocity + (self.fall_speed * delta ** 2) / 2

	def draw_shadow(self, screen: pygame.Surface, camera: pygbase.Camera):
		self.shadow.draw(screen, camera, self.pos)

	def draw(self, screen: pygame.Surface, camera: pygbase.Camera):
		self.animations.draw_at_pos(screen, (self.pos.x, self.pos.y - self.height), camera, draw_pos="midbottom")

		if self.falling_off and not screen.get_rect().collidepoint(camera.world_to_screen((self.pos.x, self.pos.y - self.height))):
			self.alive = False
