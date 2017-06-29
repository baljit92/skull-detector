# Skull detection in images

Results can be found under `results/`

The web app README file can be found under `src/webapp`.

The machine learning README file can be found under `src/machine_learning`


## Pre-requisites
The following pre-requisites need to be satisified for the machine learning project to run:
* Python 2.7
* TensorBox
* OpenCV
* pip
* pkg-config
* virtualenv
* Pillow 4.1.0

## Instructions to run
To setup TensorFlow and TensorBox, follow instructions below: 

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
	
Below is a solution for a potential error that might come up during TensorBox installation. The commands should be executed inside the `virtualenv`:

1. **Error:** pkg-config python not found

   **Solution for macOS:** 
   
   `export PKG_CONFIG_PATH=/System/Library/Frameworks/Python.framework/Versions/2.7/lib/pkgconfig/; echo $(pkg-config --			variable pc_path pkg-config)${PKG_CONFIG_PATH:+:}${PKG_CONFIG_PATH}`
