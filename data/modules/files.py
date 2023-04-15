import os
import pathlib
import sys

current_path = pathlib.Path(os.path.dirname(os.path.realpath(sys.argv[0])))
data_path = current_path / "data"
asset_path = data_path / "assets"

sprite_sheet_path = asset_path / "sprite_sheets"
image_path = asset_path / "images"
sound_path = asset_path / "sounds"
music_path = asset_path / "music"
