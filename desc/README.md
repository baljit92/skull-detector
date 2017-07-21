# Center for Medical Innovation, Software, and Technology
### Sidra Medical Research Center
![](https://raw.githubusercontent.com/CMIST/HiringExercise_MLCVEngineer/master/logo_cmist.png "CMIST LOGO")

Dear Candidate,

Congratulations on your candidacy to the CMIST Division (Center for Medical Innovation, Software, and Technology) at Sidra Medical Research Center.  Our hiring process is gated and involves four steps:
1.	**Technical Competency** - evaluated from job application
2.	**Technical Mastery** - evaluated via application and phone screen with hiring manager
3.	**Delivery Capability** - evaluated via this take-home exercise
4.	**Organizational Fit** - evaluated via group interview 

This repository details item three – a take-home exercise which aims to evaluate your ability to deliver.  With this, we are observing three major things:
1.  Ability to find and use existing solutions
2.	Technical Correctness
3.	Communication and Presentation
4.	Self-Management

### Rationale for this Exercise
Without working with confidential medical images, this exercise closely resembles types of work we do in the group, specifically:
* Find existing solutions we can build upon, try to not "re-create the wheel"
* Dealing with heterogeneous in-the-wild samples (various sizes, various aspect ratios.)  
* Execute object detection with 0,1,1+ cases per image
* Communicating ideas
* Managing own efforts 

This exercise is geared towards Position # 4285 (Developer: Machine Learning and Computer Vision,) which is a complementary role to Position # 4338 (Machine Learning: Deep Neural Networks Specialist.)  Since this is a complementary role, we tried to make the hiring exercise realistic, even to the point of interacting with the complementary role's hiring exercise.  Accordingly, you may wish to see the hiring exercise for the other role (https://github.com/CMIST/HiringExercise_MLCVEngineer) so you can build upon that -- there are several great solutions available for the upstream assignment and you should try and build upon an existing solution.

### The Exercise

Please find an existing model which can be used to recognize and annotate cats in photos.  The easiest way will be to find an existing public solution for https://github.com/CMIST/HiringExercise_MLCVEngineer (our upstream exercise.)  Of course, you are welcome to use any existing solution or even build your own from scratch.  Make sure to reference what you used as your foundation.  

Your goal is to swap the cat detector with skulls (more relevant to the hospital) and train a skull detector.  The first step will be to gather some training images, you are welcome to use anything on the web.  You can use photos or xrays or any variation.  You will want to also keep some negative images that are not skulls.  Below are some sample positive and negative images for guidance.

![](https://raw.githubusercontent.com/CMIST/HiringExercise_MLEngineer/master/sample_images/skullA.jpg "Skull")
![](https://raw.githubusercontent.com/CMIST/HiringExercise_MLEngineer/master/sample_images/skullB.jpg "Skull")
![](https://raw.githubusercontent.com/CMIST/HiringExercise_MLEngineer/master/sample_images/negative2.jpg "Negative Image")
![](https://raw.githubusercontent.com/CMIST/HiringExercise_MLEngineer/master/sample_images/skullC.jpg "Skull")
![](https://raw.githubusercontent.com/CMIST/HiringExercise_MLEngineer/master/sample_images/negative3.jpg "Negative Image")
![](https://raw.githubusercontent.com/CMIST/HiringExercise_MLEngineer/master/sample_images/skullD.jpg "Skull")
![](https://raw.githubusercontent.com/CMIST/HiringExercise_MLEngineer/master/sample_images/skullE.jpg "Skull")
![](https://raw.githubusercontent.com/CMIST/HiringExercise_MLEngineer/master/sample_images/negative1.jpg "Negative Image")
![](https://raw.githubusercontent.com/CMIST/HiringExercise_MLEngineer/master/sample_images/skullF.jpg "Skull")

Next, create a simple web-app that lets you label/annotate training images (you'll need this to do the next step.)  You'll want a simple one-page app that lets you label images as "Skulls" or "Not-Skull" and for skulls, give the user/annotator a facility to draw+save a bounding box around the object area of interest.  Note we usually work in Python, so ideally use Django/Flask+Javascript, however you are welcome to use anything you are comfortable with, as long as it can be independently run and evaluated by us.  Dont worry about making it pretty, the page can be ugly.  You are being judged on functionality, not UI/UX/design.

Re-train the foundational project you chose (or wrote yourself) to instead detect skulls.  Re-test the model to ensure it detects skulls and only skulls.  We'll be providing a blind test set to test your application.
 
Please deliver back all scripts (and everything else referenced) as well as a corresponding set of training images you used.  Your scripts should be all-encompassing, including pipeline steps and acquisition of any training sets.  If you need a setup script, that can also be included.

Your submission should be via Github.  The exercise can be done in any language (though we prefer python) as long as the submission can be successfully executed.  Please do not use paid platforms like MATLAB.  If you are completely agnostic, you can use our in-house standard: TensorFlow + Keras or Caffe2.  We plan to execute this on an AWS EC2 G-series machine.  To this point, please detail your selected environment, machine learning / computer vision platform and any other setup steps so we can re-train and re-test your model from scratch.

There is no need to re-create the wheel here, use any and all open-source or vendor-provided scripts that you can.  Ensure to include them so the submission is all-encompassing.  **Do not** include anything irrelevant to the goal of this exercise, we want the minimal set of files/work which achieves the goal and nothing more.

### Discussion Questions
1.	What foundation did you use for your project?  What did you modify and what did you keep identical?
2.	Describe your pipeline and pre-processing steps
3.	How long did your training and inference take?
4.	If you had more time, how would you expand on this submission?

Good Luck!