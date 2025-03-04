from PIL import Image
from pathlib import Path
import numpy as np
darkest_to_brightest = list("$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\\|()1{}[]?-_+~<>i!lI;:,\"^`\'. ")[::-1]
def colour_to_escape_code(r,g,b):
	return f"\033[38;2;{r};{g};{b}m"
def brightness_to_char(brightness):
	#darkest_to_brightest = ["#","0","O","x","*","?",">","~","."," "]

	brightness = round(brightness,1)
	index = brightness*(len(darkest_to_brightest)-1)
	index = int(round(index,0))
	return darkest_to_brightest[index]
# thank you https://stackoverflow.com/questions/42045362/change-contrast-of-image-in-pil for this function
def change_contrast(img, level):
    factor = (259 * (level + 255)) / (255 * (259 - level))
    def contrast(c):
        return 128 + factor * (c - 128)
    return img.point(contrast)

def np_array_to_ascii(image_array,colour=False):
	frame = ""
	for pixel_line in image_array:
		line = ""
		for r,g,b in pixel_line:
			char = darkest_to_brightest[int(round(((r+g+b)/(255*3))*(len(darkest_to_brightest)-1),1))]
			if colour:
				line += f"\033[38;2;{r};{g};{b}m" + char + "\033[39m"
			else:
				line += char
		frame += line + "\n"
	return frame
	
def image_to_ascii(image_path,target_width,target_height,contrast=0,colour=False):
	frame = ""
	# preprocessing
	image = Image.open(Path(image_path))
	if colour:
		rgb_image = image.convert("RGB")
	image = image.convert("L") # greyscale
	if contrast != 0:
		image = change_contrast(image,contrast)
	image = image.resize((target_width,target_height))
	if colour:
		rgb_image = rgb_image.resize((target_width,target_height))
	# build the frame
	for y in range(image.height):
		line = ""
		for x in range(image.width):
			pixel = image.getpixel((x,y))
			brightness = pixel/255 # between 0 and 1
			if colour:
				r,g,b = rgb_image.getpixel((x,y))
				line += colour_to_escape_code(r,g,b)
				line += brightness_to_char(brightness)
				line += "\033[39m"

			else:
				line += brightness_to_char(brightness)
				
		frame += line + "\n"
	#image.save("/tmp/out.png","PNG")
	image.close()
	return frame
if __name__ == "__main__":
	import sys
	import shutil
	if len(sys.argv) < 2:
		print("please provide the name of the file")
		quit()
	if len(sys.argv) < 4:
		term_width, term_height = shutil.get_terminal_size((80,30))
		image_width = int(term_width/1.5)
		image_height = term_height
	else:
		image_width = int(sys.argv[2])
		image_height = int(sys.argv[3])
	print(image_to_ascii(sys.argv[1],image_width,image_height,contrast=50))
