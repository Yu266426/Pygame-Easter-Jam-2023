import pygame
import pygbase


class Player:
	def __init__(self, pos):
		self.animations = pygbase.AnimationManager([
			("idle", pygbase.Animation("bunny", 0, 1), 8),
			("run", pygbase.Animation("bunny_run", 0, 4), 8)
		], "idle")
		self.flip = False

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
		self.animations.draw_at_pos(screen, self.pos, camera, flip=self.flip, draw_pos="midbottom")
