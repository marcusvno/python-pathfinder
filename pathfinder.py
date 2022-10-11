from pathlib import Path


def create_image(file):
    from PIL import Image
    import numpy as np

    print(f'Converting {file}...')
    matrix = np.loadtxt(file)
    cols = len(matrix)
    rows = len(matrix[0])

    max_elevation = np.amax(matrix)
    min_elevation = np.amin(matrix)

    # print(matrix[0][0])

    im = Image.new('RGBA', (rows, cols))

    for x in range(cols):
        for y in range(rows):
            current_color = color_calc(min_elevation, max_elevation, matrix[x][y])  # noqa
            im.putpixel((y, x), (current_color, current_color, current_color))

    print(f'Saving {Path(file).stem} map.png..')
    im.save(f'{Path(file).stem} map.png')
    print('Saved!')

    """TEST LOOPS
    for x in range(5):
        for y in range(5):
            print(matrix[x][y])
    
    print(f'Highest Elevation: {max_elevation} Lowest: {min_elevation}') # noqa
    """


def color_calc(min_ele, max_ele, current_ele):
    percent_ele = (current_ele - min_ele) / (max_ele - min_ele)
    color_code = int(percent_ele * 255)
    return color_code


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(
        description='Create elevation map from elevation points in a text file.') # noqa
    parser.add_argument('file', help='file to read')
    args = parser.parse_args()

    file = Path(args.file)
    if file.is_file():
        create_image(file)
    else:
        print(f"{file} does not exist!")
        exit(1)
