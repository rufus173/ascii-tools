from PIL import Image
from pathlib import Path
def brightness_to_char(brightness):
	darkest_to_brightest = ["#","0","O","."," "]

	brightness = round(brightness,1)
	index = brightness*(len(darkest_to_brightest)-1)
	index = int(round(index,0))
	return darkest_to_brightest[index]
def image_to_ascii(image_path,target_width,target_height):
	frame = ""
	# preprocessing
	image = Image.open(Path(image_path))
	image = image.convert("L") # greyscale
	image = image.resize((target_width,target_height))
	# build the frame
	for y in range(image.height):
		line = ""
		for x in range(image.width):
			pixel = image.getpixel((x,y))
			brightness = pixel/255 # between 0 and 1
			line += brightness_to_char(brightness)
		frame += line + "\n"
	image.close()
	return frame
