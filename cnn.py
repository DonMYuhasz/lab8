# -*- coding: utf-8 -*-
"""cnn.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/github/tensorflow/docs/blob/master/site/en/tutorials/images/cnn.ipynb

##### Copyright 2019 The TensorFlow Authors.
"""

#@title Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""# Convolutional Neural Network (CNN)

<table class="tfo-notebook-buttons" align="left">
  <td>
    <a target="_blank" href="https://www.tensorflow.org/tutorials/images/cnn">
    <img src="https://www.tensorflow.org/images/tf_logo_32px.png" />
    View on TensorFlow.org</a>
  </td>
  <td>
    <a target="_blank" href="https://colab.research.google.com/github/tensorflow/docs/blob/master/site/en/tutorials/images/cnn.ipynb">
    <img src="https://www.tensorflow.org/images/colab_logo_32px.png" />
    Run in Google Colab</a>
  </td>
  <td>
    <a target="_blank" href="https://github.com/tensorflow/docs/blob/master/site/en/tutorials/images/cnn.ipynb">
    <img src="https://www.tensorflow.org/images/GitHub-Mark-32px.png" />
    View source on GitHub</a>
  </td>
  <td>
    <a href="https://storage.googleapis.com/tensorflow_docs/docs/site/en/tutorials/images/cnn.ipynb"><img src="https://www.tensorflow.org/images/download_logo_32px.png" />Download notebook</a>
  </td>
</table>

This tutorial demonstrates training a simple [Convolutional Neural Network](https://developers.google.com/machine-learning/glossary/#convolutional_neural_network) (CNN) to classify [CIFAR images](https://www.cs.toronto.edu/~kriz/cifar.html). Because this tutorial uses the [Keras Sequential API](https://www.tensorflow.org/guide/keras/overview), creating and training your model will take just a few lines of code.

### Import TensorFlow
"""

import tensorflow as tf
import numpy as np
from tensorflow.keras import datasets, layers, models
from tensorflow import keras
import matplotlib.pyplot as plt
import keras_tuner as kt
from PIL import Image
#set true to train a new neural net
retrain = False
#set True to test URL images
test = True
img_url= ["https://cbsnews2.cbsistatic.com/hub/i/r/2017/03/27/73bd41ff-5703-48ca-995c-131d1b3572b4/thumbnail/640x335/10f4b442d725b8fa79d3e2dbf286ba76/air-force-one-two-planes.jpg",
          "https://sniteartmuseum.nd.edu/assets/166204/original/ferrari.jpg",
          "https://upload.wikimedia.org/wikipedia/commons/thumb/f/f0/Another_Airplane%21_%284676723312%29.jpg/1024px-Another_Airplane%21_%284676723312%29.jpghttps://www.kbb.com/wp-content/uploads/2020/04/00-2020-bmw-8-series-gran-coupe.jpg",
          "https://ichef.bbci.co.uk/news/976/cpsprodpb/67CF/production/_108857562_mediaitem108857561.jpg",
          "https://static.toiimg.com/thumb/msid-67586673,width-1070,height-580,overlay-toi_sw,pt-32,y_pad-40,resizemode-75,imgsize-3918697/67586673.jpg",
          "https://media.istockphoto.com/photos/toggenburg-goat-against-white-background-picture-id1069137796?s=612x612"]
#os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

"""### Download and prepare the CIFAR10 dataset


The CIFAR10 dataset contains 60,000 color images in 10 classes, with 6,000 images in each class. The dataset is divided into 50,000 training images and 10,000 testing images. The classes are mutually exclusive and there is no overlap between them.
"""

(train_images, train_labels), (test_images, test_labels) = datasets.cifar10.load_data()



#data_tf = tf.convert_to_tensor(image2, np.float32)

# Normalize pixel values to be between 0 and 1
train_images, test_images = train_images / 255.0, test_images / 255.0

AUTOTUNE = tf.data.AUTOTUNE

"""
train_dataset = tf.data.Dataset.from_tensor_slices((train_images, train_labels))
test_dataset = tf.data.Dataset.from_tensor_slices((test_images, test_labels))

AUTOTUNE = tf.data.AUTOTUNE
train_dataset = train_dataset.cache().shuffle(1000).prefetch(buffer_size=AUTOTUNE)
test_dataset = test_dataset.cache().prefetch(buffer_size=AUTOTUNE)

(train_images, train_labels) = tf.data.Dataset.as_numpy(train_dataset)
(test_images, test_labels) =  tf.data.Dataset.as_numpy(test_dataset)
"""

image_ordering_dim="tf"



def model_compiler(hp):
    hp_units = hp.Int('units', min_value=32, max_value=1024, step=32)
    hp_units2 = hp.Int('units2', min_value=32, max_value=1024, step=32)
    hp_units3 = hp.Int('units3', min_value=32, max_value=1024, step=32)
    hp_units4 = hp.Int('units4', min_value=32, max_value=512, step=32)
    hp_units5 = hp.Int('units5', min_value=32, max_value=512, step=32)
    hp_units6 = hp.Int('units6', min_value=32, max_value=512, step=32)
    hp_units7 = hp.Int('units7', min_value=32, max_value=512, step=32)
    hp_units8 = hp.Int('units8', min_value=32, max_value=512, step=32)
    hp_Batch = hp.Int('BatchNorm',0,3,step=1,default=0)
    hp_drop =hp.Float('dropout', 0, 0.9, step=0.1, default=0.5)
    
    hp_Rotate =hp.Float('rotate', 0, 0.5, step=0.05, default=0.1)
    hp_Zoom =hp.Float('zoom', 0, 0.5, step=0.05, default=0.1)
    
    
    model = models.Sequential()
    #data augmentation layers
    
    model.add(layers.RandomFlip("horizontal"))
    model.add(layers.RandomRotation(hp_Rotate))
    model.add(layers.RandomZoom(hp_Zoom))
    
    
    
    model.add(layers.Conv2D(hp_units5, (3, 3), activation='relu', input_shape=(32, 32, 3)))
    model.add(layers.MaxPooling2D((2, 2)))
    if (hp_Batch == 1) :
        model.add(layers.BatchNormalization())
    model.add(layers.Dense(hp_units4, activation='relu'))
    model.add(layers.Conv2D(hp_units6, (3, 3), activation='relu'))
    model.add(layers.MaxPooling2D((2, 2)))
    if (hp_Batch == 2) :
        model.add(layers.BatchNormalization())
    model.add(layers.Dense(hp_units8, activation='relu'))
    model.add(layers.Conv2D(hp_units7, (3, 3), activation='relu'))
    model.add(layers.MaxPooling2D((2, 2)))
    model.add(layers.Dropout(hp_drop))
    model.add(layers.Flatten())
    model.add(layers.Dense(units = hp_units, activation='relu'))
    model.add(layers.Dense(units = hp_units2, activation='relu'))
    model.add(layers.Dense(units = hp_units3, activation='relu'))
    if (hp_Batch == 0) :
        model.add(layers.BatchNormalization())
    model.add(layers.Dense(10, activation='softmax'))
    
    hp_learning_rate = hp.Choice('learning_rate', values=[1e-2, 1e-3, 1e-4])
    
    model.compile(optimizer=keras.optimizers.Adam(learning_rate=hp_learning_rate),
                  loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=False),
                  metrics=['accuracy'])
    return model

# code eddited from https://www.tensorflow.org/tutorials/keras/keras_tuner
tuner = kt.Hyperband(model_compiler,
                     objective='val_accuracy',
                     max_epochs=10,
                     factor=3,
                     directory='my_dir',
                     project_name='cnn')

stop_early = tf.keras.callbacks.EarlyStopping(monitor='val_loss', patience=5)


tuner.search(train_images,train_labels, epochs=10, validation_data=(test_images,test_labels), callbacks=[stop_early])

# Get the optimal hyperparameters
best_hps=tuner.get_best_hyperparameters(num_trials=1)[0]

"""
#previous best model
#79
#epochs: 20 

data_augmentation = keras.Sequential(
    [
      layers.RandomFlip("horizontal",input_shape = (32,32,3)),
      #layers.RandomRotation(0.4),
      layers.RandomZoom(0.4)
      ])



model = models.Sequential()
model.add(data_augmentation)
model.add(layers.Conv2D(32, (3, 3), activation='relu', input_shape=(32, 32, 3)))
model.add(layers.Dense(128, activation='relu'))
model.add(layers.Conv2D(128, (3, 3), activation='relu'))
model.add(layers.MaxPooling2D((2, 2)))
model.add(layers.Dense(64, activation='relu'))
model.add(layers.Conv2D(64, (3, 3), activation='relu'))
model.add(layers.MaxPooling2D((2, 2)))
model.add(layers.Conv2D(64, (3, 3), activation='relu'))
model.add(layers.Dense(64, activation='relu'))
model.add(layers.Dropout(0.2))
model.add(layers.Conv2D(64, (3, 3), activation='relu'))
model.add(layers.Flatten())
model.add(layers.Dense(64, activation='relu'))
model.add(layers.Dense(10))

"""


model = tuner.hypermodel.build(best_hps)

if retrain == True:
    #best epoch 67
    history = model.fit(train_images,train_labels, epochs=50, 
                        validation_data=(test_images,test_labels))
    model.save_weights('./checkpoints/my_checkpoint')
    







# Save the weights


# Create a new model instance
model = model_compiler(best_hps)

# Restore the weights
model.load_weights('./checkpoints/my_checkpoint')

#model.build()

# Re-evaluate the model
loss, acc = model.evaluate(test_images, test_labels, verbose=2)
print("Restored model, accuracy: {:5.2f}%".format(100 * acc))
if test == True:
    for img_ur in img_url:
        picture_path = tf.keras.utils.get_file( origin=img_ur)
        img = Image.open(picture_path )
        img= img.resize((32,32),Image.ANTIALIAS)
        imgn = np.array(img)
        imgn = imgn/255.0
        imgn = imgn[np.newaxis,:,:]
        prediction = model.predict(imgn)

        print(np.argmax(prediction))
    

#model.summary()

if retrain == True:
    """### Evaluate the model"""
    plt.figure()
    plt.plot(history.history['accuracy'], label='accuracy')
    plt.plot(history.history['val_accuracy'], label = 'val_accuracy')
    plt.xlabel('Epoch')
    plt.ylabel('Accuracy')
    plt.ylim([0.5, 1])
    plt.legend(loc='lower right')

    test_loss, test_acc = model.evaluate(test_images,  test_labels, verbose=2)
    print(test_acc)




