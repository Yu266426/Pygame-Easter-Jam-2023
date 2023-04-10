import pygbase

from data.modules.files import sprite_sheet_path
from data.modules.game import Game
from data.modules.tile import Tile

if __name__ == '__main__':
	pygbase.init((800, 800))

	pygbase.add_sprite_sheet_resource("sprite_sheet", 1, sprite_sheet_path, Tile.TILE_SCALE)

	app = pygbase.App(Game)
	app.run()

	pygbase.quit()
