# Perceptron-Classifier
 Perceptron classifiers (vanilla and averaged) to identify hotel reviews as either true or fake, and either positive or negative. It uses the word tokens as features.
 
 # Data
 
One file train-labeled.txt containing labeled training data with a single training instance (hotel review) per line. The first 3 tokens in each line are:
a unique 7-character alphanumeric identifier
a label True or Fake
a label Pos or Neg
These are followed by the text of the review.
One file dev-text.txt with unlabeled development data, containing just the unique identifier followed by the text of the review.
One file dev-key.txt with the corresponding labels for the development data, to serve as an answer key.

# Programs

There are two programs: perceplearn.py will learn perceptron models (vanilla and averaged) from the training data, and percepclassify.py will use the models to classify new data. The learning program will be invoked in the following way:

> python perceplearn.py /path/to/input
ex:
> python perceplearn.py train-labeled.txt

The argument is a single file containing the training data; the program will learn perceptron models, and write the model parameters to two files: vanillamodel.txt for the vanilla perceptron, and averagedmodel.txt for the averaged perceptron. 
The classification program will be invoked in the following way:

> python percepclassify.py /path/to/model /path/to/input
ex:
> python percepclassify.py vanillamodel.txt dev-text.txt

The first argument is the path to the model file (vanillamodel.txt or averagedmodel.txt), and the second argument is the path to a file containing the test data file; the program will read the parameters of a perceptron model from the model file, classify each entry in the test data, and write the results to a text file called percepoutput.txt in the same format as the answer key.

# Results
Results (Vanilla model):
Neg 0.94 0.89 0.92
True 0.84 0.83 0.83
Pos 0.90 0.94 0.92
Fake 0.83 0.84 0.83
Mean F1: 0.8765
{'Neg': {'fp': 9, 'fn': 17, 'tp': 143}, 'True': {'fp': 26, 'fn': 27, 'tp': 133}, 'Pos': {'fp': 17, 'fn': 9, 'tp': 151}, 'Fake': {'fp': 27, 'fn': 26, 'tp': 134}}
100

Results (Averaged model):
Neg 0.94 0.91 0.92
True 0.83 0.87 0.85
Pos 0.91 0.94 0.92
Fake 0.86 0.82 0.84
Mean F1: 0.8828
{'Neg': {'fp': 10, 'fn': 15, 'tp': 145}, 'True': {'fp': 29, 'fn': 21, 'tp': 139}, 'Pos': {'fp': 15, 'fn': 10, 'tp': 150}, 'Fake': {'fp': 21, 'fn': 29, 'tp': 131}}

99.8190863863
