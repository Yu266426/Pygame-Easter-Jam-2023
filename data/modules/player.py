import pygame
import pygbase

from data.modules.level import Level
from data.modules.shadow import Shadow


class Player:
	def __init__(self, pos, level: Level):
		self.animations = pygbase.AnimationManager([
			("idle", pygbase.Animation("bunny", 0, 2), 4),
			("run", pygbase.Animation("bunny_run", 0, 4), 8)
		], "idle")
		self.flip = False

		self.shadow = Shadow(self.animations.get_current_image().get_image().get_width(), (1, 0.2), 0.1)

		self.angle = 0

		self.pos = pygame.Vector2(pos)

		self.input = pygame.Vector2()

		self.level = level

		self.falling_off = False
		self.fall_direction = None

		self.fall_speed = 10
		self.y_velocity = 0
		self.height = 0

	def fall(self):
		self.falling_off = True
		self.fall_direction = self.input.copy()

	def update(self, delta):
		self.animations.update(delta)

		if not self.falling_off:
			self.input.x = pygbase.InputManager.keys_pressed[pygame.K_d] - pygbase.InputManager.keys_pressed[pygame.K_a]
			self.input.y = pygbase.InputManager.keys_pressed[pygame.K_s] - pygbase.InputManager.keys_pressed[pygame.K_w]

			if self.input.length() != 0:
				self.input.normalize_ip()
				self.animations.switch_state("run")
			else:
				self.animations.switch_state("idle")

			if self.input.x > 0:
				self.flip = False
			elif self.input.x < 0:
				self.flip = True

			self.pos += self.input * 400 * delta
		else:
			self.y_velocity += self.fall_speed * delta
			self.height += self.y_velocity + (self.fall_speed * delta ** 2) / 2

			self.angle += 5

	def draw_shadow(self, screen: pygame.Surface, camera: pygbase.Camera):
		if not self.falling_off:
			self.shadow.draw(screen, camera, self.pos)

	def draw(self, screen: pygame.Surface, camera: pygbase.Camera):
		if not self.falling_off:
			self.animations.draw_at_pos(screen, self.pos, camera, flip=self.flip, draw_pos="midbottom")
		else:
			self.animations.draw_at_pos(screen, (self.pos.x, self.pos.y + self.height), camera, flip=self.flip, angle=self.angle, draw_pos="midbottom")
