from PIL import Image
from pathlib import Path
class ImageStorage():
	def __init__(self,directory,fps):
		self.image_dir = Path(directory)
		self.fps = fps
		# load all the images into an array
		self.image_array = [
			file for file in self.image_dir.iterdir()
		]
		self.image_array.sort(key = lambda path : int(path.name[:-4]))
		for image in self.image_array:
			print(image.name)


# load the images (sampled at 8 fps)
images = ImageStorage("images",8)
