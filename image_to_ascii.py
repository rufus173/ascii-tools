from PIL import Image
from pathlib import Path
def brightness_to_char(brightness):
	#darkest_to_brightest = ["#","0","O","x","*","?",">","~","."," "]
	darkest_to_brightest = list("$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\\|()1{}[]?-_+~<>i!lI;:,\"^`\'. ")

	brightness = round(brightness,1)
	index = brightness*(len(darkest_to_brightest)-1)
	index = int(round(index,0))
	return darkest_to_brightest[::-1][index]
# thank you https://stackoverflow.com/questions/42045362/change-contrast-of-image-in-pil for this function
def change_contrast(img, level):
    factor = (259 * (level + 255)) / (255 * (259 - level))
    def contrast(c):
        return 128 + factor * (c - 128)
    return img.point(contrast)

def image_to_ascii(image_path,target_width,target_height,contrast=0):
	frame = ""
	# preprocessing
	image = Image.open(Path(image_path))
	image = image.convert("L") # greyscale
	image = image.resize((target_width,target_height))
	if contrast != 0:
		image = change_contrast(image,contrast)
	# build the frame
	for y in range(image.height):
		line = ""
		for x in range(image.width):
			pixel = image.getpixel((x,y))
			brightness = pixel/255 # between 0 and 1
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
	term_width, term_height = shutil.get_terminal_size((80,30))
	print(image_to_ascii(sys.argv[1],int(term_width/1.5),term_height,contrast=50))
