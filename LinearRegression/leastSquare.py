from __future__ import print_function
"""
This code is adopted based on stackoverflow

https://stackoverflow.com/questions/43170017/linear-regression-with-tensorflow

"""
import tensorflow as tf
# import a sample dataset from skylearn
""" There are some sample datasets that can be used
load_boston([return_X_y])   Load and return the boston house-prices dataset (regression).
load_iris([return_X_y]) Load and return the iris dataset (classification).
load_diabetes([return_X_y]) Load and return the diabetes dataset (regression).
load_digits([n_class, return_X_y])  Load and return the digits dataset (classification).
load_linnerud([return_X_y]) Load and return the linnerud dataset (multivariate regression).
load_wine([return_X_y]) Load and return the wine dataset (classification).
load_breast_cancer([return_X_y])    Load and return the breast cancer wisconsin dataset (classification).
ther are also data generator
http://scikit-learn.org/stable/datasets/index.html
"""
from sklearn.datasets import load_diabetes
from sklearn.preprocessing import scale
import numpy as np
import numpy
import matplotlib.pyplot as plt
# for sklearn only
#from sklearn import datasets, linear_model
#from sklearn.metrics import mean_squared_error, r2_score

# Parameters
learning_rate = 0.025
training_epochs = 1000
display_step = 50

# training data
# load data and target into separate array, when True 
# http://scikit-learn.org/stable/modules/generated/sklearn.datasets.load_boston.html
diabetes = load_diabetes()


# Use only one feature
"""
Could use scale to standarize the data
sklearn.preprocessing.scale(X, axis=0, with_mean=True, with_std=True, copy=True)
with_mean : boolean, True by default If True, center the data before scaling.
with_std : boolean, True by default If True, scale the data to unit variance (or equivalently, unit standard deviation).
Standardize a dataset along any axis
Center to the mean and component wise scale to unit variance.

"""
diabetes_X = diabetes.data[:, np.newaxis, 2]

# Split the data into training/testing sets
train_X = diabetes_X[:-20]
test_X = diabetes_X[-20:]
n_samples=train_X.shape[0]

# Split the targets into training/testing sets
train_Y = diabetes.target[:-20]
test_Y = diabetes.target[-20:]

"""
use sklearn regression instead of tensorflow
http://scikit-learn.org/stable/auto_examples/linear_model/plot_ols.html#sphx-glr-auto-examples-linear-model-plot-ols-py
# Create linear regression object
regr = linear_model.LinearRegression()

# Train the model using the training sets
regr.fit(diabetes_X_train, diabetes_y_train)

# Make predictions using the testing set
diabetes_y_pred = regr.predict(diabetes_X_test)
"""

#print(train_X)
#print(train_Y)
"""
There are various kinds of useful ops in TensorFlow. Some important ones are constant, placeholder and variable. 
Constants, as the name suggests, are nodes used to hold static values. 
Placeholders are containers in memory that can be fed different values at each execution of the program. 
Variables are ops whose values can change.
"""

X = tf.placeholder("float")
Y = tf.placeholder("float")

# Use random values from a truncated normal distribution to populate w
# random value is considered good pratice
"""
tf.truncated_normal(shape, mean=0.0, stddev=1.0, dtype=tf.float32, seed=None, name=None)
mean: A 0-D Tensor or Python value of type dtype. The mean of the truncated normal distribution.
stddev: A 0-D Tensor or Python value of type dtype. The standard deviation of the truncated normal distribution.
dtype: The type of the output.
seed: A Python integer. Used to create a random seed for the distribution. See tf.set_random_seed for behavior.
https://www.tensorflow.org/versions/r1.0/api_docs/python/tf/truncated_normal
"""

w = tf.Variable(tf.truncated_normal(shape=[1,1],mean=0.0, stddev=1.0, dtype=tf.float32),name="weight")
"""
w = tf.Variable(tf.truncated_normal([13, 1], mean=0.0, stddev=1.0, dtype=tf.float64))
"""

"""    
Creates a tensor with all elements set to zero.
b = tf.Variable(tf.zeros(1, dtype = tf.float64), name="bias")
tf.zeros([3, 4], tf.int32)  # [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]
"""
b=tf.Variable(tf.zeros(1, tf.float32,name="bias"))

def calc(x,y):
    prediction = tf.add(b,tf.multiply(x, w))
    # use reduce mean
    error = tf.reduce_mean(tf.square(y - prediction))
    # could use mean square error
    # error=tf.reduce_sum(tf.pow(prediction-Y, 2))/(2*n_samples)
    return [prediction,error]

# calculate the cost
prediction,cost=calc(X,Y)

# Gradient descent
optimizer = tf.train.GradientDescentOptimizer(learning_rate).minimize(cost)

# Initializing the variables
init = tf.global_variables_initializer()

# Launch the graph
with tf.Session() as sess:
    sess.run(init)

    # Fit all training data
    for epoch in range(training_epochs):
        # https://docs.python.org/3.3/library/functions.html#zip
        # zip makes iterator that aggreates elements from each of the iterables
        for (x, y) in zip(train_X, train_Y):
            # use feed_dict to feed data into the place holder
            sess.run(optimizer, feed_dict={X: x, Y: y})
        
        # Display log every 50
        if (epoch+1) % display_step == 0:
            c = sess.run(cost, feed_dict={X: train_X, Y:train_Y})
            print("Epoch:", (epoch+1), "cost=", c, \
                "W=", sess.run(w), "b=", sess.run(b))
            
    print("Model Run finished")
    training_cost = sess.run(cost, feed_dict={X: train_X, Y: train_Y})
    print("Training cost=", training_cost, "W=", sess.run(w), "b=", sess.run(b), '\n')

    # Graphic display
    plt.plot(train_X, train_Y, 'ro', label='Scatter Data')
    plt.plot(train_X, sess.run(w) * train_X + sess.run(b), label='Line of Best Fit')
    plt.legend()
    plt.show()