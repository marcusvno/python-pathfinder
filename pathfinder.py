from pathlib import Path


def color_calc(min_ele, max_ele, current_ele):
    percent_ele = (current_ele - min_ele) / (max_ele - min_ele)
    color_code = int(percent_ele * 255)
    return color_code

def create_image(file):
    from PIL import Image
    import numpy as np

    print(f'Converting {file}...')
    matrix = np.loadtxt(file)
    rows, cols = matrix.shape

    max_elevation = np.amax(matrix)
    min_elevation = np.amin(matrix)

    im = Image.new('RGBA', (rows, cols))

    for x in range(rows):
        for y in range(cols):
            current_color = color_calc(min_elevation, max_elevation, matrix[x][y])  # noqa
            im.putpixel((y, x), (current_color, current_color, current_color))

    print(f'Saving {Path(file).stem} map.png..')
    im.save(f'{Path(file).stem} map.png')
    print('...Saved!')


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
