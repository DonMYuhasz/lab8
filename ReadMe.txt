CNN:
Convolution neaural network
requires:tensorflow, numpy, matplotlib, PIL and keras_tuner

Uses a retrain boolean to train or load a neural net. somwhat consistantly achieves 82% accuracy on the cifar 10 validation set. requires a my_dir file to set neural net params and a checkpoints directory to load weights. without these directories it can attempt to retrain a neural net and save new weights

modifications to the original google collab file allow automatic parameter tuning and weight saving. sadly the tuning apparently doesn't have enough scope for it to reach 90% accuracy
Ballon Flight:

created to match the program Coding games in Python
modifed to have multiple lives, increasing speed, a level system, more max score spaces, it also should be tolerant of screen width changes. were I inspired to continue I'd add pickup items to the game.