import cv2
import shutil
import image_to_ascii
import sys

aspect_ratio = 1.5
if len(sys.argv) == 2:
	aspect_ratio = float(sys.argv[1])
elif len(sys.argv) > 2:
	aspect_ratio = float(sys.argv[1])
	video = True


term_width, term_height = shutil.get_terminal_size((80,30))
image_width = int(term_width/aspect_ratio)
image_height = term_height

camera = cv2.VideoCapture(0)
while True:
	result, image = camera.read()
	cv2.imwrite("/tmp/cam_dump.png",image)

	frame = image_to_ascii.image_to_ascii("/tmp/cam_dump.png",image_width,image_height,contrast=50,colour=True)
	print("\033[2J")
	print(frame)
	if not video:
		break
