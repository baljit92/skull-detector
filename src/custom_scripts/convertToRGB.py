from PIL import Image
import csv
import os
import sys, getopt


def main(argv):
	
	if len(argv) < 1:
		print 'python convertToRGB.py <image_file_path>'
		sys.exit(2)
	else:
		try:
			file_path, file_name = os.path.split(argv[0])
			im = Image.open(argv[0])
			rgb_im = im.convert('RGB')
			rgb_im.save(file_path+"/"+file_name.split(".")[0]+".jpeg")
		except IOError:
			print "Please enter a valid image"
			sys.exit(2)

if __name__ == "__main__":
	main(sys.argv[1:])