#!/usr/bin/env python3
##
## Compare a set of images and report a structural similarity index (SSIM) matrix, in CSV and Mega-compatible formats.
## As for dendograms smaller values mean closer objects, the report in the MEG file is abs(1-SSIM).
##
## Amaury Pupo Merino
## amaury.pupo@gmail.com
##
## This script is released under GPL v3.
##

## Importing modules
import argparse
import os
import sys
import numpy as np
from skimage import io, img_as_float
from skimage.transform import resize
from skimage.metrics import structural_similarity
from natsort import natsorted

## Functions
"""
    rootname

Get root file name, excluding rest of the path and extensions.
"""
def rootname(filename):
    rootname, ext = os.path.splitext(os.path.basename(filename))
    if ext.lower() == ".gz":
        rootname = os.path.splitext(rootname)[0]

    return rootname

def write_csv(filename, unique_files, mat):
	print("Writing file {}".format(filename))
	with open(filename, "w") as output_file:
		output_file.write("structures")

		image_names = [rootname(f) for f in unique_files]

		for image_name in image_names:
			output_file.write(",{}".format(image_name))

		output_file.write("\n")

		for i in range(mat.shape[0]):
			for j in range(mat.shape[1]):
				if j == 0:
					output_file.write("{}".format(image_names[i]))

				if i > j:
					output_file.write(",{:f}".format(mat[i,j]))

				else:
					output_file.write(",")

			output_file.write("\n")

def write_meg(filename, unique_files, mat):
	print("Writing file {}".format(filename))
	with open(filename, "w") as output_file:
		output_file.write("#mega\n")
		output_file.write("!Title: SSIM matrix;\n")
		output_file.write("!Format DataType=Distance DataFormat=LowerLeft NTaxa={:d};\n".format(len(unique_files)))
		output_file.write("!Description\n")
		output_file.write("abs(1-SSIM) between images, as calculated by cmpimg\n;\n\n")

		image_names = [rootname(f) for f in unique_files]

		for (i, image_name) in enumerate(image_names):
			output_file.write("[{:d}] #{}\n".format(i+1, image_name))

		output_file.write("\n[     ")

		for i in range(len(image_names)):
			output_file.write("{:9d}".format(i+1))

		output_file.write("  ]\n")

		for i in range(mat.shape[0]):
			for j in range(mat.shape[1]):
				if j == 0:
					output_file.write("[{:2d}]   ".format(i+1))

				if i > j:
					output_file.write("{:9.3g}".format(abs(1 - mat[i,j])))
				else:
					output_file.write(" " * 9)

			output_file.write("\n")

def compute_ssim(image1, image2):
	image1 = img_as_float(image1)
	image2 = img_as_float(image2)
	ssim_value = -10.0
	
	if image1.shape[2] != image2.shape[2]:
		sys.stderr.write("ERROR: Images need to have the same number of channels to be compared, ie. you can not compare RGB vs grayscale or RGBA vs RGB, etc. Please convert the images accordantly.\n")
		exit(1)
	
	if image1.shape[:2] != image2.shape[:2]:
		tmp_ssim1 = structural_similarity(image1, resize(image2, image1.shape[:2]), multichannel=True)
		tmp_ssim2 = structural_similarity(resize(image1, image2.shape[:2]), image2, multichannel=True)
		ssim_value = (tmp_ssim1 + tmp_ssim2)/2.0

	else:
		ssim_value = structural_similarity(image1, image2, multichannel=True)

	return ssim_value


## Main
def main():
	"""Main function.
	"""
	parser=argparse.ArgumentParser(description="Compare a set of images and report a structural similarity index (SSIM) matrix, in CSV and Mega-compatible formats.")
	parser.add_argument('image', nargs='+', help='Any image format supported by skimage.')
	parser.add_argument('-o', '--output', default='ssim_matrix', help='output files base name [default: %(default)s].')
	parser.add_argument('-v', '--version', action='version', version='1.1', help="Show program's version number and exit.")

	args=parser.parse_args()

	unique_files = natsorted(set(args.image))

	n = len(unique_files)

	if n < 2:
	    parser.error("ERROR: At least two unique images are required.")

	ssim_mat = np.zeros((n, n)) - 10.0 # SSIM values range from -1.0 to 1.0.
	
	for c in range(n-1):
		print("{} vs ".format(unique_files[c]))

		try:
			image1 = io.imread(unique_files[c])

		except:
			sys.stderr.write("WARNING: Can not load image {}. Ignoring it. Corresponding SSIM values will be set to -10.0\n".format(unique_files[c]))
			continue

		for r in range(c + 1, n):

			try:
				image2 = io.imread(unique_files[r])
				print("\t{}".format(unique_files[r]), end="... ")

			except:
				sys.stderr.write("WARNING: Can not load image {}. Ignoring it. Corresponding SSIM values will be set to -10.0\n".format(unique_files[r]))
				continue

			ssim_mat[r, c] = compute_ssim(image1, image2)

			print("{:.3f}".format(ssim_mat[r, c]))

	print()

	write_csv(args.output + ".csv", unique_files, ssim_mat)
	write_meg(args.output + ".meg", unique_files, ssim_mat)

## Running the script
if __name__ == "__main__":
        main()
