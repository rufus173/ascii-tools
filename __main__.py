import shutil
from image_to_ascii import image_to_ascii
import time
from pathlib import Path
from sys import argv
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
	def __init__(self,image_storage):
		self.frame_buffer = []
		self.time_at_next_frame = 0
	def convert_and_play(self,image_storage,target_width,target_height,fps):
		for image in image_storage:
			start_time = time.time()
			frame = image_to_ascii(image,target_width,target_height)
			print("\033[2J")
			print(frame.strip("\n"))
			while self.time_at_next_frame > time.time():
				pass
			self.time_at_next_frame = start_time+(1/fps)
# change directory
print(argv[0])
# load the images (sampled at 8 fps)
print("loading...")
term_width, term_height = shutil.get_terminal_size((80,30))
images = ImageStorage(Path(argv[0])/Path("images"))
frames = FrameStorage(images)
frames.convert_and_play(images,term_width,term_height,16)
