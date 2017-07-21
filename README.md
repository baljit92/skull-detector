# Skull detection in images

## Basic setup instructions
The following pre-requisites need to be satisified for the project to run:
* Python 2.7
* Django 1.11.2
* `pip`
* OpenCV
* pip
* Pillow 4.1.1
* TensorBox
* pkg-config
* virtualenv
* FreeType

For Ubuntu, the below files are required before installing the required modules:
```
sudo apt-get install libfreetype6-dev libxft-dev
sudo apt-get install python-tk
```
Following commands can be used to install pre-reqs using `pip`:
```
git clone https://github.com/baljit92/skull-detector.git
cd skull-detector
chmod +x *.sh
./setup_virtualenv.sh
source ./bin/activate
```



# Web app to annotate/label images

## Description

The web app let's the user annotate images by drawing a bounding box around the skulls in the image. The user can label the image with *Skull* or *Not Skull* class.

![Web app](/results/misc/webapp_shot.png)
Once the user clicks the Save button; the metadata of the annotated image is stored in a csv file. The metadata consists of

Field | Description
------| -----------
Image name | The name of the image file without the path
Bounding box | The coordinates of the box (top-left coordinates, bottom right coordinates, width, height)
Image class | The clss to which the image belongs

Non-Maximal Suppression support has been added to combine multiple bounding boxes for an image. This helps in suppressing all the image information and displaying
only the essential bounding boxes. This is helpful when multiple users draw bounding boxes on one image. 

Whenever the user wants to view/download the training images; we make use of the coordinates present in the .csv to draw the bounding box on the fly.
Users can view/download the training images both with and without NMS. The csv file gets downloaded when the user downloads the training images.
Once we have the dataset, we manually separate 20% of the data for validation and keep the 80% for training.


## Instructions to run

Once the requirements have been installed, follow the commands below to run the server:
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
image. All the transformations we use preserve the bounding box in the images.
3) `convertToRGB.py` which converts different image formats to `.jpeg`. This is important since Tensorbox cannot evaluate images with formats `.png` , `.bmp`. Whenever an image format is not `.jpeg` or `jpg`; use this wrapper to convert the image to appropriate format.

After downloading the dataset csv file from the webapp; use the script `convert_csv_to_json.py` so that it can be used with TensorBox.


# Machine Learning to detect human skulls

## Description

Once we have the training data and the validation data, use [TensorBox](https://github.com/TensorBox/TensorBox) to train a machine learning model. A trained model has
already been provided with the name of _save.ckpt-18000_


## Instructions to run

To setup TensorBox and evaluate the model, after completing the basic setup, follow instructions below(inside virtualenv) have been installed: 
	
	./libraries_setup.sh
	./install_tensorbox.sh
	mv ./src/machine_learning/model/* ./tensorbox/data/
	mv ./src/machine_learning/data/* ./tensorbox/data/
	mv ./src/machine_learning/config/* ./tensorbox/hypes/
	cd tensorbox
	python evaluate.py --weights data/save.ckpt-18000 --test_boxes data/testing_set.json

The evaluated image results are saved under `data/images_testing_set_18000`. 


To manually evaluate a custom image by uploading:
	
	mv web_upload_eval.py ./tensorbox

After moving the above file, go to the browser and type in `localhost:8000/draw/modelTest` 

To use a custom testing dataset, add the image files to `data/images` and replace the testing_set.json with the custom test dataset. The custom dataset should have image_path field as `/images/<image_name>` and the rects field will contain the true bounding box coordinates.

Below is a solution for a potential error that might come up during TensorBox installation. The commands should be executed inside the `virtualenv`:

1. **Error:** pkg-config python not found
   
   **Solution for macOS:** export PKG_CONFIG_PATH=/System/Library/Frameworks/Python.framework/Versions/2.7/lib/pkgconfig/; echo $(pkg-config --variable pc_path pkg-config)${PKG_CONFIG_PATH:+:}${PKG_CONFIG_PATH}

_Note: In order to use a custom training dataset, the training and validation files should be placed under 'tensorbox/data' and modify the fields training and testing fields in `tensorbox/hypes/overfeat_rezoom.js`_

## The Dataset
The images used for this project have all been taken from the web. The images are of human skulls, non human skulls and various other objects such as people, cartoon characters, etc. After the completion of data collection, every image was passed through
the web app developed in the first phase.  The image metadata is then saved in a .csv file which will be used as a training the model. We also used a script to generate 4-5 augmentated versions of the images so s to provide variations in the dataset.

* For every **positive image** (human skulls), the image was labeled with class 'Skull` and annotated by drawing bounding box(es) around every skull in an image.

* For every **negative image** (non human skulls plus other objects), the image was labeled with class 'Not Skull`. No bounding box was drawn.

## Results

Full testing output from the trained model can be found under `results/`. In the images, the green boxes are the final predictions after merging, and red are all predictions after applying a threshold of confidence, but before merging.

For the test dataset used, average accuracy was 90%.

#### Positive Images
Below are some positive images that were classified correctly. Most of the positively classified images, as below, are images that contain a standalone skull whereas some of them also contain noise in the background.
![Positive images](/results/misc/good_results.png)

![Negative images](/results/misc/positive_negatve_results.png)
#### Negative Images
Most of the negative images were classified correctly, however as we can see below, some of the negative images that were positively classified contain backgorunds, skeletons, faces or facial-like features such as eyes. The trained model drew bounding boxes around random objects in addition to the human skull (if present). 




## Discussion

#### What foundation did you use for your project? What did you modify and what did you keep identical?
We used TensorBox for this project. TensorBox is a new framework that is used for training models to detect
objects in images. TensorBox is based on TensorFlow. 

The training image set in our case is very small. We were only able to collect and annotate around 1350(including augmented versions) skull images due to time limitations. 

#### Describe your pipeline and pre-processing steps
The dataset consists of images of human skulls, animal skulls, cartoon faces, human faces, random objects and surroundings. 
Each of the image was labelled and annotated manually using the Annotate webapp. A positive image was annotated with bounding box(es) around areas of skull(s). 

* The training set consistsed of 1780 images with 1000 positive images
* The validation set consisted of 440 images with 296 positive images
* The testing set consisted of 78 images with 54 positive images

We used a split of 80/20 training/validation to train the model.

##### Training pipeline
1. Prepare the training and validation data files using the webapp
2. Using the dataset, we train the model for 9 epochs

##### Testing pipeline
1. Prepare the testing data and evaluate it using the model trained by TensorBox. 
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
3. Train the model for more epochs
4. Use more variations of image augmentations such as shearing, rotation to increase the accuracy.
5. For web app, use outlier detection to prevent spam in the training set
6. For web app, fix canvas drawing for large resolution images

