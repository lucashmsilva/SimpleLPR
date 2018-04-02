# SimpleLPR

I implemented this LPR (license plate recognition) system as a assignment of a DIgital Image Processing course I took at college.

I wrote a small paper with a colleague explaining the system and presenting some results. It's in portuguese, but fell free to email me or open a issue if you have any questions.

# Dependencies

Use python >=3

`pip install matplotlib`

`pip install numpy`

`pip install sci-kit-learn`

`pip install sci-kit-image`

# Usage

First you need to train the models:

 * Extract the dataset inside `imgs`
 * Then run `python train.py` (you can modify the list of models you want to train inside the file. The way it is, it will train all models one after another).
 
 To predict, run `python predict.py` and follow the instructions.
 
 # Basic Functioning
 
When a license plate image is entered, the firt thing to do is segmente the characters inside the image. This is done by combining a series of image processing tecniques until the number of segmented regions (that oby some constaints) match the number of characters at the  image label (or the number of your domain). Then, each segmented charecter is passed thought all the models that try to predict them.
