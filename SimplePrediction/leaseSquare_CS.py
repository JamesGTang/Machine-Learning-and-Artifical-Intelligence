from __future__ import print_function

"""
This code is used to anaylze the RGB value from color sensor and try to find linear relationship
between distance and value. the code is related to repository
https://github.com/JamesGTang/Robotics/tree/master/Search_Localize

"""
import tensorflow as tf
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

# Parameters
learning_rate = 0.025
training_epochs = 200
display_step = 50

# total data point per color variation is 400, keep 1st row as header and do not skip row
data_frame=pd.read_csv('./data/RGB.csv',encoding='gbk',nrows=400,skiprows=range(1,0))
# replace missing data with outlier inplace
data_frame.replace('RED',0,inplace=True)
data_frame.replace('BLUE',1,inplace=True)
data_frame.replace('YELLOW',2,inplace=True)
data_frame.replace('WHITE',4,inplace=True)

# Split the data into training/testing sets
X_set=np.array(data_frame['Red'])
X_set.shape=(400,1)
Y_set=np.array(data_frame['Distance'])
Y_set.shape=(400,1)
#X_set.shape[0]

# Split the targets into training/testing sets
train_Y = tf.constant(Y_set,dtype=tf.float32,shape=[400,1])
train_X = tf.constant(X_set,dtype=tf.float32,shape=[400,1])


X = tf.placeholder("float")
Y = tf.placeholder("float")

w = tf.Variable(tf.truncated_normal(shape=[1, 1], mean=0.0, stddev=1.0, dtype=tf.float32), name="weight")

b = tf.Variable(tf.zeros(1, tf.float32, name="bias"))


def calc(x, y):
    prediction = tf.add(b, tf.multiply(x, w))
    # use reduce mean
    error = tf.reduce_mean(tf.square(y - prediction))
    return [prediction, error]


# calculate the cost
prediction, cost = calc(X, Y)

# Gradient descent
optimizer = tf.train.GradientDescentOptimizer(learning_rate).minimize(cost)

# Initializing the variables
init = tf.global_variables_initializer()

# Launch the graph
with tf.Session() as sess:
    sess.run(init)

    # Fit all training data
    for epoch in range(training_epochs):
        for (x, y) in zip(sess.run(train_X), sess.run(train_Y)):
            #print(x,y)
            sess.run(optimizer, feed_dict={X: x, Y: y})
            # Display log every 50
            if (epoch + 1) % display_step == 0:
                c = sess.run(cost, feed_dict={X: sess.run(train_X), Y: sess.run(train_Y)})
                print("Epoch:", (epoch + 1), "cost=", c, \
                  "W=", sess.run(w), "b=", sess.run(b))

    print("Model Run finished")
    training_cost = sess.run(cost, feed_dict={X: sess.run(train_X), Y: sess.run(train_Y)})
    print("Training cost=", training_cost, "W=", sess.run(w), "b=", sess.run(b), '\n')

    # Graphic display
    plt.plot(X_set, Y_set, 'ro', label='Scatter Data')
    plt.plot(X_set, sess.run(w) * X_set + sess.run(b), label='Line of Best Fit')
    plt.legend()
    plt.show()