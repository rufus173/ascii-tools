import cv2
from PIL import Image
import shutil
import image_to_ascii
import sys
import numpy as np

def parse_args(argv):
	short = []
	long = []
	other = []
	for arg in argv:
		if arg[0] != "-":
			other.append(arg)
		if len(arg) > 1:
			if arg[0] == "-":
				if arg[1] == "-":
					long.append(arg[2:])
				else:
					[short.append(char) for char in argv[1:]]
	return short, long, other


aspect_ratio = 0.7

short_args, long_args, other_args = parse_args(sys.argv)

for arg in long_args:
	arg = arg.split("=")
	if "width-scale" in arg:
		aspect_ratio = float(arg[1])

term_width, term_height = shutil.get_terminal_size((80,30))
image_width = int(term_width*aspect_ratio)
image_height = term_height

camera = cv2.VideoCapture(0)
if "video" in long_args:
	while True:
		result, image = camera.read()
		image_array = cv2.cvtColor(image,cv2.COLOR_BGR2RGB)
		#Image.fromarray(image_array).show()

		pil_image = Image.fromarray(image_array)
		image_array = np.asarray(pil_image.resize((image_width,image_height)))
		frame = image_to_ascii.np_array_to_ascii(image_array,colour=True)
		print("\033[2J")
		print(frame)
		#break
else:
		result, image = camera.read()
		cv2.imwrite("/tmp/cam_output.png",image)

		image_array = cv2.cvtColor(image,cv2.COLOR_BGR2RGB)
		pil_image = Image.fromarray(image_array)
		image_array = np.asarray(pil_image.resize((image_width,image_height)))
		frame = image_to_ascii.np_array_to_ascii(image_array,colour=True)
		print("\033[2J")
		print(frame)

