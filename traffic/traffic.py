import random
import cv2
import numpy as np
import os
import sys
import tensorflow as tf

from sklearn.model_selection import train_test_split

EPOCHS = 10
IMG_WIDTH = 30
IMG_HEIGHT = 30
NUM_CATEGORIES = 43
TEST_SIZE = 0.45


def main():

    # Check command-line arguments
    if len(sys.argv) not in [2, 3]:
        sys.exit("Usage: python traffic.py data_directory [model.h5]")

    # Get image arrays and labels for all image files
    images, labels = load_data(sys.argv[1])
    # Split data into training and testing sets
    labels = tf.keras.utils.to_categorical(labels)
    x_train, x_test, y_train, y_test = train_test_split(
        np.array(images), np.array(labels), test_size=TEST_SIZE
    )

    # Get a compiled neural network
    model = get_model()

    # Fit model on training data
    print(f"-------------------------------------- \nTRAING MODEL:\n--------------------------------------")
    model.fit(x_train, y_train, epochs=EPOCHS)

    # Evaluate neural network performance
    model.evaluate(x_test,  y_test, verbose=2)

    # Save model to file
    if len(sys.argv) == 3:
        filename = sys.argv[2]
        model.save(filename)
        print(f"Model saved to {filename}.")


def load_data(data_dir):
    """
    Load image data from directory `data_dir`.

    Assume `data_dir` has one directory named after each category, numbered
    0 through NUM_CATEGORIES - 1. Inside each category directory will be some
    number of image files.

    Return tuple `(images, labels)`. `images` should be a list of all
    of the images in the data directory, where each image is formatted as a
    numpy ndarray with dimensions IMG_WIDTH x IMG_HEIGHT x 3. `labels` should
    be a list of integer labels, representing the categories for each of the
    corresponding `images`.
    """
    show_size = True
    images = []
    labels = []
    #goes through the data_dir
    for dirpath, dirname, filenames in os.walk(data_dir):
        #goes by each image
        for name in filenames:
            #ignores the weird thing that we don't need, i think
            if name != ".DS_Store":
                #gets the label and img path
                label = int(os.path.basename(dirpath))
                img_path = os.path.join(dirpath, name)
                #interprets and resizes the img
                img = cv2.imread(img_path, flags= cv2.IMREAD_COLOR)
                img = cv2.resize(img, (IMG_WIDTH, IMG_HEIGHT))


                #adds the image and its label to the lists
                labels.append(label)
                images.append(img)

    print(f"-------------------------------------- \n(temporary) size of random Image: {random.choice(images).shape}")
    print("data loaded (finally)\n--------------------------------------")
    return (images, labels)

def get_model():
    """
    Returns a compiled convolutional neural network model. Assume that the
    `input_shape` of the first layer is `(IMG_WIDTH, IMG_HEIGHT, 3)`.
    The output layer should have `NUM_CATEGORIES` units, one for each category.
    """
    print(f"COMPILING MODEL:\n--------------------------------------")
    model = tf.keras.models.Sequential([

        # Convolutional layer. Learn 30 filters using a 3x3 kernel
        tf.keras.layers.Conv2D(40, (5, 5), activation="gelu", input_shape=(IMG_WIDTH, IMG_HEIGHT, 3)),

        #add a hidden layer before the pooling to keep in mind the original size and the more detailed features (i hope)
        tf.keras.layers.Dense(25, activation="softmax"),

        # Max-pooling layer, using 3x3 pool size
        tf.keras.layers.MaxPooling2D(pool_size=(2, 2)),
        
        #Add some more filters after the pooling, now with a smaller kernel.
        tf.keras.layers.Conv2D(30, (3, 3), activation="relu", input_shape=(IMG_WIDTH/2, IMG_HEIGHT/2, 3)),

        # Flatten units
        tf.keras.layers.Flatten(),
        
        #add a hidden layer after the flattening
        tf.keras.layers.Dense(150, activation="relu"),

        # Add hidden layers with dropout
        tf.keras.layers.Dropout(0.45),

        # Add an output layer with output units for all 10 digits
        tf.keras.layers.Dense(NUM_CATEGORIES, activation="softmax")
    ])

    # Train neural network
    model.compile(
        optimizer="adam",
        loss="categorical_crossentropy",
        metrics=["accuracy"]
    )

    return model
    #raise NotImplementedError

if __name__ == "__main__":
    main()
