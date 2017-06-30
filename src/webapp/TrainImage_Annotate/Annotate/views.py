from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
import re
import csv
import os
import zipfile
import StringIO
from PIL import Image, ImageDraw
import numpy as np
import fnmatch
import math

def prepareArrayNMS(filename):
	
	# prepares the array that is to be passed to the
	# Non Maximum Suppression function 

	# Parameters:
	# ------------
	# filename : The csv file which contains training image data

	# Returns:
	# ---------
	# An array of tuples for each image. Each tuple contains the
	# (image_name, bounding_box_list, image_class)

	final_imgs = []
	# check if .csv file exists
	file_exists = os.path.isfile(filename)
	if file_exists:
		with open(filename, 'r') as csv_file:
			# skip the headers
			next(csv_file)
			trainingImgs = []
			
			# create a list of dictionaries for each line
			training_img_rect_dict = {}
			training_image_class_dict = {}
			for line in csv_file:
				d = {}
				line_split = line.split(",")

				img_name = line_split[0]

				# parse the coordinates for the bounding box and 
				# store the bounding box coorindate array in dictionary
				box = []
				if line_split[1] != "[]":

					# the raw data can contain N copies for each image 
					# Combine the all bounding box coordinates onto one
					# image
					if img_name in training_img_rect_dict:
						# if the image_name is present in dict; append the
						# box coordinates from other images into on
						bounding_rect = training_img_rect_dict[img_name]
						bounding_rect.append(line_split[1][2:])
						for i in range(2,len(line_split)-2):
							bounding_rect.append(line_split[i])
						bounding_rect.append(line_split[i+1][:-2])
						training_img_rect_dict[img_name] = bounding_rect
					else:
						temp_box = []
						temp_box.append(line_split[1][2:])

						for i in range(2,len(line_split)-2):
							temp_box.append(line_split[i])
						temp_box.append(line_split[i+1][:-2])
						training_img_rect_dict[img_name] = temp_box
						training_image_class_dict[img_name] = line_split[len(line_split)-1][:-1]
				else:	
					training_img_rect_dict[img_name] = []
					training_image_class_dict[img_name] = line_split[len(line_split)-1][:-1]

			for img_file in training_img_rect_dict:
				data = {}
				data['image_name'] = img_file
				data['bounding_box'] = training_img_rect_dict[img_file]
				data['class'] = training_image_class_dict[img_file]

				
				num_rects = len(data['bounding_box'])/6
				box_coords = []
				box_area = []

				# preparing tuples
				for i in range(0,num_rects):

					x0_str = len(data['bounding_box'][(6*i)+0])
					y0_str = len(data['bounding_box'][(6*i)+1])
					x1_str = len(data['bounding_box'][(6*i)+2])
					y1_str = len(data['bounding_box'][(6*i)+0])
					
					if x0_str > 0 and y0_str > 0 and x1_str > 0 and y1_str > 0:
						x0 = math.isnan(float(data['bounding_box'][(6*i)+0]))
						y0 = math.isnan(float(data['bounding_box'][(6*i)+1]))
						x1 = math.isnan(float(data['bounding_box'][(6*i)+2]))
						y1 = math.isnan(float(data['bounding_box'][(6*i)+3]))

						if not x0 and not x1 and not y0 and not y1:
							temp_tuple = (float(data['bounding_box'][(6*i)+0]), float(data['bounding_box'][(6*i)+1]), float(data['bounding_box'][(6*i)+2]), float(data['bounding_box'][(6*i)+3]))
							box_coords.append(temp_tuple)
						
							area = (float(data['bounding_box'][(6*i)+2]) - float(data['bounding_box'][(6*i)+0])) * (float(data['bounding_box'][(6*i)+3]) - float(data['bounding_box'][(6*i)+1]))
							box_area.append(area)
						else:
							box_area = []
							box_coords = []
							continue
					else:
						box_area = []
						box_coords = []
						continue

				# tuple for every annotated image for Non-Maximum Suppression
				img_nms_tuple = (data['image_name'], data['class'], np.array(box_coords), box_area)
				final_imgs.append(img_nms_tuple)

	return final_imgs



def prepareInputImageArray(folder_name):
	"""

	Parameters
	-----------
	folder_name : The folder which contains the images 
	to be trained

	Returns
	--------
	An array with the image names

	Prepare the array for displaying images on the 
	index page. The images are pulled from a folder 
	and stored in an array for iterative indexing
	"""
	image_files = []
	folder_name =  "Annotate/static/media"
	for index, file in enumerate(os.listdir(folder_name)):
		file_ext = file.split('.')[-1]
		if file_ext.lower() not in ['jpg', 'jpeg', 'png', 'gif', 'bmp', 'tiff']:
			continue
		image_files.append(file)
	return image_files



def index(request):
	folder_name =  "Annotate/static/media"
	return render(request, 'index.html', {'imagesToAnnotate':prepareInputImageArray(folder_name)})


def non_max_suppression_slow(boxes, overlapThresh, areas=None):
	"""
	Non maximum suppression based on Malisiewicz et al. Based on
	implementation found here:
	http://www.pyimagesearch.com/2015/02/16/faster-non-maximum-suppression-python/

	Parameters
	----------
	boxes : numpy matrix [N x 4] -> (x0,y0,x1,y1)
	List of bounding boxes to perform NMS on.
	overlapThresh : number
	Overlap threshold parameter for NMS.
	areas : numpy vector [N]
	List of areas for each bounding box
	Returns
	-------
	bboxes : numpy matrix [N x 4]
	Final Bounding Boxes
	idx : numpy vector [N]
	Indexing array into original boxes matrix for selection.
	"""

	# if there are no boxes, return an empty list
	if len(boxes) == 0:
		return np.array([]), np.array([]), np.array([])

	if boxes.dtype.kind == "i":
		boxes = boxes.astype("float")

	# initialize the list of picked indexes
	pick = []

	# grab the coordinates of the bounding boxes
	x1 = boxes[:,0]
	y1 = boxes[:,1]
	x2 = boxes[:,2]
	y2 = boxes[:,3]

	# compute the area of the bounding boxes and sort the bounding
	# boxes areas of the bounding box
	area = (x2 - x1 + 1) * (y2 - y1 + 1)
	idxs = np.argsort(areas)

	# keep looping while some indexes still remain in the indexes
	# list
	while len(idxs) > 0:
		# grab the last index in the indexes list, add the index
		# value to the list of picked indexes, then initialize
		# the suppression list (i.e. indexes that will be deleted)
		# using the last index
		last = len(idxs) - 1
		i = idxs[last]
		pick.append(i)

		# loop over all indexes in the indexes list
		xx1 = np.maximum(x1[i], x1[idxs[:last]])
		yy1 = np.maximum(y1[i], y1[idxs[:last]])
		xx2 = np.minimum(x2[i], x2[idxs[:last]])
		yy2 = np.minimum(y2[i], y2[idxs[:last]])
 
		# compute the width and height of the bounding box
		w = np.maximum(0, xx2 - xx1 + 1)
		h = np.maximum(0, yy2 - yy1 + 1)
 
		# compute the ratio of overlap
		overlap = (w * h) / area[idxs[:last]]
 
		# delete all indexes from the index list that have
		idxs = np.delete(idxs, np.concatenate(([last],
			np.where(overlap > overlapThresh)[0])))

	# return only the bounding boxes that were picked
	return boxes[pick].astype("int"), pick



def viewAnnotImgs(request):
# lists all the training images without Non-Maximum Suppression	

	trainingImgs = []
	filename = "Annotate/static/trainingdata/training_set.csv"

	final_imgs = []

	image_paths = []
	image_boundingbox = []

	file_exists = os.path.isfile(filename)
	if file_exists:
		with open(filename, 'r') as csv_file:
			# skip the headers
			next(csv_file)
			
			# create a list of dictionaries for each line
			training_img_rect_dict = {}
			training_img_class_dict = {}
			for line in csv_file:
				line_split = line.split(",")

				img_name = line_split[0]
				
				# parse the coordinates for the bounding box and 
				# store the bounding box coorindate array in dictionary
				box = []
				if line_split[1] != "[]":

					# the raw data can contain N copies for each image 
					# Combine the all bounding box coordinates onto one
					# image
					if img_name in training_img_rect_dict:
						# if the image_name is present in dict; append the
						# box coordinates from other images into on
						bounding_rect = training_img_rect_dict[img_name]
						bounding_rect.append(line_split[1][2:])
						for i in range(2,len(line_split)-2):
							bounding_rect.append(line_split[i])
						bounding_rect.append(line_split[i+1][:-2])
						training_img_rect_dict[img_name] = bounding_rect
					else:
						temp_box = []
						temp_box.append(line_split[1][2:])
						for i in range(2,len(line_split)-2):
							temp_box.append(line_split[i])
						temp_box.append(line_split[i+1][:-2])
						training_img_rect_dict[img_name] = temp_box
						training_img_class_dict[img_name] = line_split[len(line_split)-1][:-1]
				else:	
					# when the image is labeled as "Not skull"; initialize
					# empty array
					training_img_rect_dict[img_name] = []
					training_img_class_dict[img_name] = line_split[len(line_split)-1][:-1]

			for img_file in training_img_rect_dict:
				data = {}
				data['image_name'] = img_file
				data['bounding_box'] = training_img_rect_dict[img_file]
				data['class'] = training_img_class_dict[img_file]

				trainingImgs.append(data)
	return render(request, 'view.html', {'trainingMap':trainingImgs})



def viewAnnotImgsNMS(request):
	# lists all the training images with Non-Maximum Suppression
	trainingImgs = []
	filename = "Annotate/static/trainingdata/training_set.csv"

	final_imgs = []

	image_paths = []
	image_boundingbox = []
	img_class = "0"

	final_imgs = prepareArrayNMS(filename)

	for (imagefile_name, imagefile_class, imagefile_rects, areas) in final_imgs:

		if imagefile_rects.size > 0:
			final_bboxes, idx = non_max_suppression_slow(imagefile_rects, 0.3, areas=areas)
		else:
			final_bboxes = []
		
		d = {}
		d['image_name'] = imagefile_name

		box = []
		# appending the new coordinates as returned by Non Maximum 
		# Suppression to the coordinates array for an image.
		# the width and height is also calculated
		x0 = x1 = y0 = y1 = 0.0
		for i in range(0, len(final_bboxes)):
			for j in range(0, len(final_bboxes[i])):
			 	box.append(final_bboxes[i][j])
				x0 = final_bboxes[i][0]
				y0 = final_bboxes[i][1]
				x1 = final_bboxes[i][2]
				y1 = final_bboxes[i][3]
			box_width = x1 - x0
			box_height = y1 - y0
			box.append(box_width)
			box.append(box_height)


		d['bounding_box'] = box

		d['class'] = imagefile_class
		trainingImgs.append(d)
	
	return render(request, 'view.html', {'trainingMap':trainingImgs})




def downloadAll(request):
	# downloads all the images in the folder used for training

	zip_subdir = "all_images_dataset"
	zip_filename = "%s.zip" % zip_subdir
	
	s = StringIO.StringIO()
	zf = zipfile.ZipFile(s, "w")
	folder_name = "Annotate/static/media"

	# only append if the file is an image file
	for index, file in enumerate(os.listdir(folder_name)):
		file_ext = file.split('.')[-1]
		if file_ext.lower() not in ['jpg', 'jpeg', 'png', 'gif', 'bmp', 'tiff']:
			continue
		zip_path = os.path.join(zip_subdir, file)
		full_path = "Annotate/static/media/"+file
		zf.write(full_path, zip_path)
			
	# Must close zip for all contents to be written
	zf.close()

    # Grab ZIP file from in-memory
	resp = HttpResponse(s.getvalue(), content_type = "application/x-zip-compressed")
  
	resp['Content-Disposition'] = 'attachment; filename=%s' % zip_filename

	return resp


# download the csv file which contains the metadata for 
# each annotated image
def downloadFile(request):
	zip_subdir = "training_datafile"
	zip_filename = "%s.zip" % zip_subdir
	s = StringIO.StringIO()
	zf = zipfile.ZipFile(s, "w")

    	#CSV File
	csvfilename = "Annotate/static/trainingdata/training_set.csv"
	file_exists = os.path.isfile(csvfilename)
	if file_exists:
		zip_path = os.path.join(zip_subdir, "training_set.csv")
		zf.write("Annotate/static/trainingdata/training_set.csv", zip_path)

   # Must close zip for all contents to be written
	zf.close()

    # Grab ZIP file from in-memory
	resp = HttpResponse(s.getvalue(), content_type = "application/x-zip-compressed")
  
	resp['Content-Disposition'] = 'attachment; filename=%s' % zip_filename

	return resp


def downloadImgs(request):
	"""
	 Download the annotated images with the bounding box.
	"""
	zip_subdir = "training_images"
	zip_filename = "%s.zip" % zip_subdir
	
	img_files_arr = []
	bounding_box_arr = []
	img_class_arr = []
	s = StringIO.StringIO()
	zf = zipfile.ZipFile(s, "w")

	training_img_rect_dict = {}
	training_img_class_dict = {}

	filename = "Annotate/static/trainingdata/training_set.csv"

	# check if .csv file exists
	file_exists = os.path.isfile(filename)
	if file_exists:
		with open(filename, 'r') as csv_file:
			# skip the headers
			next(csv_file)
			trainingImgs = []

			# create a list of dictionaries for each line
			for line in csv_file:
				line_split = line.split(",")

				img_name = line_split[0]
		
				# parse the coordinates for the bounding box and 
				# store the bounding box coorindate array in dictionary
				box = []
				if line_split[1] != "[]":

					if img_name in training_img_rect_dict:
						bounding_rect = training_img_rect_dict[img_name]
						bounding_rect.append(line_split[1][2:])
						for i in range(2,len(line_split)-2):
							bounding_rect.append(line_split[i])
						bounding_rect.append(line_split[i+1][:-2])
						training_img_rect_dict[img_name] = bounding_rect
					else:
						temp_box = []
						temp_box.append(line_split[1][2:])

						for i in range(2,len(line_split)-2):
							temp_box.append(line_split[i])
						temp_box.append(line_split[i+1][:-2])
						training_img_rect_dict[img_name] = temp_box
						training_img_class_dict[img_name] = line_split[len(line_split)-1][:-1]
				else:	
					training_img_rect_dict[img_name] = []
					training_img_class_dict[img_name] = line_split[len(line_split)-1][:-1]

			for img_file in training_img_rect_dict:
				data = {}
				data['image_name'] = img_file
				data['bounding_box'] = training_img_rect_dict[img_file]
				data['class'] = training_img_class_dict[img_file]

				im = Image.open("Annotate/static/media/"+data['image_name'])

				# draw bounding boxes for each image by first calculating
				# the number of boxes for each image and then indexing the 
				# array for the coordindates accordingly
				numRectangles = len(data['bounding_box'])/6

				# prepare the image for drawing and then draw the 
				# bounding boxes
				draw = ImageDraw.Draw(im)
				for i in range(0,numRectangles):
					draw.rectangle([(float(data['bounding_box'][(6*i)+0]), float(data['bounding_box'][(6*i)+1])), (float(data['bounding_box'][(6*i)+2]), float(data['bounding_box'][(6*i)+3]))], fill=None, outline='red')
				del draw
				
				# Since ZipModule cannot handle duplicate file names;
				# rename the duplicate files by appending the copy number
				# to the image 

				# save the image with the bounding box; for zipping purposes
				im.save(data['image_name'])
				
				# getting the image ready to be added to the zip file
				
				# add zip path to the annotated image; new path after zip
				zip_path = os.path.join(zip_subdir, data['image_name'])
				
				# Add file, at correct path
				full_path = data['image_name']

				zf.write(full_path, zip_path)

				#remove the annotated image
				os.remove(data['image_name'])

	# create a new csv file with naming according to the annotated images.
	# this csv file contains metadata related to each annotated image
	csv_filename = "Annotate/static/trainingdata/training_data.csv"
	
	csv_file_exists = os.path.isfile(csv_filename)

	# create a new file everytime we download the files
	# this is to avoid any data inconsistency issues
	if csv_file_exists:
		os.remove(csv_filename)

	# open the new csv file
	with open(csv_filename,'a') as filedata:
		headers = ["imagename","coordinates","class"]
		writer = csv.DictWriter(filedata, delimiter=',', lineterminator='\n',fieldnames=headers)
		writer.writeheader()
		
		#for i in range(0,len(img_files_arr)):
		for img_file in training_img_rect_dict:
			data = {}
			data['image_name'] = img_file
			data['bounding_box'] = training_img_rect_dict[img_file]
			data['class'] = training_img_class_dict[img_file]

			img_rects = []
			num_rects = len(data['bounding_box'])/6
			for j in range(0, num_rects):
				arr = [data['bounding_box'][(6*j)+0], data['bounding_box'][(6*j)+1], data['bounding_box'][(6*j)+2], data['bounding_box'][(6*j)+3], data['bounding_box'][(6*j)+4], data['bounding_box'][(6*j)+5]]
				img_rects.append(arr)
			writer.writerow({"imagename":data['image_name'], "coordinates":img_rects, "class":data['class']})

	zip_path = os.path.join(zip_subdir, "training_set.csv")
	# add the newly created .csv file to the zip archive
	zf.write(csv_filename, zip_path)
	# Must close zip for all contents to be written
	zf.close()
	
    # Grab ZIP file from in-memory
	resp = HttpResponse(s.getvalue(), content_type = "application/x-zip-compressed")
  
	resp['Content-Disposition'] = 'attachment; filename=%s' % zip_filename

	return resp

def downloadImgsNMS(request):

	"""
	 Download the annotated images with the bounding box
	 with Non-Maximum Suppression
	"""
	zip_subdir = "training_images_nms"
	zip_filename = "%s.zip" % zip_subdir

	img_files_arr = []
	img_class_arr = []
	img_bounding_box = []

	s = StringIO.StringIO()
	zf = zipfile.ZipFile(s, "w")

	filename = "Annotate/static/trainingdata/training_set.csv"

	final_imgs = prepareArrayNMS(filename)
	
	
	for (imagefile_name, imagefile_class, imagefile_rects, areas) in final_imgs:

		if imagefile_rects.size > 0:
			final_bboxes, idx = non_max_suppression_slow(imagefile_rects, 0.3, areas=areas)
		else:
			final_bboxes = []

		box = []
		for i in range(0, len(final_bboxes)):
			
			for j in range(0, len(final_bboxes[i])):
			 	box.append(final_bboxes[i][j])
			box_width = box[2] - box[0]
			box_height = box[3] - box[1]
			box.append(box_width)
			box.append(box_height)

		img_file = imagefile_name.split(".")[0]
		img_ext = imagefile_name.split(".")[1]
		
		
		im = Image.open("Annotate/static/media/"+imagefile_name)

		
		img_files_arr.append(imagefile_name)

		img_class_arr.append(imagefile_class)

		img_bounding_box.append(box)

		# prepare the image for drawing and then draw the 
		# bounding boxes

		num_rects = len(box)/6
		draw = ImageDraw.Draw(im)

		for i in range(0,num_rects):
			draw.rectangle([(float(box[(6*i)+0]), float(box[(6*i)+1])), (float(box[(6*i)+2]), float(box[(6*i)+3]))], fill=None, outline='red')
		del draw
		

		# save the image with the bounding box; for zipping purposes
		im.save(imagefile_name)
		
		# getting the image ready to be added to the zip file
		
		# add zip path to the annotated image; new path after zip
		zip_path = os.path.join(zip_subdir, imagefile_name)
		
		# Add file, at correct path
		full_path = imagefile_name

		zf.write(full_path, zip_path)

		#remove the annotated image
		os.remove(imagefile_name)

		# create a new csv file with naming according to the annotated images.
		# this csv file contains metadata related to each annotated image
	csv_filename = "Annotate/static/trainingdata/training_data_nms.csv"
		
	csv_file_exists = os.path.isfile(csv_filename)

		# create a new file everytime we download the files
		# this is to avoid any inconsistency issues
	if csv_file_exists:
		os.remove(csv_filename)

		# open the new csv file
	with open(csv_filename,'a') as filedata:
		headers = ["imagename","coordinates","class"]
		writer = csv.DictWriter(filedata, delimiter=',', lineterminator='\n',fieldnames=headers)
		writer.writeheader()
		
		for i in range(0,len(img_files_arr)):
			img_rects = []
			num_rects = len(img_bounding_box[i])/6
			for j in range(0, num_rects):
				arr = [img_bounding_box[i][(6*j)+0], img_bounding_box[i][(6*j)+1], img_bounding_box[i][(6*j)+2], img_bounding_box[i][(6*j)+3], img_bounding_box[i][(6*j)+4], img_bounding_box[i][(6*j)+5]]
				img_rects.append(arr)
			writer.writerow({"imagename":img_files_arr[i], "coordinates":img_rects, "class":img_class_arr[i]})

	zip_path = os.path.join(zip_subdir, "training_set.csv")

	# add the newly created .csv file to the zip archive
	zf.write(csv_filename, zip_path)
	# Must close zip for all contents to be written
	zf.close()
	
    # Grab ZIP file from in-memory
	resp = HttpResponse(s.getvalue(), content_type = "application/x-zip-compressed")
  
	resp['Content-Disposition'] = 'attachment; filename=%s' % zip_filename

	return resp


def replace_line(file_name, line_num, text):
    lines = open(file_name, 'r').readlines()
    lines[line_num] = text
    out = open(file_name, 'w')
    out.writelines(lines)
    out.close()



@csrf_exempt
def add(request):
# save the annotated image metadata to a csv file
	folder_name =  "Annotate/static/media"
	image_index = request.POST.get('image_index');

	if image_index is None:
		image_index = "0"

	try:
		print image_index
		image_index = str(int(image_index)+1)
	except ValueError:
		temp_index = image_index[:-1]
		image_index = str(int(temp_index)+1)

	# only get the file name; 
	image_name = request.POST.get('image_name')

	
	if image_name is None:
		image_name = ""
	imgNameSplit = image_name.split("/")
	
	if all(v for v in imgNameSplit):
		image_name = imgNameSplit[1]

	# get image label
	image_isSkull = request.POST.get('isskull')
	
	# get the coordinates array
	# format: array = [x0,y0,x1,y1,width,height]
	image_rect = request.POST.get('rect_cords')

		
	# here we store the meta data related to the annotated image
	# format : imagename, coordinates array, class

	# create file if it does not exist. if exists; append data
	filename = "Annotate/static/trainingdata/training_set.csv"
	file_exists = os.path.isfile(filename)

	with open(filename,'a') as filedata:     
		#headers for the csv file
		headers = ["imagename","coordinates","class"]
		writer = csv.DictWriter(filedata, delimiter=',', lineterminator='\n',fieldnames=headers)

		# add header if the file is newly created
		if not file_exists:
			writer.writeheader()

		# check the class to which the image belongs
		# class 0 if the image does not have skull; 1 if image has a skull
		if image_isSkull == "Skull":
			imgClass = "1"
		else:
			imgClass = "0"

		#append image data to file
		if image_name!= "":
			writer.writerow({"imagename":image_name, "coordinates":'['+image_rect+']', "class":imgClass})
	return render(request, 'index.html', {'currentIndex':image_index, 'imagesToAnnotate':prepareInputImageArray(folder_name)})



