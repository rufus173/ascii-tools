from PIL import Image
import time
from pathlib import Path
class ImageStorage():
	def __init__(self,directory):
		self.image_dir = Path(directory)
		# load all the images into an array
		self.image_array = [
			file for file in self.image_dir.iterdir()
		]
		self.image_array.sort(key = lambda path : int(path.name[:-4]))
	def get_image(self,index):
		return self.image_array(index)
	def __len__(self):
		return len(self.image_array)
	def __iter__(self):
		for image in self.image_array:
			yield image

class FrameStorage():
	def __init__(self,image_storage,target_x,target_y):
		self.frame_buffer = []
		self.time_at_next_frame = 0
	def convert_and_play(self,image_storage,target_x,target_y,fps):
		for image in image_storage:
			start_time = time.time()
			frame = self.image_to_frame(image,target_x,target_y)
			print(frame)
			while self.time_at_next_frame > time.time():
				pass
			self.time_at_next_frame = start_time+(1/fps)
	def image_to_frame(self,image,target_x,target_y):
		frame = ""
		# preprocessing
		image = Image.open(image)
		image = image.convert("L") # greyscale
		image = image.resize((target_x,target_y))
		# build the frame
		for y in range(target_x):
			line = ""
			for x in range(target_y):
				pixel = image.getpixel((x,y))
				brightness = pixel/255 # between 0 and 1
				if brightness > 0.5:
					line += "#"
				else:
					line += " "
			frame += line + "\n"
			

		#image.save("res.png","PNG")
		image.close()
		return frame
# load the images (sampled at 8 fps)
print("loading...")
images = ImageStorage("images")
frames = FrameStorage(images,50,50)
frames.convert_and_play(images,50,50,16)
