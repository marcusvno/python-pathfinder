from pathlib import Path


def create_image(file):
    from PIL import Image
    import numpy

    print(file)
    matrix = numpy.loadtxt(file)
    rows = len(matrix)
    cols = len(matrix[0])

    max_elevation = int(numpy.amax(matrix))
    min_elevation = int(numpy.amin(matrix))

    im = Image.new('RGBA', (rows, cols))

    for x in range(rows):
        for y in range(cols):
            current_color = color_calc(min_elevation, max_elevation, matrix[x][y])  # noqa
            im.putpixel((x, y), (current_color, current_color, current_color))


    print(f'{Path(file).stem} has {rows} Rows and {cols}')
    print(f'Largest number: {max_elevation} Lowest: {min_elevation}') # noqa

    # im.save(f'{Path(file).stem}.png')


def color_calc(min_ele, max_ele, current_ele):
    pass

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
