import csv
import os
import json
import ast
import sys, getopt


def parse(ifile, ofile):
	'''
	Check if the input and output files end with a 
	JSON extension since the files o TensorBox should
	be in JSON format

	Parameters
	-----------
	ifile: Input file which contains the data to be be
	converted to TensorBox json file format

	ofile: Output file which will be used with Tensorbox

	Returns
	--------
	True: If both files are in JSON format
	False: If one of the files is not a JSON file
	'''

	ifile_name_split = ifile.split(".")
	ofile_name_split = ofile.split(".")

	if ifile_name_split > 1 and ofile_name_split > 1:
		if ifile_name_split[-1].lower() == "csv" and ofile_name_split[-1].lower() == "json":
			return True
		else:
			return None
	return None

def main(argv):

	'''
	Convert csv files to JSON file. The input csv file
	is the file that was downloaded from the web app with 
	a specific format. The output json file is formatted based 
	on the file format rules used for TensorBox input files. 

	The input file format for TensorBox is: 
	[
		{
			image_path: ..
			rects: [{x1:.., y1:..., x2:..., y2:...}]
		},
		{
			image_path: ..
			rects: [{x1:.., y1:..., x2:..., y2:...}]
		},
		.......

	]
	'''
	inputfile = ''
	outputfile = ''
	img_directory = ''

	try:
		opts, args = getopt.getopt(argv,"hi:o:d:",["ifile=", "ofile=", "direct="])
	except getopt.GetoptError:
		print 'convert_csv_to_json.py -i <input_csv_file> -o <output_json_file> -d <image_directory>'	
		sys.exit(2)

	print len(sys.argv )
	if len(sys.argv ) >= 7:
		for opt, arg in opts:
			if opt == '-h':
				print 'convert_csv_to_json.py -i <input_csv_file> -o <output_json_file> -d <image_directory>' 
				sys.exit()
			elif opt in ("-i", "--ifile"):
				inputfile = arg
			elif opt in ("-o", "--ofile"):
				outputfile = arg
			elif opt in ("-d", "--direct"):
				img_directory = arg
	else:
		print 'convert_csv_to_json.py -i <input_csv_file> -o <output_json_file> -d <image_directory>'
		sys.exit(2)

	if not parse(inputfile, outputfile):
		print 'convert_csv_to_json.py -i <input_csv_file> -o <output_json_file> -d <image_directory>'
		sys.exit(2) 

	json_array = []

	file_exists = os.path.isfile(inputfile)

	# conver tot absolute path
	img_directory = os.path.abspath(img_directory)
	img_directory_exist = os.path.isdir(img_directory)

	# check if image directory exists
	if not img_directory_exist:
		print "Image directory does not exist"
		sys.exit(2)

	if file_exists:
		with open(inputfile, 'r') as csv_file:
			# skip the headers
			next(csv_file)
			
			# create a list of dictionaries for each line
			for line in csv_file:
				d = {}
				print line
				line_split = line.split("\"")
				
				imgfile_name = img_directory+"/"+line_split[0]
				d['image_path'] = imgfile_name[:-1]

				try:
					line_split[1] != "[]"
					line_split[1] = line_split[1][1:]
					line_split[1] = line_split[1][:-1]

					temp_array = ast.literal_eval(line_split[1])

					#duck-typing
					var_type = isinstance(temp_array, (list, tuple))

					rects_array = []

					if var_type:
						# list if there iis more than one rectangle
						if type(temp_array) == type([]):
							rects_array.append({'x1':temp_array[0], 'y1':temp_array[1], 'x2':temp_array[2], 'y2':temp_array[3]})
						# tuple if there is one rectangle
						elif type(temp_array) == type(()):
							for (index, _) in enumerate(temp_array):
								coords = {'x1':temp_array[index][0], 'y1':temp_array[index][1], 'x2':temp_array[index][2], 'y2':temp_array[index][3]}
								rects_array.append(coords)
					d['rects'] = rects_array
					 
					json_array.append(d)

				except IndexError:
					#create image object
					d['image_path'] = d['image_path'].split(",")[0]
					d['rects'] = []
					json_array.append(d)

			with open(outputfile, 'wb') as test_out_file:
				json.dump(json_array, test_out_file)

	else:
		print "Input file not found"
		sys.exit()


if __name__ == "__main__":
	main(sys.argv[1:])


