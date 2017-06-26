# Train machine learning model

## Description

Once we have the training data and the validation data, use TensorBox to train a machine learning model. A trained model has
already been provided with the name of (write the name)_

## Instructions to run
The following pre-requisites need to be satisified for the project to run:
* Python 2.7
* TensorFlow
* OpenCV
* pip
* pkg-config
* virtualenv
* Pillow 4.1.0

In order to install and run TensorBox, follow the instructions on this page [TensorBox setup](https://github.com/baljit92/TensorBox)

Once TensorBox is setup; **modify** the corresponding fields in `TensorBox/hypes/overfeat_rezoom.json`:

```
	"train_idl": "<path_to_training_json_file>",
	"test_idl": "<path_to_validation_json_file>"
```
**Note: The paths should be absolute paths**

### Evaluation
To evaluate new images, use the evaluation file provided by Tensor box as follows:
`python evaluate.py --weights output/overfeat_rezoom_2017_01_17_15.20/<name of model> --test_boxes <path_to_testing_json_file>`

### Scripts
Two scripts have ben provided:
1) `convert.py` which converts the .csv file downloaded from the web app to JSON format accepted by TensorBox
2) `image-augment.py` used to generate augmentated versions of a single training/annotated image. Over here; we first
draw bounding box in the area of interest in an image and then use this script to generate an augmented version of the 
image. Of course, it is made sure that the image is not rotated to avoid any rectangle coordinate issues. One requirement,
however, to run this is that it uses `Pillow 2.1.0` instead of the latest version.
