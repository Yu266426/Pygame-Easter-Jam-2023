import pygame
import pygbase


class Shadow:
	def __init__(self, size: int, scale: tuple[float, float], darkness: float):
		self.size = size
		self.scale = scale
		self.darkness = darkness * 255

		self.shadow = pygame.Surface((size, size), flags=pygame.SRCALPHA)
		pygame.draw.circle(self.shadow, (self.darkness, self.darkness, self.darkness, 40), (size / 2, size / 2), size / 3)

		self.shadow = pygame.transform.scale_by(self.shadow, scale)

	def draw(self, screen: pygame.Surface, camera: pygbase.Camera, pos: pygame.Vector2):
		screen.blit(self.shadow, camera.world_to_screen((pos.x - self.size / 2, pos.y - self.size * self.scale[1] / 2)))
