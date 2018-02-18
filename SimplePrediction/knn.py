"""
    KNN: use intuition to classify a new point x
    Voronoi tesselation: partiion space into regions where each region is dominated by one data point
    classification boundary: non-linear reflects classes well, the boundary can be very complicated
    knn can also be used to predict regression

"""
from __future__ import print_function

"""
    You can use future to help to port your code from Python 2 to Python 3 today – and still have it run on Python 2.
    If you already have Python 3 code, you can instead use future to offer Python 2 compatibility with almost no eimga work.
    This bring print function to python2
    https://docs.python.org/2/library/__future__.html
"""

import numpy as np
import tensorflow as tf
import time
import matplotlib.pyplot as plt
# Import MNIST data
from tensorflow.examples.tutorials.mnist import input_data

Neighbors = 4
Training_step=500
Train_Batch=12000

mnist = input_data.read_data_sets("/tmp/data/", one_hot=True)

# load 5500 training data into set
img_training_set, label_training_set = mnist.train.next_batch(Train_Batch)  # whole training set
# we will test a dataset of 100
img_testing_set, label_testing_set = mnist.test.next_batch(Training_step)  # whole test set

# tf Graph Input
img_training = tf.placeholder("float", [None, 784])
label_training = tf.placeholder("float", [None, 10])
img_testing = tf.placeholder("float", [784])

# Euclidean Distance
# reduce the sum by one dimension
distance = tf.negative(tf.sqrt(tf.reduce_sum(tf.square(tf.subtract(img_training, img_testing)), axis=1)))

# Prediction: Get min distance neighbors
# Finds values and indices of the k largest entries for the last dimension.
# input: 1-D or higher Tensor with last dimension at least k.
# k: 0-D int32 Tensor. Number of top elements to look for along the last dimension (along each row for matrices).
# values: The k largest elements along each last dimensional slice.
# indices: The indices of values within the last dimension of input.

values, indices = tf.nn.top_k(distance, k=Neighbors, sorted=False)

nearest_neighbors = []
for i in range(Neighbors):
    #Returns the index with the largest value across axes of a tensor.
    nearest_neighbors.append(tf.argmax(label_training[indices[i]], 0))

#stack the tensor together
neighbors_tensor = tf.stack(nearest_neighbors)

#returns a tensor y containing all of the unique elements of x sorted in the same order that they occur in x.
# This operation also returns a tensor idx the same size as x that contains the index of each value of x in the unique output y
y, idx, count = tf.unique_with_counts(neighbors_tensor)

#This operation extracts a slice of size size from a tensor input starting at the location specified by begin.
#Get the closest neightbor
pred = tf.slice(y, begin=[tf.argmax(count, 0)], size=tf.constant([1], dtype=tf.int64))[0]

accuracy = 0.

# Initializing the variables
init = tf.initialize_all_variables()

start_time=time.time()

# Launch the graph
with tf.Session() as sess:
    sess.run(init)

    # loop over test data
    for i in range(len(img_testing_set)):
        # Get nearest neighbor
        # feed to place holder
        nn_index = sess.run(pred, feed_dict={img_training: img_training_set, label_training: label_training_set, img_testing: img_testing_set[i, :]})
        distances = sess.run(distance, feed_dict={img_training: img_training_set, label_training: label_training_set,
                                                 img_testing: img_testing_set[i, :]})
        """ This is for testing only
        distance=sess.run(distance, feed_dict={img_training: img_training_set, label_training: label_training_set, img_testing: img_testing_set[i, :]})
        print("Distnace is ",len(distance)," ",distance)
        values=sess.run(values, feed_dict={img_training: img_training_set, label_training: label_training_set, img_testing: img_testing_set[i, :]})
        print("Value is ", len(values), " ", values)
        nearest_neighbors = sess.run(nearest_neighbors, feed_dict={img_training: img_training_set, label_training: label_training_set,
                                             img_testing: img_testing_set[i, :]})
        print("Nearest neighbors ", len(nearest_neighbors), " ", nearest_neighbors)
        # Get nearest neighbor class label and compare it to its true label
        """
        print("Case:", i, "Prediction:", nn_index,
             "True label", np.argmax(label_testing_set[i]))
        #Calculate accuracy
        if nn_index == np.argmax(label_testing_set[i]):
            accuracy += 1. / len(img_testing_set)
        else:
            print("Not matched")
    print("==========================================")
    print('Neighbors:',Neighbors)
    print('Training step:',Training_step)
    print("Training batch:",Train_Batch)
    print("Time used: %s second" % (time.time() - start_time))
    print("Accuracy:", accuracy)

"""
Some trial result

Neighbors: 4
Training step: 500
Training batch: 3000
Time used: 1.8929190635681152
Accuracy: 0.9160000000000007
==========================================
Neighbors: 4
Training step: 500
Training batch: 6000
Time used: 6.029782056808472 second
Accuracy: 0.9240000000000007
==========================================
Neighbors: 4
Training step: 500
Training batch: 12000
Time used: 11.018649816513062 second
Accuracy: 0.9300000000000007
==========================================
Neighbors: 5
Training step: 500
Training batch: 12000
Time used: 11.197718143463135 second
Accuracy: 0.9640000000000007
==========================================
Neighbors: 6
Training step: 500
Training batch: 12000
Time used: 11.186767816543579 second
Accuracy: 0.9540000000000007


The Training batch and time used has linear relationship, the bigger the batch, the better the result

"""