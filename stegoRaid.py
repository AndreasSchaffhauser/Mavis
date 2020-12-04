import sys
import optparse
from pathlib import Path
from os import listdir
from os.path import isfile, join
import csv


i = 0
class Image:
	def __init__(self, number, name, size):
		self.number = number
		self.name = name
		self.size = size
		self.malicious_mode_1 = False
		self.malicious_mode_2 = False
		self.time_detection_mode_1 = 0
		self.time_detection_mode_2 = 0
		self.time_estimation = 0
		self.script_estimation = 0
		self.time_extraction = 0
		self.script_extraction = 0

#true/false for malicious/benig, number for the time needed
def detection_mode_1(file):
	return True, 1234

def detection_mode_2(file):
	return True, 1234

#first value for the size of the script, second valie for the time needed
def payload_estimation(file):
	return 1234, 5678

def payload_extraction(file):
	return 'string', 5678

def image_process(path_to_image):
	global i
	image_to_process = Image(i, path_to_image, Path(path_to_image).stat().st_size)
	image_to_process.malicious_mode_1, image_to_process.time_detection_mode_1 = detection_mode_1(path_to_image)
	image_to_process.malicious_mode_2, image_to_process.time_detection_mode_2 = detection_mode_2(path_to_image)
	if (image_to_process.malicious_mode_1 and not image_to_process.malicious_mode_2) or (not image_to_process.malicious_mode_1 and image_to_process.malicious_mode_2):
		image_to_process.script_estimation, image_to_process.time_estimation = payload_estimation(path_to_image)
		image_to_process.script_extraction, image_to_process.time_extraction = payload_extraction(path_to_image)
	elif image_to_process.malicious_mode_1 and image_to_process.malicious_mode_2:
		print("dunno")
	#not necessary, all class variables are already set
	#elif not image_to_process.malicious_mode_1 and not image_to_process.malicious_mode_2:
	i += 1
	return image_to_process

def write_to_csv(array, csv_file_name):
	with open(csv_file_name, mode='a') as file:
		writer = csv.writer(file, delimiter=',')
		writer.writerow(['No.', 'Name', 'Size', 'Malicious_1?', 'Malicious_2?', 'Payload size', 
			'Detection time_1', 'Detection time_2', 'Estimation time', 'Extraction time'])
		for x in array:
			writer.writerow([x.number, x.name, x.size, x.malicious_mode_1, x.malicious_mode_2, x.script_estimation, 
				x.time_detection_mode_1, x.time_detection_mode_2, x.time_estimation, x.time_extraction])

def process_command_line(argv):
	parser = optparse.OptionParser()

	parser.add_option(
		'-f',
		'--file',
		help='Specify the file (image in png) that you want to check',
		action='store',
		type='string',
		dest='file'
	)

	parser.add_option(
		'-d',
		'--directory',
		help='Specify the directory which contains file (images in png) that you want to check',
		action='store',
		type='string',
		dest='directory'
	)

	parser.add_option(
		'-c',
		'--csv',
		help='Write the output log to a csv file: default is to wrote on the shell',
		action='store',
		type='string',
		dest='csv'
	)

	settings, args = parser.parse_args(argv)

	if not settings.file and not settings.directory:
		raise ValueError("You should specify a file or a directory!")
	if settings.file and settings.directory:
		raise ValueError("You can specify a file or a directory!")
	if settings.file and not settings.file.endswith('.png'):
		raise ValueError("The file should be a .png!")

	return settings, args

if __name__ == "__main__":

	settings,args = process_command_line(sys.argv)
	if settings.file:
		processed_image = image_process(settings.file)
		#write_to_shell(processed_image)
	else:
		only_png_files = [f for f in listdir(settings.directory) if isfile(join(settings.directory, f)) and f.endswith('.png')]
		obj_array = []
		for png in only_png_files:
			obj_array.append(image_process(settings.directory + '/' + str(png)))
		if settings.csv:
			write_to_csv(obj_array, settings.csv)
		#else:
		#	write_to_shell(obj_array)






