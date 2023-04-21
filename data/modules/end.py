import pygame
import pygbase


class End(pygbase.GameState, name="end"):
	def __init__(self, run_time: float, eggs: int):
		super().__init__()

		self.run_time = run_time

		self.camera = pygbase.Camera()

		self.ui = pygbase.UIScreen()
		self.image_frame = self.ui.add_frame(pygbase.Frame((0, 0), (800, 300)))
		self.image_frame.add_element(pygbase.ImageElement((400, 150), 2, "cracked_egg", alignment="c"))

		self.text_frame = self.ui.add_frame(pygbase.Frame((0, 300), (800, 200)))
		self.text_frame.add_element(pygbase.TextElement(
			(400, 0),
			"Comic Sans MS",
			40,
			(255, 207, 210),
			f"You survived {round(self.run_time)} seconds!",
			True
		))

		self.text_frame.add_element(pygbase.TextElement(
			(400, 40),
			"Comic Sans MS",
			40,
			(255, 207, 210),
			f"{eggs} eggs collected",
			True
		), add_on_to_previous=(False, True))

		self.button_frame = self.ui.add_frame(pygbase.Frame((0, 500), (800, 300)))
		from data.modules.game import Game
		self.button_frame.add_element(pygbase.Button(
			(400, 0),
			2,
			"button",
			self.set_next_state,
			(Game(),),
			text="Restart",
			text_colour=(255, 255, 252),
			font="Comic Sans MS",
			alignment="c"
		))

		self.particles = pygbase.ParticleManager()
		self.rect_spawner = self.particles.add_spawner(
			pygbase.RectSpawner(
				(0, 0),
				0.05,
				100,
				(800, 800),
				True,
				"everything",
				self.particles
			)
		)

	def update(self, delta: float):
		self.ui.update(delta)
		self.particles.update(delta)

		if pygbase.InputManager.keys_down[pygame.K_ESCAPE]:
			pygbase.EventManager.post_event(pygame.QUIT)

	def draw(self, screen: pygame.Surface):
		screen.fill((255, 255, 252))

		self.ui.draw(screen)
		self.particles.draw(screen, self.camera)
