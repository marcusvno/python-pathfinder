from pathlib import Path
from PIL import Image
import numpy as np


def color_calc(min_ele, max_ele, current_ele):
    percent_ele = (current_ele - min_ele) / (max_ele - min_ele)
    color_code = int(percent_ele * 255)
    return color_code


def track_best_path():
    pass


def check_elevations(current_loc):
    i = int(current_loc[0])
    j = int(current_loc[1])
    elevation = current_loc[2]
    elevation_comparison = []

    if (i < 600) and (j < 599):
        OPTION_A = [i-1, j+1, matrix[i-1][j+1]] # noqa
        elevation_comparison.append(np.abs(OPTION_A[2] - elevation))
    if (i < 600) and (j < 599):
        OPTION_B = [i, j+1, matrix[i][j+1]] # noqa
        elevation_comparison.append(np.abs(OPTION_B[2] - elevation))
    if (i < 599) and (j < 599):
        OPTION_C = [i+1, j+1, matrix[i+1][j+1]] # noqa
        elevation_comparison.append(np.abs(OPTION_C[2] - elevation))

    small_ele_change = np.amin(elevation_comparison)
    change_index = elevation_comparison.index(small_ele_change)
    if change_index == 0:
        return OPTION_A
    elif change_index == 1:
        return OPTION_B
    elif change_index == 2:
        return OPTION_C


def map_path(start_loc):
    from PIL import ImageColor

    x = int(start_loc[0])
    y = int(start_loc[1])

    current_loc = [x, y, matrix[x][y]] # noqa

    for i in range(COLS-1):
        map_Copy.putpixel((y, x), (ImageColor.getcolor('purple', 'RGBA')))
        current_loc = check_elevations(current_loc)
        x = int(current_loc[0])
        y = int(current_loc[1])


def create_image(file):
    max_elevation = np.amax(matrix)
    min_elevation = np.amin(matrix)

    im = Image.new('RGBA', (ROWS, COLS))

    for x in range(ROWS):
        for y in range(COLS):
            current_color = color_calc(min_elevation, max_elevation, matrix[x][y])  # noqa
            im.putpixel((y, x), (current_color, current_color, current_color))

    print(f'\nConverting {file}...')
    print(f'Saving MAP - {Path(file).stem}.png...')
    im.save(f'MAP - {Path(file).stem}.png')
    print('...Saved!')


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(
        description='Create elevation map from elevation points in a text file.') # noqa
    parser.add_argument('file', help='file to read')
    args = parser.parse_args()

    file = Path(args.file)
    if file.is_file():
        matrix = np.loadtxt(file)
        ROWS, COLS = matrix.shape

        create_image(file)

        map_unmarked = Image.open(f'MAP - {Path(file).stem}.png')
        map_Copy = map_unmarked.copy()

        print(f'\nPathfinding through {file}...')

        x = 0
        for x in range(ROWS):
            location = (x, 0)
            map_path(location)

        map_Copy.save(f'PATH - {Path(file).stem}.png')
        print(f'Saving PATH - {Path(file).stem}.png...')
        print('...Saved!')

    else:
        print(f"{file} does not exist!")
        exit(1)
