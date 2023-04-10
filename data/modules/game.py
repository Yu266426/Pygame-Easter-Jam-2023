import pygame
import pygbase

from data.modules.level import Level
from data.modules.player import Player


class Game(pygbase.GameState):
	def __init__(self):
		super().__init__(1)

		self.camera = pygbase.Camera()
		self.level = Level((20, 20))

		self.player = Player((60, 60))

	def update(self, delta: float):
		self.player.update(delta)

		self.camera.lerp_to_target(self.player.pos - pygame.Vector2(400, 400), 2 * delta)

		if pygbase.InputManager.keys_pressed[pygame.K_SPACE]:
			self.level.decay_tile()

		if pygbase.InputManager.keys_down[pygame.K_ESCAPE]:
			pygbase.EventManager.post_event(pygame.QUIT)

	def draw(self, screen: pygame.Surface):
		screen.fill("black")
		self.level.draw(screen, self.camera)
		self.player.draw(screen, self.camera)
