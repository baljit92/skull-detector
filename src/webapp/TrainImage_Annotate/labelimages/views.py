from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
import re
from labelimages.models import *
import csv
import os
import zipfile
import StringIO
from PIL import Image, ImageDraw
import numpy as np
import fnmatch

# prepare the array for displaying images on the 
# index page. The images are pulled from a folder 
# and stored in an array for iterative indexing
def prepareInputImageArray():
	imageFiles = []
	foldername = "labelimages/static/media"

	files = os.listdir(foldername)

	for file in files:
		# check if the file is an image
		if fnmatch.fnmatch(file, '*.jpg') or fnmatch.fnmatch(file, '*.png') or fnmatch.fnmatch(file, '*.jpeg'):
			imageFiles.append(file)
	return imageFiles


def index(request):
	return render(request, 'index.html', {'imagesToAnnotate':prepareInputImageArray()})

# Cite: http://www.pyimagesearch.com/2015/02/16/faster-non-maximum-suppression-python/
# Felzenszwalb et al.
def non_max_suppression_slow(boxes, overlapThresh):
	# if there are no boxes, return an empty list
	if len(boxes) == 0:
		return []

	# initialize the list of picked indexes
	pick = []

	# grab the coordinates of the bounding boxes
	x1 = boxes[:,0]
	y1 = boxes[:,1]
	x2 = boxes[:,2]
	y2 = boxes[:,3]

	# compute the area of the bounding boxes and sort the bounding
	# boxes by the bottom-right y-coordinate of the bounding box
	area = (x2 - x1 + 1) * (y2 - y1 + 1)
	idxs = np.argsort(y2)

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
		suppress = [last]

		# loop over all indexes in the indexes list
		for pos in xrange(0, last):
			# grab the current index
			j = idxs[pos]

			# find the largest (x, y) coordinates for the start of
			# the bounding box and the smallest (x, y) coordinates
			# for the end of the bounding box
			xx1 = max(x1[i], x1[j])
			yy1 = max(y1[i], y1[j])
			xx2 = min(x2[i], x2[j])
			yy2 = min(y2[i], y2[j])

			# compute the width and height of the bounding box
			w = max(0, xx2 - xx1 + 1)
			h = max(0, yy2 - yy1 + 1)

			# compute the ratio of overlap between the computed
			# bounding box and the bounding box in the area list
			overlap = float(w * h) / area[j]

			# if there is sufficient overlap, suppress the
			# current bounding box
			if overlap > overlapThresh:
				suppress.append(pos)

		# delete all indexes from the index list that are in the
		# suppression list
		idxs = np.delete(idxs, suppress)

	# return only the bounding boxes that were picked
	return boxes[pick]



# lists all the annotated images
def viewImg(request):
	trainingFile = []
	dlist = []
	filename = "labelimages/static/trainingdata/training_set.csv"
	# check if .csv file exists
	file_exists = os.path.isfile(filename)
	if file_exists:
		with open(filename, 'r') as csv_file:
			# skip the headers
			next(csv_file)
			

			# create a list of dictionaries for each line
			for line in csv_file:
				d = {}
				line_split = line.split(",")

				img_name = line_split[0]
				d['image_name'] = img_name

				# parse the coordinates for the bounding box and 
				# store the bounding box coorindate array in dictionary
				box = []
				if line_split[1] != "[]":

					box.append(line_split[1][2:])

					for i in range(2,len(line_split)-2):
						box.append(line_split[i])
					box.append(line_split[i+1][:-2])
					d['bounding_box'] = box

				# class of each image
				d['class'] = line_split[len(line_split)-1][:-1]
				
				# append dictionary to the final array
				dlist.append(d)
	return render(request, 'view.html', {'trainingMap':dlist})



# downloads all the annotated images in a zip file
def downloadAll(request):
	zip_subdir = "training_images"
	zip_filename = "%s.zip" % zip_subdir
	
	imgFiles = []
	s = StringIO.StringIO()
	zf = zipfile.ZipFile(s, "w")
	foldername = "labelimages/static/media"

	files = os.listdir(foldername)

	for file in files:
		# check if the file is an image
		if fnmatch.fnmatch(file, '*.jpg') or fnmatch.fnmatch(file, '*.png') or fnmatch.fnmatch(file, '*.jpeg'):

			zip_path = os.path.join(zip_subdir, file)
				
				# Add file, at correct path
			full_path = "labelimages/static/media/"+file
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
	csvfilename = "labelimages/static/trainingdata/training_set.csv"
	file_exists = os.path.isfile(csvfilename)
	if file_exists:
		zip_path = os.path.join(zip_subdir, "training_set.csv")
		zf.write("labelimages/static/trainingdata/training_set.csv", zip_path)

   # Must close zip for all contents to be written
	zf.close()

    # Grab ZIP file from in-memory
	resp = HttpResponse(s.getvalue(), content_type = "application/x-zip-compressed")
  
	resp['Content-Disposition'] = 'attachment; filename=%s' % zip_filename

	return resp

# download the annotated images with the bounding box.
# the .csv file which contains the metadata
# is also downloaded with the annotated images
# P.S. the .csv file contains images with the same
# name while the images are labeled with copy 
# numbers since ZipFile module does not allow
# duplicate files.

def downloadImg(request):
	zip_subdir = "training_annot_images"
	zip_filename = "%s.zip" % zip_subdir
	
	imgFiles = []
	boundingBox = []
	imgClass = []
	s = StringIO.StringIO()
	zf = zipfile.ZipFile(s, "w")
	filename = "labelimages/static/trainingdata/training_set.csv"
	# check if .csv file exists
	file_exists = os.path.isfile(filename)
	if file_exists:
		with open(filename, 'r') as csv_file:
			# skip the headers
			next(csv_file)
			dlist = []
			dup_dict = {}
			# create a list of dictionaries for each line
			for line in csv_file:
				d = {}
				line_split = line.split(",")

				img_name = line_split[0]

				img_file = img_name.split(".")[0]
				img_ext = img_name.split(".")[1]

				count = 0
				if img_name in dup_dict:
					count = dup_dict[img_name]
					dup_dict[img_name] += 1
				else:
					dup_dict[img_name] = 1

				# add coordinates for the annotated image in 
				# an array named 'box'. This is to draw the
				# bounding box(es) on the image 
				box = []
				box.append(line_split[1][2:])
				for i in range(2,len(line_split)-2):
					box.append(line_split[i])
				box.append(line_split[i+1][:-2])

				boundingBox.append(box);
				if count>0:
					imgFiles.append(img_file+"_"+str(count)+"."+img_ext)
				else:
					imgFiles.append(img_name)

				imgClass.append(line_split[-1][0])

				im = Image.open("labelimages/static/media/"+img_name)

				# draw bounding boxes for each image by first calculating
				# the number of boxes for each image and then indexing the 
				# array for the coordindates accordingly
				numRectangles = len(box)/6

				# prepare the image for drawing and then draw the 
				# bounding boxes
				draw = ImageDraw.Draw(im)
				for i in range(0,numRectangles):
					draw.rectangle([(float(box[(6*i)+0]), float(box[(6*i)+1])), (float(box[(6*i)+2]), float(box[(6*i)+3]))], fill=None, outline='red')
				
				del draw
				
				# Since ZipModule cannot handle duplicate file names;
				# rename the duplicate files by appending the copy number
				# to the image 

				# save the annotated; for zipping purposes
				if count>0:
					im.save(img_file+"_"+str(count)+"."+img_ext)
				else:
					im.save(img_name)
				
				# getting the image ready to be added to the zip file
				
				# add zip path to the annotated image; new path after zip
				if count>0:
					zip_path = os.path.join(zip_subdir, img_file+"_"+str(count)+"."+img_ext)
				else:
					zip_path = os.path.join(zip_subdir, img_name)
				
				# Add file, at correct path
				if count>0:
					full_path = img_file+"_"+str(count)+"."+img_ext
				else:
					full_path = img_name

				zf.write(full_path, zip_path)

				#remove the annotated
				if count>0:
					os.remove(img_file+"_"+str(count)+"."+img_ext)
				else:
					os.remove(img_name)

	# create a new csv file with naming according to the annotated images.
	# this csv file contains metadata related to each annotated image
	csv_filename = "labelimages/static/trainingdata/final_training_set.csv"
	
	csv_file_exists = os.path.isfile(csv_filename)

	if csv_file_exists:
		os.remove(csv_filename)

	with open(csv_filename,'a') as filedata:
		dataToWrite = ""
		headers = ["imagename","coordinates","class"]
		writer = csv.DictWriter(filedata, delimiter=',', lineterminator='\n',fieldnames=headers)
		writer.writeheader()
		
		for i in range(0,len(imgFiles)):
			writer.writerow({"imagename":imgFiles[i], "coordinates":boundingBox[i], "class":imgClass[i]})

	zip_path = os.path.join(zip_subdir, "final_training_set.csv")
		
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


# save the annotated image meta data to a csv file
@csrf_exempt
def add(request):
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
	filename = "labelimages/static/trainingdata/training_set.csv"
	file_exists = os.path.isfile(filename)

	with open(filename,'a') as filedata:     

	
		dataToWrite = ""

		#headers for the csv file
		headers = ["imagename","coordinates","class"]
		writer = csv.DictWriter(filedata, delimiter=',', lineterminator='\n',fieldnames=headers)

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
	return render(request, 'index.html', {'currentIndex':image_index, 'imagesToAnnotate':prepareInputImageArray()})
	
