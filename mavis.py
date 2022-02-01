import sys
import optparse
import os
import csv
import numpy as np
import time
import shutil
import json
import uuid

from pathlib import Path
from os import listdir
from os.path import isfile, join
from PIL import Image
from PIL import UnidentifiedImageError
from collections import Counter
from datetime import datetime
# from kafka import KafkaProducer


class Process_Image:
	def __init__(self, path, size):
		self.path = path
		self.size = size
		self.malicious_mode_1 = False
		self.time_detection_mode_1 = 0.0
		self.malicious_mode_2 = False
		self.time_detection_mode_2 = 0.0
		self.estimated_script_size = 0
		self.time_estimation = 0.0
		self.extracted_script = "No script extracted!"
		self.time_extraction = 0.0
		self.script_functionality = "No category determined!"

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
			   'time_extraction [ms]: ' + str(self.time_extraction) + '\n' + \
			   'script_functionality: ' + str(script_functionality)

def countDistinct(arr):
	return len(Counter(arr).keys())

def detection_mode_1(file, r_newarr, g_newarr, b_newarr):
	
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

def detection_mode_2(file, r_newarr, g_newarr, b_newarr):

	t_start = time.perf_counter()

	# ------------ DETECTION PoC ------------ #

	# arr = []
	# for i in range(4):
	# 	for j in range(100):
	# 		arr.append((r_newarr[i+109*j])&(0x0f))
	# file.malicious_mode_2 = (countDistinct(arr)<5):

	# ------------ DETECTION PoC ------------ #

	# ----------- DETECTION Mavis ----------- #

	arr_1 = [x & (0x0f) for x in r_newarr[::+109]]
	arr_2 = [x for x in g_newarr[::+109]]
	arr_3 = [x for x in b_newarr[::+109]]
	# red channel is the positiv criterion
	# green & blue channel is the false positive criterion (e.g. when analyzing monotonous images)
	file.malicious_mode_2 = countDistinct(arr_1) < 2 and countDistinct(arr_2) > 4 and countDistinct(arr_3) > 4
    
    # ----------- DETECTION Mavis ----------- #

	t_stop = time.perf_counter()
	file.time_detection_mode_2 = (t_stop - t_start) * 1000
	file.time_detection_mode_2 = round(file.time_detection_mode_2, 2)

def payload_estimation_mode_1(file, r_newarr, g_newarr, b_newarr):

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

def payload_estimation_mode_2(file, g_newarr, b_newarr):

	t_start = time.perf_counter()

	# ------------ Payload Estimation PoC ------------ # 
	
	# idems = []
	# datasize = len(g_newarr) - 67
	# for i in range(datasize):
	# 	if ((g_newarr[i]&0x0f) == (g_newarr[i+67]&0x0f)):
	# 		idems.append(i)
	# diff = np.diff(idems)
	# res = diff[::-1]
	# occurrences = np.count_nonzero(res == 1)
	# i = 0
	# while(i < len(res) and res[i] == 1):
	# 	i = i + 1
	# idems = []
	# datasize = len(b_newarr) - 113
	# for i in range(datasize):
	# 	if ((b_newarr[i]&0x0f) == (b_newarr[i+113]&0x0f)):
	# 		idems.append(i)
	# diff = np.diff(idems)
	# res = diff[::-1]
	# occurrences = np.count_nonzero(res == 1)
	# i = 1
	# while(i<len(res) and res[i] == 1):
	# 	i = i + 1
	# file.estimated_script_size = datasize - i - 1

	# ------------ Payload Estimation PoC ------------ # 


	# ------------ Payload Estimation Mavis ------------ # 

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

	# ------------ Payload Estimation Mavis ------------ # 

	t_stop = time.perf_counter()
	file.time_estimation = (t_stop - t_start) * 1000
	file.time_estimation = round(file.time_estimation, 2)

def payload_extraction_mode_1(file, r_newarr, g_newarr, b_newarr):
	
	if file.estimated_script_size == - 1:
		file.extracted_script = "No extraction possible!"
	else:
		t_start = time.perf_counter()

		file.extracted_script = ''
		tmp = []

		for x in range(len(r_newarr)):
			tmp.append(b_newarr[x])
			tmp.append(g_newarr[x])
			tmp.append(r_newarr[x])
		
		for i in range(file.estimated_script_size):
			file.extracted_script += chr(tmp[i])
		file.extracted_script = file.extracted_script.replace("\n", " ")
		t_stop = time.perf_counter()
		
		file.time_extraction = (t_stop - t_start) * 1000
		file.time_extraction = round(file.time_extraction, 2)

def payload_extraction_mode_2(file, g_newarr, b_newarr):
	
	t_start = time.perf_counter()

	file.extracted_script = ''
	
	for i in range(file.estimated_script_size):
		tmp = (b_newarr[i]&0x0f) * 16 + (g_newarr[i]&0x0f)
		file.extracted_script += chr(tmp)
	file.extracted_script = file.extracted_script.replace("\n", " ")
	t_stop = time.perf_counter()
	
	file.time_extraction = (t_stop - t_start) * 1000
	file.time_extraction = round(file.time_extraction, 2)

def determine_script_functionality_by_its_size(file, obfuscation="deobfuscated"):

	mean_value_malware_rest = 265.37
	mean_value_shellexecute = 513.72
	mean_value_memset = 2354.7

	obfuscation_factor = 0

	if obfuscation == "deobfuscated":
		obfuscation_factor = 1
	elif obfuscation == "ascii":
		obfuscation_factor = 4.194446103579311
	elif obfuscation  == "ast":
		obfuscation_factor = 1.096724269206056
	elif obfuscation == "token":
		obfuscation_factor = 2.028516722292627
	elif obfuscation == "string":
		obfuscation_factor = 1.7949865327280152
	else:
		raise ValueError("Unknown Obfuscation Technique!")

	means = [mean_value_malware_rest, mean_value_shellexecute, mean_value_memset]
	means = [x * obfuscation_factor for x in means]
	absolute_difference_function = lambda list_value : abs(list_value - file.estimated_script_size)
	closest_value = min(means, key=absolute_difference_function)

	if closest_value == mean_value_malware_rest:
		file.script_functionality = "malware/rest"
	elif closest_value == mean_value_shellexecute:
		file.script_functionality = "shellexecute"
	elif closest_value == mean_value_memset:
		file.script_functionality = "memset"
	else:
		raise ValueError("Unknown Script Functionality!")

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
				'Time Extraction', \
				'Functionality'])

		writer.writerow([image.path, \
			image.size, \
			image.malicious_mode_1, \
			str(image.time_detection_mode_1).replace('.', ','), \
			image.malicious_mode_2, 
			str(image.time_detection_mode_2).replace('.', ','), \
			image.estimated_script_size, \
			str(image.time_estimation).replace('.', ','), \
			image.extracted_script, \
			str(image.time_extraction).replace('.', ','), \
			image.script_functionality])

def write_json_file(file, dir_name_json1, dir_name_json2):

	json_file_name = os.path.basename(file.path)
	json_file_name = json_file_name.replace("png", "json")
	
	detected_mode = "mode-"
	if file.malicious_mode_1:
		detected_mode += "1"
	if file.malicious_mode_2:
		detected_mode += "2"

	result_dict = { "label": "Mavis Examination",
		"description": "Examination of file " + str(file.path),
		"data": { "file": str(file.path),
		"detected mode": detected_mode,
		"extracted_script": file.extracted_script },
		"sources": [ { 
			"uuid": str(uuid.uuid4()),
			"markers": [ { 
				"tool": "Mavis",
				"from": str(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
			} ]
		} ]
	}

	# producer = KafkaProducer(bootstrap_servers='217.73.164.210:9094')
	# producer.send('mavis-test', result_dict)

	if file.malicious_mode_1:
		write_path = os.path.join(dir_name_json1, json_file_name)
	else:
		write_path = os.path.join(dir_name_json2, json_file_name)

	with open(write_path, 'w') as json_file:
		json.dump(result_dict, json_file)

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
		print('- Script Functionality: ' + file.script_functionality)

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
		help='Write the output log also to a csv file: default is to write only to the shell',
		action='store',
		type='string',
		dest='csv'
	)

	settings, args = parser.parse_args(argv)

	# Both set
	if settings.file and settings.directory:
		raise ValueError("You can't specify a path to a file AND to a directory!")
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

	if settings.directory:
		settings.directory = Path(settings.directory)

	return settings, args

if __name__ == "__main__":

	settings,args = process_command_line(sys.argv)

	files = []

	dir_name_mal1 = 'malicious_mode_1_files'
	dir_name_mal2 = 'malicious_mode_2_files'

	dir_name_json1 = "json_files_mode_1"
	dir_name_json2 = "json_files_mode_2"

	if settings.file:
		files.append(Process_Image(settings.file, Path(settings.file).stat().st_size))		
	else:
		files = [Process_Image(settings.directory / f, (settings.directory / f).stat().st_size) for f in listdir(settings.directory) if isfile(join(settings.directory, f)) and f.endswith('.png')]
	
	for x in range(len(files)):

		try:

			im = Image.open(files[x].path)

			try:
				r,g,b = im.split()

				r_arr = np.array(r)
				r_newarr = r_arr.reshape(-1)

				g_arr = np.array(g)
				g_newarr = g_arr.reshape(-1)

				b_arr = np.array(b)
				b_newarr = b_arr.reshape(-1)

				detection_mode_1(files[x], r_newarr, g_newarr, b_newarr)
				detection_mode_2(files[x], r_newarr, g_newarr, b_newarr)

				# mode-1 pictures can trigger mode-2 alarms.
				# mode-2 pictures can NOT trigger mode-1 alarms.
				if files[x].malicious_mode_1 and files[x].malicious_mode_2:
					files[x].malicious_mode_2 = False

				if files[x].malicious_mode_1 and not files[x].malicious_mode_2:
					if not os.path.isdir(dir_name_mal1):
						os.mkdir(dir_name_mal1)
						os.mkdir(dir_name_json1)
					shutil.copy2(files[x].path, dir_name_mal1)
					payload_estimation_mode_1(files[x], r_newarr, g_newarr, b_newarr)
					payload_extraction_mode_1(files[x], r_newarr, g_newarr, b_newarr)

				if files[x].malicious_mode_2 and not files[x].malicious_mode_1:
					if not os.path.isdir(dir_name_mal2):
						os.mkdir(dir_name_mal2)
						os.mkdir(dir_name_json2)
					shutil.copy2(files[x].path, dir_name_mal2)
					payload_estimation_mode_2(files[x], g_newarr, b_newarr)
					payload_extraction_mode_2(files[x], g_newarr, b_newarr)

				if (files[x].malicious_mode_1 or files[x].malicious_mode_2) and files[x].estimated_script_size > -1:
					determine_script_functionality_by_its_size(files[x])

				if files[x].malicious_mode_1 or files[x].malicious_mode_2:
					write_json_file(files[x], dir_name_json1, dir_name_json2)

				write_to_shell(x, len(files), files[x])
				
				if settings.csv:
					write_to_csv(files[x], settings.csv)

			except ValueError as ve:
				print(str(files[x].path) + ': wrong color depth! Invoke-PSImage resulting images have always 24-Bit color depth!\n--> hence clean file! (' + str(ve) + ')')

			except IndexError as ie:
				print(str(files[x].path) + ': caused a value error! (' + str(ie) + ')')

		except UnidentifiedImageError as uie:
			print(str(files[x].path) + ': caused a UnidentifiedImageError! (' + str(uie) + ')')

		except Exception as ex:
			print(str(files[x].path) + ': caused an Exception! (' + str(ex) + ')')

