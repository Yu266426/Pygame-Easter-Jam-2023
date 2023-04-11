import pygame
import pygbase

from data.modules.shadow import Shadow


class Player:
	def __init__(self, pos):
		self.animations = pygbase.AnimationManager([
			("idle", pygbase.Animation("bunny", 0, 2), 4),
			("run", pygbase.Animation("bunny_run", 0, 4), 8)
		], "idle")
		self.flip = False

		self.shadow = Shadow(self.animations.get_current_image().get_image().get_width(), (1, 0.2), 0.1)

		self.pos = pygame.Vector2(pos)

		self.input = pygame.Vector2()

	def update(self, delta):
		self.animations.update(delta)

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

	def draw(self, screen: pygame.Surface, camera: pygbase.Camera):
		self.shadow.draw(screen, camera, self.pos)

		self.animations.draw_at_pos(screen, self.pos, camera, flip=self.flip, draw_pos="midbottom")
