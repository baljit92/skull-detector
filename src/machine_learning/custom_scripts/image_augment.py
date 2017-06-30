'''
Orignial source: https://github.com/vxy10/ImageAugmentation
'''

import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import cv2
import sys, getopt
import numpy as np
import matplotlib.image as mpimg
import os
from PIL import Image
import csv
import ast

Image.Image.tostring = Image.Image.tobytes

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
		if ifile_name_split[-1].lower() == "csv" and ofile_name_split[-1].lower() == "csv":
			return True
		else:
			return None
	return None

def augment_brightness_camera_images(image):
	image1 = cv2.cvtColor(image,cv2.COLOR_RGB2HSV)
	random_bright = .25+np.random.uniform()
	image1[:,:,2] = image1[:,:,2]*random_bright
	image1 = cv2.cvtColor(image1,cv2.COLOR_HSV2RGB)
	return image1

def transform_image(img,ang_range,brightness=0):
	'''
	This function transforms images to generate new images.
	The function takes in following arguments,
	1- Image
	2- ang_range: Range of angles for rotation
	3- shear_range: Range of values to apply affine transform to
	4- trans_range: Range of values to apply translations over.

	A Random uniform distribution is used to generate different parameters for transformation

	'''
	# Rotation

	ang_rot = ang_range
	rows,cols,ch = img.shape    
	Rot_M = cv2.getRotationMatrix2D((cols/2,rows/2),ang_rot,1)

	img = cv2.warpAffine(img,Rot_M,(cols,rows))

	if brightness == 1:
	  img = augment_brightness_camera_images(img)

	return img

def main(argv):

	inputfile = ''
	outputfile = ''
	input_img_directory = ''
	output_img_directory = ''

	try:
		opts, args = getopt.getopt(argv,"hi:o:I:O:",["ifile=", "ofile", "idirect=", "odirect="])
	except getopt.GetoptError:
		print 'image_augment.py -i <training_csv_file> -o <output_csv_file> -I <input_img_directory>  -O <out_img_directory>'	
		sys.exit(2)


	if len(sys.argv) >= 9:
		for opt, arg in opts:
			if opt == '-h':
				print 'image_augment.py -i <training_csv_file> -o <output_csv_file> -I <input_img_directory>  -O <out_img_directory>' 
				sys.exit()
			elif opt in ("-i", "--ifile"):
				inputfile = arg
			elif opt in ("-o", "--ofile"):
				outputfile = arg
			elif opt in ("-I", "--idirect"):
				input_img_directory = arg
			elif opt in ("-O", "--odirect"):
				output_img_directory = arg
	else:
		print 'image_augment.py -i <training_csv_file> -o <output_csv_file> -I <input_img_directory>  -O <out_img_directory>'
		sys.exit(2)

	if not parse(inputfile, outputfile):
		print "Please enter valid CSV file(s)"
		sys.exit(2) 

	file_array = []

	#check if input csv file exists
	input_file_exists = os.path.isfile(inputfile)

	if not input_file_exists:
		print "Input CSV file does not exist"
		sys.exit(2)

	output_file_exists = os.path.isfile(outputfile)

	input_img_directory = os.path.abspath(input_img_directory)
	input_img_directory_exist = os.path.isdir(input_img_directory)

	# check if image directory exists
	if not input_img_directory_exist:
		print "Input image directory does not exist"
		sys.exit(2)

	output_img_directory = os.path.abspath(output_img_directory)
	output_img_directory_exist = os.path.isdir(output_img_directory)

	# check if image directory exists
	if not output_img_directory_exist:
		print "Output image directory does not exist"
		sys.exit(2)

	if input_file_exists:
		with open(inputfile, 'r') as csv_file:

			# skip the headers
			next(csv_file)
			
			# create a list of dictionaries for each line
			for line in csv_file:
				d = {}
				line_split = line.split(",")
				
				imgfile_name = input_img_directory+"/"+line_split[0]
				
				rect_coords = line_split[1].split("[")
				
				temp_split = line.split("\"")
				
				try:
					temp_split[1] != "[]"
					temp_split[1] = temp_split[1][1:]
					temp_split[1] = temp_split[1][:-1]

					temp_array = [ast.literal_eval(temp_split[1])]
				except IndexError:
					temp_array = []
				img_class = int(line_split[-1])
				


				file_name = line_split[0].split('.')[0]
				#print file_name
				file_ext = line_split[0].split('.')[-1]
				if file_ext.lower() not in ['jpg', 'jpeg', 'gif', 'tiff']:
				   continue

				try:
					image = mpimg.imread(imgfile_name)
				except IOError:
					continue


				for i in range(20):
					img = transform_image(image,0,brightness=1)
					im = Image.fromarray(img)
					
					#generate only 5 augmented versions with big variations in the image
					if i%5:
						im.save(output_img_directory+"/"+file_name+"_"+str(i)+"."+file_ext)
						image_new = file_name+"_"+str(i)+"."+file_ext
						
						#write the augmented versions to a csv file with the existin coordinates
						with open(outputfile,'a') as filedata:    

							
							headers = ["imagename","coordinates","class"]
							writer = csv.DictWriter(filedata, delimiter=',', lineterminator='\n',fieldnames=headers)

							if not output_file_exists:
								writer.writeheader()
							writer.writerow({"imagename":image_new, "coordinates":temp_array, "class":img_class})
	else:
		print "Not found"
if __name__ == "__main__":
	main(sys.argv[1:])
