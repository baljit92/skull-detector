# Web app to annotate/label training images

## Instructions to run
There are two main scripts to this project, both in the `src/` folder. The following pre-requisites need to be satisified for the project to run:
* Python 2.7
* Django 1.11.2
* pip

Following commands can be used to install Django on both macOs and Unix machines:
```
pip install Django==1.11.2
```

Once installed, head to the TrainImage_Annotate project and execute:
```
python manage.py runserver
```

Go to the browser and type in `localhost:8000/draw`