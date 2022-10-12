from pathlib import Path
from PIL import Image
import numpy as np


def color_calc(min_ele, max_ele, current_ele):
    percent_ele = (current_ele - min_ele) / (max_ele - min_ele)
    color_code = int(percent_ele * 255)
    return color_code


def check_elevations(current_loc):
    OPTION_A = [current_loc[0]-1, current_loc[1]+1, matrix[int(current_loc[0])-1][int(current_loc[1]+1)]] # noqa
    OPTION_B = [current_loc[0], current_loc[1]+1, matrix[int(current_loc[0])][int(current_loc[1])+1]] # noqa
    OPTION_C = [current_loc[0]+1, current_loc[1]+1, matrix[int(current_loc[0])+1][int(current_loc[1]+1)]] # noqa

    elevation_comparison = []
    elevation_comparison.append(np.abs(OPTION_A[2] - current_loc[2]))
    elevation_comparison.append(np.abs(OPTION_B[2] - current_loc[2]))
    elevation_comparison.append(np.abs(OPTION_C[2] - current_loc[2]))

    small_ele_change = np.amin(elevation_comparison)
    change_index = elevation_comparison.index(small_ele_change)
    if change_index == 0:
        return OPTION_A
    elif change_index == 1:
        return OPTION_B
    elif change_index == 2:
        return OPTION_C


def map_path(file, start_loc):
    from PIL import ImageColor

    # map_unmarked = Image.open(f'MAP - {Path(file).stem}.png')
    # map_Copy = map_unmarked.copy()

    # STARTING_LOC = (np.floor(rows/2), 0)
    # x = int(STARTING_LOC[0])
    # y = int(STARTING_LOC[1])

    x = int(start_loc[0])
    y = int(start_loc[1])

    current_loc = [x, y, matrix[x][y]] # noqa

    for i in range(COLS-1):
        map_Copy.putpixel((y, x), (ImageColor.getcolor('purple', 'RGBA')))
        current_loc = check_elevations(current_loc)
        x = int(current_loc[0])
        y = int(current_loc[1])

    # map_Copy.save(f'PATH - {Path(file).stem}.png')

    """ print()
    print('Calculating path...')
    print(f'Saving path for {file}...')
    print('...Saved!') """


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

        x = 0
        for x in range(ROWS-2):
            location = (x, 0)
            map_path(file, location)

        map_Copy.save(f'PATH - {Path(file).stem}.png')
    else:
        print(f"{file} does not exist!")
        exit(1)
