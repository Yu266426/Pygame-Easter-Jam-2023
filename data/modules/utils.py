def generate_2d_list(n_rows: int, n_cols: int, fill: bool = True) -> list[list]:
	data = []
	for _ in range(n_rows):
		col = []
		if fill:
			for __ in range(n_cols):
				col.append(None)
		data.append(col)
	return data


def darken_rgb(colour: tuple[int, int, int], percent: float) -> tuple[int, int, int]:
	return int(colour[0] * percent), int(colour[1] * percent), int(colour[2] * percent)
