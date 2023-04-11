import cProfile

import pygbase

from data.modules.files import sprite_sheet_path
from data.modules.game import Game
from data.modules.tile import Tile
from data.modules.utils import darken_rgb

if __name__ == '__main__':
	pygbase.init((800, 800))

	pygbase.add_sprite_sheet_resource("sprite_sheet", 1, sprite_sheet_path, Tile.TILE_SCALE)

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

	# profiler = cProfile.Profile()
	# profiler.enable()

	app = pygbase.App(Game)
	app.run()

	# profiler.disable()
	# profiler.dump_stats("stats.prof")

	pygbase.quit()
