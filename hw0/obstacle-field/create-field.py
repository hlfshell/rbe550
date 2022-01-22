import sys
from getopt import getopt

from field import Field

try:
    opts, args = getopt(sys.argv[1:], "g:w::h::o::p:")
except Exception as e:
    print("python create-field.py -w 128 -h 128 -o out.jpg -p 30")
    sys.exit(2)

width = 0
height = 0
output = ""
percentage = 0
gif = ""

for opt, arg in opts:
    if opt == "-w":
        width = int(arg)
    elif opt == "-h":
        height = int(arg)
    elif opt == "-o":
        output = arg
    elif opt == "-p":
        percentage = int(arg)/100
    elif opt == "-g":
        gif = arg

field = Field(width, height)

if gif == "":
    field.fill_field_to_percent(percentage)
    print(f"Field created and filled to {field.coverage_percentage()*100}%")
else:
    im_gif = field.draw()
    frames = []
    try:
        while field.coverage_percentage() < percentage:
            field.place_random_tetrominoe()
            frames.append(field.draw())
    except:
        # Ignore exception for now, as we expect it might happen when
        # placing obstacles and our field is overflooded
        pass

    # The last frame we pause on for five frames
    for i in range(1, 10):
        frames.append(frames[-1])
    im_gif.save("out.gif", save_all=True, append_images=frames, duration=10, loop=0)
    print(f"Field created and filled to {field.coverage_percentage()*100}%")
    print(f"Gif saved to {gif}")

im = field.draw()
im.save(output)
print(f"Saved to {output}")