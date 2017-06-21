# Web app to annotate/label training images

## Description

The web app let's the user annotate images by drawing a red color bounding box around the skulls in the image. The user can label the image with *Skull* or *Not Skull* class.
Once the user clicks the Save button; the metadata of the annotated image such as `(image_name, [[x0, y0, x1, y1, width, height]], class)` is stored in a csv file. 
The csv file gets downloaded when the user downloads the training images.

Non-Maximum Suppression(NSM) support has been added to combine multiple bounding boxes for an image. This helps in suppressing all the image information and displaing only
the essential bounding boxes.

No annotated images are stored in any directory. Whenever the user wants to view/download the training images; we make use of the coordinates present in the .csv
to draw the bounding box on the fly. user can view/download the training images both with NSM and without NSM.

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

Once installed, head to the TrainImage_Annotate project and execute:
```
python manage.py runserver
```

Go to the browser and type in `localhost:8000/draw`


