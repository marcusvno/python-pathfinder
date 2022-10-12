from pathlib import Path
from PIL import Image
import numpy as np


def color_calc(min_ele, max_ele, current_ele):
    percent_ele = (current_ele - min_ele) / (max_ele - min_ele)
    color_code = int(percent_ele * 255)
    return color_code


def check_elevations(current_loc):
    global path_total

    i = int(current_loc[0])
    j = int(current_loc[1])
    elevation = current_loc[2]
    elevation_comparison = []

    if (i < ROWS) and (j < COLS-1):
        OPTION_A = [i-1, j+1, matrix[i-1][j+1]] # noqa
        elevation_comparison.append(np.abs(OPTION_A[2] - elevation))
    if (i < ROWS) and (j < COLS-1):
        OPTION_B = [i, j+1, matrix[i][j+1]] # noqa
        elevation_comparison.append(np.abs(OPTION_B[2] - elevation))
    if (i < ROWS-1) and (j < COLS-1):
        OPTION_C = [i+1, j+1, matrix[i+1][j+1]] # noqa
        elevation_comparison.append(np.abs(OPTION_C[2] - elevation))

    smallest_ele_change = np.amin(elevation_comparison)
    change_index = elevation_comparison.index(smallest_ele_change)

    path_total += smallest_ele_change

    if change_index == 0:
        return OPTION_A
    elif change_index == 1:
        return OPTION_B
    elif change_index == 2:
        return OPTION_C


def map_path(start_loc, flag):
    from PIL import ImageColor

    x = int(start_loc[0])
    y = int(start_loc[1])

    current_loc = [x, y, matrix[x][y]] # noqa

    for i in range(COLS-1):
        if flag:
            map_Copy.putpixel((y, x), (ImageColor.getcolor('goldenrod', 'RGBA'))) # noqa
        else:
            map_Copy.putpixel((y, x), (ImageColor.getcolor('purple', 'RGBA'))) # noqa
        current_loc = check_elevations(current_loc)
        x = int(current_loc[0])
        y = int(current_loc[1])


def create_map(file):
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


def highlight_best_path():
    best_ele = int(np.amin(best_path))
    best_start_pt = (best_path.index(best_ele), 0)
    map_path(best_start_pt, True)

    pass


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

        create_map(file)

        map_unmarked = Image.open(f'MAP - {Path(file).stem}.png')
        map_Copy = map_unmarked.copy()

        print(f'\nPathfinding through {file}...')

        k = 0
        best_path = []
        best_flag = False

        for k in range(ROWS):
            path_total = 0
            location = (k, 0)
            map_path(location, best_flag)
            best_path.append(path_total)

        highlight_best_path()

        print(f'Saving PATH - {Path(file).stem}.png...')
        map_Copy.save(f'PATH - {Path(file).stem}.png')
        print('...Saved!')

    else:
        print(f"{file} does not exist!")
        exit(1)
