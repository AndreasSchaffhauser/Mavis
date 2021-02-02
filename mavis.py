import sys
import optparse
import os
import csv
import numpy as np
import time
from pathlib import Path
from os import listdir
from os.path import isfile, join
from PIL import Image
from collections import Counter 


class Process_Image:
	def __init__(self, path, size):
		self.path = path
		self.size = size
		self.malicious_mode_1 = None
		self.time_detection_mode_1 = None
		self.malicious_mode_2 = None
		self.time_detection_mode_2 = None
		self.estimated_script_size = 0
		self.time_estimation = None
		self.extracted_script = None
		self.time_extraction = None

	def __str__(self):
		return 'path: ' + str(self.path) + '\n' + \
			   'size [bytes]: ' + str(self.size) + '\n' + \
		       'malicious_mode_1: ' + str(self.malicious_mode_1) + '\n' + \
			   'time_detection_mode_1 [ms]: ' + str(self.time_detection_mode_1) + '\n' + \
		       'malicious_mode_2: ' + str(self.malicious_mode_2) + '\n' + \
			   'time_detection_mode_2 [ms]: ' + str(self.time_detection_mode_2) + '\n' + \
			   'estimated_script_size [bytes]: ' + str(self.estimated_script_size) + '\n' + \
			   'time_estimation [ms]: ' + str(self.time_estimation) + '\n' + \
			   'extracted_script: ' + str(self.extracted_script) + '\n' + \
			   'time_extraction [ms]: ' + str(self.time_extraction)

def countDistinct(arr):
	return len(Counter(arr).keys())

def detection_mode_1(file):
	
	im = Image.open(file.path)
	try:
		r,g,b = im.split()
	except ValueError:
		print('Too few colour channels present, can\'t hide data, hence clean file!')

	r_arr = np.array(r)
	r_newarr = r_arr.reshape(-1)

	g_arr = np.array(g)
	g_newarr = g_arr.reshape(-1)

	b_arr = np.array(b)
	b_newarr = b_arr.reshape(-1)
	
	t_start = time.perf_counter()

	file.malicious_mode_1 = True
	for j in range(len(r_newarr)):
		if r_newarr[j] < 9 or (r_newarr[j] > 10 and r_newarr[j] < 32) or r_newarr[j] > 126:
			file.malicious_mode_1 = False
			break
		if g_newarr[j] < 9 or (g_newarr[j] > 10 and g_newarr[j] < 32) or g_newarr[j] > 126:
			file.malicious_mode_1 = False
			break
		if g_newarr[j] < 9 or (g_newarr[j] > 10 and g_newarr[j] < 32) or g_newarr[j] > 126:
			file.malicious_mode_1 = False
			break

	t_stop = time.perf_counter()
	file.time_detection_mode_1 = (t_stop - t_start) * 1000
	file.time_detection_mode_1 = round(file.time_detection_mode_1, 2)

def detection_mode_2(file):
	im = Image.open(file.path)
	try:
		r,g,b = im.split()
	except ValueError:
		print('Too few colour channels present, can\'t hide data, hence clean file!')

	r_arr = np.array(r)
	r_newarr = r_arr.reshape(-1)

	t_start = time.perf_counter()

	arr = [x & (0x0f) for x in r_newarr[::+109]]
	file.malicious_mode_2 = countDistinct(arr) < 2 

	t_stop = time.perf_counter()
	file.time_detection_mode_2 = (t_stop - t_start) * 1000
	file.time_detection_mode_2 = round(file.time_detection_mode_2, 2)

def payload_estimation_mode_1(file):
	im = Image.open(file.path)
	try:
		r,g,b = im.split()
	except ValueError:
		print('Too few colour channels present, can\'t hide data, hence clean file!')

	r_arr = np.array(r)
	r_newarr = r_arr.reshape(-1)

	g_arr = np.array(g)
	g_newarr = g_arr.reshape(-1)

	b_arr = np.array(b)
	b_newarr = b_arr.reshape(-1)

	t_start = time.perf_counter()

	tmp = []

	for x in range(len(r_newarr)):
		tmp.append(b_newarr[x])
		tmp.append(g_newarr[x])
		tmp.append(r_newarr[x])

	ending = 0
	for x in range(len(tmp)-113):
		if tmp[x] == tmp[x+113]:
			ending+=1
		else:
			ending=0

	pattern = []

	if ending > 0:
		pattern = tmp[-ending:]
		for i in range(len(tmp)-113):
			if tmp[i:ending+i] == pattern:
				break
			else:
				file.estimated_script_size += 1
	else:
		file.estimated_script_size = -1

	t_stop = time.perf_counter()
	file.time_estimation = (t_stop - t_start) * 1000
	file.time_estimation = round(file.time_estimation, 2)

def payload_estimation_mode_2(file):
	im = Image.open(file.path)
	try:
		r,g,b = im.split()
	except ValueError:
		print('Too few colour channels present, can\'t hide data, hence clean file!')

	g_arr = np.array(g)
	g_newarr = g_arr.reshape(-1)

	b_arr = np.array(b)
	b_newarr = b_arr.reshape(-1)

	t_start = time.perf_counter()

	tmp1_before = []
	tmp2_before = []

	for i in range(int(len(b_newarr) / 113)):

		tmp1 = [k&0x0f for k in b_newarr[i*113:(i+1)*113]]
		tmp2 = [k&0x0f for k in b_newarr[(i+1)*113:(i+2)*113]]

		if tmp1 != tmp2:
			tmp1_before = tmp1
			tmp2_before = tmp2
			file.estimated_script_size += 113
		else:
			for j in range(len(tmp1_before)):
				if tmp1_before[j:] == tmp2_before[j:]:
					file.estimated_script_size -= len(tmp1_before[j:])
					break
			break

	if g_newarr[file.estimated_script_size]&0x0f != g_newarr[file.estimated_script_size+67]&0x0f:
		file.estimated_script_size += 1

	t_stop = time.perf_counter()
	file.time_estimation = (t_stop - t_start) * 1000
	file.time_estimation = round(file.time_estimation, 2)

def payload_extraction_mode_1(file):
	
	im = Image.open(file.path)
	try:
		r,g,b = im.split()
	except ValueError:
		print('Too few colour channels present, can\'t hide data, hence clean file!')

	r_arr = np.array(r)
	r_newarr = r_arr.reshape(-1)

	g_arr = np.array(g)
	g_newarr = g_arr.reshape(-1)

	b_arr = np.array(b)
	b_newarr = b_arr.reshape(-1)

	t_start = time.perf_counter()

	file.extracted_script = ''
	tmp = []

	for x in range(len(r_newarr)):
		tmp.append(b_newarr[x])
		tmp.append(g_newarr[x])
		tmp.append(r_newarr[x])
	
	for i in range(file.estimated_script_size):
		file.extracted_script += chr(tmp[i])

	t_stop = time.perf_counter()
	
	file.time_extraction = (t_stop - t_start) * 1000
	file.time_extraction = round(file.time_extraction, 2)

def payload_extraction_mode_2(file):
	
	im = Image.open(file.path)
	try:
		r,g,b = im.split()
	except ValueError:
		print('Too few colour channels present, can\'t hide data, hence clean file!')

	g_arr = np.array(g)
	g_newarr = g_arr.reshape(-1)

	b_arr = np.array(b)
	b_newarr = b_arr.reshape(-1)

	t_start = time.perf_counter()

	file.extracted_script = ''
	
	for i in range(file.estimated_script_size):
		tmp = (b_newarr[i]&0x0f) * 16 + (g_newarr[i]&0x0f)
		file.extracted_script += chr(tmp)
	t_stop = time.perf_counter()
	
	file.time_extraction = (t_stop - t_start) * 1000
	file.time_extraction = round(file.time_extraction, 2)

def write_to_csv(image, csv_file_name):
	
	csv_exists = os.path.isfile(csv_file_name)

	with open(csv_file_name, mode='a', newline='', encoding='utf-8') as file:
		writer = csv.writer(file, delimiter=';', quotechar='"', quoting=csv.QUOTE_MINIMAL)
		if not csv_exists:
			writer.writerow(['Path', \
				'Size', \
				'Malicious_1?', \
				'Time Detection Mode-1', \
				'Malicious_2?', \
				'Time Detection Mode-2', \
				'Estimated Script Size', \
				'Time Estimation', \
				'Extracted Script', \
				'Time Extraction'])

		writer.writerow([image.path, \
			image.size, \
			image.malicious_mode_1, \
			str(image.time_detection_mode_1).replace('.', ','), \
			image.malicious_mode_2, 
			str(image.time_detection_mode_2).replace('.', ','), \
			image.estimated_script_size, \
			str(image.time_estimation).replace('.', ','), \
			image.extracted_script, \
			str(image.time_extraction).replace('.', ',')])

def write_to_shell(number_of_file,  number_of_all_files, file):

	print('# ==================== File ' + str(number_of_file + 1) + '/' + str(number_of_all_files) + ' ==================== #')
	print('- Path: ' + str(file.path))
	print('- Image size: ' + str(file.size) + ' B')
	print('- Malicious/Benign: ', end='')
	if not file.malicious_mode_1 and not file.malicious_mode_2:
		print('Benign File :-)')
	elif file.malicious_mode_1 and not file.malicious_mode_2:
		print('PSI Mode-1 detected!')
	elif not file.malicious_mode_1 and file.malicious_mode_2:
		print('PSI Mode-2 detected!')
	else:
		print('PSI both modes detected! I am confused!')
	print('- Time Detection Mode-1: ' + str(file.time_detection_mode_1) + ' ms')
	print('- Time Detection Mode-2: ' + str(file.time_detection_mode_2) + ' ms')
	
	if file.malicious_mode_1 or file.malicious_mode_2:
		print('- Estimated Script Size: ', end='')
		if file.estimated_script_size > -1:
			print(str(file.estimated_script_size) + ' B')
		else:
			print("No reliable Pattern Detection!")
		print('- Time for Estimation: ' + str(file.time_estimation) + ' ms')
		print('- Extracted Script: ' + str(file.extracted_script))
		print('- Time for Extraction: ' + str(file.time_extraction) + ' ms')

	for x in range(len('# ==================== File ' + str(number_of_file) + '/' + str(number_of_all_files) + ' ==================== #')):
		if x == 0 or x == len('# ==================== File ' + str(number_of_file) + '/' + str(number_of_all_files) + ' ==================== #') - 1:
			print('#', end='')
		if x == 1 or x == len('# ==================== File ' + str(number_of_file) + '/' + str(number_of_all_files) + ' ==================== #') - 2:
			print(' ', end='')
		elif x > 1 and x < len('# ==================== File ' + str(number_of_file) + '/' + str(number_of_all_files) + ' ==================== #') - 2:
			print('=', end='')
	print()
	print()

def process_command_line(argv):
	parser = optparse.OptionParser()

	parser.add_option(
		'-f',
		'--file',
		help='Specify the file (PNG-format) that you want to check',
		action='store',
		type='string',
		dest='file'
	)

	parser.add_option(
		'-d',
		'--directory',
		help='Specify the directory which contains files (PNG-format) that you want to check',
		action='store',
		type='string',
		dest='directory'
	)

	parser.add_option(
		'-c',
		'--csv',
		help='Write the output log to a csv file: default is to write on the shell',
		action='store',
		type='string',
		dest='csv'
	)

	settings, args = parser.parse_args(argv)

	# Both set
	if settings.file and settings.directory:
		raise ValueError("You can't specify a path to a file AND to a  directory!")
	# None of both set
	elif not settings.file and not settings.directory:
		raise ValueError("You have to specify a path to a file XOR a path to a directory!")
	# Either or Set
	else:
		# File set, but not regular file
		if settings.file and not os.path.isfile(settings.file):
			raise ValueError("Specified path to file is not a regular file!")
		# File set, regular file, but not a *.png
		if settings.file and not settings.file.endswith('.png'):
			raise ValueError("The file should be a .png!")
		# Directory set, but not a directory
		if settings.directory and not os.path.isdir(settings.directory):
			raise ValueError("Specified path to directory is not a directory!")

	return settings, args

if __name__ == "__main__":

	settings,args = process_command_line(sys.argv)

	files = []

	if settings.file:
		files.append(Process_Image(settings.file, Path(settings.file).stat().st_size))		
	else:
		files = [Process_Image(settings.directory + f, Path(settings.directory + f).stat().st_size) for f in listdir(settings.directory) if isfile(join(settings.directory, f)) and f.endswith('.png')]
	
	for x in range(len(files)):

		detection_mode_1(files[x])
		detection_mode_2(files[x])

		# mode-1 pictures can trigger mode-2 alarms.
		# mode-2 pictures can NOT trigger mode-1 alarms.
		if files[x].malicious_mode_1 and files[x].malicious_mode_2:
			files[x].malicious_mode_2 = False

		if files[x].malicious_mode_1 and not files[x].malicious_mode_2:
			payload_estimation_mode_1(files[x])
			payload_extraction_mode_1(files[x])

		if files[x].malicious_mode_2 and not files[x].malicious_mode_1:
			payload_estimation_mode_2(files[x])
			payload_extraction_mode_2(files[x])

		if settings.csv:
			write_to_csv(files[x], settings.csv)
		else:
			write_to_shell(x, len(files), files[x])

