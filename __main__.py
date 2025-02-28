import shutil
from multiprocessing import Process, Lock, Queue
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
	max_threads = 4
	def __init__(self,image_storage):
		self.converted_buffer = []
		self.converted_buffer_lock = Lock()
	def converter_thread(self,converted_queue,image_array,target_width,target_height):
		for image in image_array:
			frame = image_to_ascii(image,target_width,target_height)
			converted_queue.put(frame)
	def convert_and_play(self,image_storage,target_width,target_height,fps):
		#dispatch converter threads
		converted_queues = [Queue() for i in range(self.max_threads)]
		converter_threads = [
			Process(
				target=self.converter_thread,
				args=(
					converted_queues[i],
					list(image_storage)[i::self.max_threads],
					target_width,
					target_height,
				)
			) for i in range(self.max_threads)
		]
		[thread.start() for thread in converter_threads]
			

		#start playing
		time_at_next_frame = time.time() + (1/fps)
		for image in image_storage:
			# retrieve more frames if the buffer is out
			if len(self.converted_buffer) < 1:
				[
					self.converted_buffer.append(queue.get(block=True))
					for queue in converted_queues
				]
					
			# grab the next available frame
			frame = None
			print(len(self.converted_buffer))
			frame = self.converted_buffer.pop(0)

			#display
			print("\033[2J")
			print(frame.strip("\n"))

			# chill untill we have to display the next frame
			sleep_time = time_at_next_frame-time.time()
			if sleep_time > 0:
				time.sleep(sleep_time)

			# calc when we need to wake back up again after rendering the next frame
			# calc stands for calculate btw chat
			time_at_next_frame = time_at_next_frame+(1/fps)


		# clean up after our threads
		for thread in converter_threads:
			thread.start()

# load the images (sampled at 8 fps)
print("loading...")
term_width, term_height = shutil.get_terminal_size((80,30))
# argv to set the directory back to this repo
images = ImageStorage(Path(argv[0])/Path("images"))
frames = FrameStorage(images)
frames.convert_and_play(images,term_width,term_height,24)
