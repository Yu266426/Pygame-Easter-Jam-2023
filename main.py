import cProfile
import logging

import pygbase

from data.modules.files import sprite_sheet_path, image_path, sound_path
from data.modules.game import Game
from data.modules.tile import Tile
from data.modules.utils import darken_rgb

if __name__ == '__main__':
	pygbase.init((800, 800), logging_level=logging.ERROR)

	pygbase.add_sprite_sheet_resource("sprite_sheet", 1, sprite_sheet_path, Tile.TILE_SCALE)
	pygbase.add_image_resource("image", 2, image_path)
	pygbase.add_sound_resource("sound", 3, sound_path, ".wav")

	pygbase.add_particle_setting(
		"void",
		["white"],
		(14.0, 26.0),
		(5.0, 10.0),
		(2.0, 2.0),
		(0, -2),
		False
	)
	pygbase.add_particle_setting(
		"decay1",
		[darken_rgb((185, 251, 192), 0.9), (152, 245, 225)],
		(8.0, 12.0),
		(3.0, 6.0),
		(2.0, 2.0),
		(0, -3),
		False
	)
	pygbase.add_particle_setting(
		"decay2",
		[darken_rgb((251, 248, 204), 0.95), (253, 228, 207)],
		(8.0, 12.0),
		(6.0, 9.0),
		(2.0, 2.0),
		(0, -3),
		False
	)

	pygbase.add_particle_setting(
		"fire",
		[(255, 185, 185), (255, 203, 185), (255, 224, 186), (255, 238, 185), (255, 249, 185)],
		(8.0, 12.0),
		(6.0, 9.0),
		(2.0, 2.0),
		(0, -3),
		False
	)

	pygbase.add_particle_setting(
		"everything",
		[
			(255, 185, 185), (255, 203, 185), (255, 224, 186), (255, 238, 185), (255, 249, 185),
			darken_rgb((251, 248, 204), 0.95), (253, 228, 207),
			darken_rgb((185, 251, 192), 0.9), (152, 245, 225),
			"white"
		],
		(8.0, 12.0),
		(6.0, 9.0),
		(2.0, 2.0),
		(0, -3),
		False
	)

	# profiler = cProfile.Profile()
	# profiler.enable()

	app = pygbase.App(Game, title="Egg Hunt!")
	app.run()

	# profiler.disable()
	# profiler.dump_stats("stats.prof")

	pygbase.quit()
