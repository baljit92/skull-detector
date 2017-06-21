# Web app to annotate/label training images

## Description

The web app let's the user annotate images by drawing a red color bounding box around the skulls in the image. The user can label the image with *Skull* or *Not Skull* class.
Once the user clicks the Save button; the metadata of the annotated image such as `(image name, x0, y0, x1, y1, width, height, class)` is stored in a .csv file. 
The csv file gets downloaded when the user downloads the annotated images. 

No annotated images are stored in any directory. Whenever the user wants to view/download the annotated images; we make use of the coordinates present in the .csv
to draw the bounding box on the fly.

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


