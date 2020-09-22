# cmpimg
Compare a set of images and report a structural similarity index (ssim) matrix, in CSV and Mega-compatible formats.

# Rationale
Given a set of images it computes the corresponding pairwise structural similarity index values, as implemented in the `structural_similarity` function of *skimage*. For more help about this index check [skimage documentation](https://scikit-image.org/docs/stable/auto_examples/transform/plot_ssim.html).

# Usage
```
cmpimg [-h] [-o OUTPUT] [-v] image [image ...]

positional arguments:
  image                 Any image format supported by skimage.

optional arguments:
  -h, --help            show this help message and exit
  -o OUTPUT, --output OUTPUT
                        output files base name [default: ssim_matrix].
  -v, --version         Show program's version number and exit.
```

# Installation
This is a Python script, so, you can just run the *cmpimg.py* file or put a symbolic link in any directory of your `PATH`.

# Dependencies
The following python3 packages are required:
* argparse
* os
* sys
* numpy
* skimage
* natsort

