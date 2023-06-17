import pygame
import pygbase

from data.modules.level import Level
from data.modules.shadow import Shadow


class Player:
	def __init__(self, pos, level: Level):
		self.animations = pygbase.AnimationManager([
			("idle", pygbase.Animation("bunny", 0, 2), 4),
			("run", pygbase.Animation("bunny_run", 0, 4), 8),
			("jump", pygbase.Animation("bunny_run", 0, 4), 2)
		], "idle")
		self.flip = False

		self.shadow = Shadow(self.animations.get_current_image().get_image().get_width(), (1, 0.2), 0.1)

		self.angle = 0

		self.pos = pygame.Vector2(pos)

		self.input = pygame.Vector2()

		self.level = level

		self.falling_off = False
		self.fall_direction = None

		self.height = 0

		self.fall_speed = 10
		self.y_velocity = 0
		self.fall_sound: pygame.mixer.Sound = pygbase.ResourceManager.get_resource(3, "fall")

		self.jump_charge = 0
		self.is_jumping = False

	def fall(self):
		self.falling_off = True
		self.fall_direction = self.input.copy()

		self.fall_sound.play()

	def update(self, delta):
		# print(self.is_jumping, self.jump_charge)
		self.animations.update(delta)

		if not self.falling_off:
			if not self.is_jumping:
				if pygbase.InputManager.get_key_pressed(pygame.K_SPACE):
					if self.jump_charge == 0:
						self.jump_charge = 6

					self.jump_charge += 20 * delta
					if self.jump_charge > 12:
						self.jump_charge = 10
				elif self.jump_charge > 0:
					self.is_jumping = True

				self.input.x = pygbase.InputManager.get_key_pressed(pygame.K_d) - pygbase.InputManager.get_key_pressed(pygame.K_a)
				self.input.y = pygbase.InputManager.get_key_pressed(pygame.K_s) - pygbase.InputManager.get_key_pressed(pygame.K_w)

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
				self.height += self.jump_charge * 100 * delta
				self.height -= 500 * delta

				self.jump_charge -= 13 * delta
				if self.jump_charge < 0:
					self.jump_charge = 0

				if self.height <= 1:
					self.height = 0
					self.jump_charge = 0
					self.is_jumping = False

				self.pos += self.input * 500 * delta
		else:
			self.y_velocity += self.fall_speed * delta
			self.height -= self.y_velocity + (self.fall_speed * delta ** 2) / 2

			self.angle += 5

	def draw_shadow(self, screen: pygame.Surface, camera: pygbase.Camera):
		if not self.falling_off:
			self.shadow.draw(screen, camera, self.pos)

	def draw(self, screen: pygame.Surface, camera: pygbase.Camera):
		self.animations.draw_at_pos(screen, (self.pos.x, self.pos.y - self.height), camera, flip=(self.flip, False), angle=self.angle, draw_pos="midbottom")
