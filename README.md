# Skull detection in images

# Web app to annotate/label images

## Description

The web app let's the user annotate images by drawing a red color bounding box around the skulls in the image. The user can label the image with *Skull* or *Not Skull* class.

Once the user clicks the Save button; the metadata of the annotated image such as `(image_name, [[x0, y0, x1, y1, width, height]], class)` is stored in a csv file. 

The csv file gets downloaded when the user downloads the training images.

Non-Maximum Suppression(NSM) support has been added to combine multiple bounding boxes for an image. This helps in suppressing all the image information and displaing only the essential bounding boxes.

No annotated images are stored in any directory. Whenever the user wants to view/download the training images; we make use of the coordinates present in the .csv to draw the bounding box on the fly. Users can view/download the training images both with NSM and without NSM.

Non-Maximum Suppression support has been added to combine multiple bounding boxes for an image. This helps in suppressing all the image information and displaying
only the essential bounding boxes. 


## Instructions to run
The following pre-requisites need to be satisified for the project to run:
* Python 2.7
* Django 1.11.2
* pip

Following commands can be used to install Django on both macOs and Unix machines:
```
pip install Django==1.11.2
pip install Pillow
```

Once installed, follow the commands below:
```
cd src/webapp/TrainImage_Annotate/
python manage.py runserver
```

Go to the browser and type in `localhost:8000/draw`

The images used in the web app are fetched from `src/webapp/TrainImage_Annotate/Annotate/static/media`

## Scripts
Two scripts have ben provided in `src/custom_scripts` :
1) `convert_csv_to_json.py` which converts the .csv file downloaded from the web app to JSON format accepted by TensorBox
2) `image-augment.py` used to generate augmentated versions of a single training/annotated image. Over here; we first
draw bounding box in the area of interest in an image and then use this script to generate an augmented version of the 
image. Of course, it is made sure that the image is not rotated to avoid any rectangle coordinate issues. 

After downloading the dataset csv file from the webapp; use the script `convert_csv_to_json.py` so that it can be used with TensorBox.


# Machine Learning to detect human skulls

## Description

Once we have the training data and the validation data, use *TensorBox* to train a machine learning model. A trained model has
already been provided with the name of _save.ckpt-180000_

## Pre-requisites
The following pre-requisites need to be satisified for the project to run:
* Python 2.7
* TensorBox
* OpenCV
* pip
* pkg-config
* virtualenv
* Pillow 4.1.1

## Instructions to run
To setup TensorBox and evaluate the model, follow instructions below: 
	```
	git clone https://github.com/saifrahmed/HiringExercise_MLEngineer_Baljit92.git
	cd HiringExercise_MLEngineer_Baljit92
	chmod +x *.sh
	./install_tensorflow.sh
	source ./bin/activate
	./libraries_setup.sh
	./install_tensorbox.sh
	mv ./src/machine_learning/model/* ./tensorbox/data/
	mv ./src/machine_learning/data/* ./tensorbox/data/
	mv ./src/machine_learning/config/* ./tensorbox/hypes/
	cd tensorbox
	python evaluate.py --weights data/save.ckpt-180000 --test_boxes data/testing_set.json
	```

Below is a solution for a potential error that might come up during TensorBox installation. The commands should be executed inside the `virtualenv`:

2. *Error:* pkg-config python not found
   *Solution for macOS:* export PKG_CONFIG_PATH=/System/Library/Frameworks/Python.framework/Versions/2.7/lib/pkgconfig/; echo $(pkg-config --variable pc_path pkg-config)${PKG_CONFIG_PATH:+:}${PKG_CONFIG_PATH}

_Note: In order to use a custom training dataset, the files should be placed under the folder 'tensorbox/data' and modify the fields training and testing fields in `tensorbox/hypes/overfeat_rezoom.js`_

## The Dataset
The images used for this project have all been taken from the web. The images are of human skulls, non human skulls and various other objects such as people, cartoon characters, etc. After the completion of data collection, every image was passed through
the web app developed in the first phase.  The image metadata is then saved in a .csv file which will be used as a training the model. The metadata is in the format `(image_name, [x0,y0,x1,y1,w,h], image_class)`. 

For every image, we have created five augmented versions so as to provide variations in the dataset. 

* For every **positive image** (human skulls), the image was labeled with class 'Skull` and annotated by drawing bounding box(es) around every skull in an image.

* For every **negative image** (non human skulls plus other objects), the image was labeled with class 'Not Skull`. No bounding box was drawn.

## Results

Full testing output fromm the trainined model can be found under `results/`. In the images, the green boxes are the final predictions after merging, and red are all predictions after applying a threshold, but before merging.

#### Positive Images
Below are some positive images that were classified correctly. Most of the positively classified images, as below, are images that contain a standalone skull whereas some of them also contain noise in the background.

#### Negative Images
Most of the negative images were classified correctly, however as we can see below, some of the negative images that were positively classified contain backgorunds, skeletons, faces or facial-like features such as eyes. The trained model drew bounding boxes around random objects in addition to the human skull (if present). 

For the test dataset used, average accuracy was 90%

## Discussion

#### What foundation did you use for your project? What did you modify and what did you keep identical?
We used TensorBox for this project. TensorBox is a new framework that is used for training models to detect
objects in images. TensorBox is based on TensorFlow. 

The training image set in our case is very small. We were only able to collect and annotate around 1200 skull images due to time limitations. 

#### Describe your pipeline and pre-processing steps
The dataset consists of images of human skulls, animal skulls, cartoon faces, human faces, random objects and surroundings. 
Each of the image was labelled and annotated manually using the Annotate webapp. A positive image was annotated with bounding box(es) around areas of skull(s). 

* The training set consistsed of 1780 images with 1000 annotated images
* The validation set consisted of 440 images with 296 annotated images
* The testing set consisted of 78 images with 54 annotated images

We used a split of 80/20 training/validation to train the model.

##### Training pipeline
1. Capture the training and validation data files and give it to TensorBox as a training and testing file.
2. TensorBox runs with a gap of 50 steps. At each step, a batch of images are used to train the model.
3. The model training is completed after passing over the entire dataset 9 times.

##### Testing pipeline
1. Capture the testing data and evaluate it using the model trained by TensorBox. 
2. Once evaluated, TensorBox draws bounding boxes around the areas of interest in the testing image set and saves these images
in an `output/` folder. 
3. Use _Non Maximal Suppression_ to draw a combined bounding box around the areas of interest.


#### How long did your training and inference take?
The training and inference was performed on a _Late 2013 Macbook Pro_ configured with _Intel i5 2.4 GHz_ and _8 GB RAM_. Training the model with validation took upto 8 hours with 9 iterations over the entire data.

The time to train/image on average was ~2.3s and the time to train the entire model for every 50 steps was around ~115s with each complete pass over the entire dataset taking ~3100s.

#### If you had more time, how would you expand on this submission?
Couple of points:

1. Use ResNet. TensorBox contains ResNet that we could use for much deeper learning with more resources.
2. Training on a much larger data set that includes more negative class than positives and images with different resolutions.
3. Use more variations of image augmentations such as shearing, rotation to increase the accuracy.
4. For web app, use outlier detection to prevent spam in the training set
5. For web app, fix canvas drawing for large resolution images
