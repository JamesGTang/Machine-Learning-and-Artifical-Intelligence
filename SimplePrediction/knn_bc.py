"""
Using dataset from UCI
http://archive.ics.uci.edu/ml/datasets.html?format=&task=cla&att=&area=&numAtt=&numIns=&type=&sort=nameUp&view=table

    Attribute Information: (class attribute has been moved to last column)

   #  Attribute                     Domain
   -- -----------------------------------------
   1. Sample code number            id number
   2. Clump Thickness               1 - 10
   3. Uniformity of Cell Size       1 - 10
   4. Uniformity of Cell Shape      1 - 10
   5. Marginal Adhesion             1 - 10
   6. Single Epithelial Cell Size   1 - 10
   7. Bare Nuclei                   1 - 10
   8. Bland Chromatin               1 - 10
   9. Normal Nucleoli               1 - 10
  10. Mitoses                       1 - 10
  11. Class:                        (2 for benign, 4 for malignant)

    Missing attribute values: 16

   There are 16 instances in Groups 1 to 6 that contain a single missing
   (i.e., unavailable) attribute value, now denoted by "?"

   9. Class distribution:
   Benign: 458 (65.5%)
   Malignant: 241 (34.5%)
   http://archive.ics.uci.edu/ml/machine-learning-databases/breast-cancer-wisconsin/breast-cancer-wisconsin.names
"""

import numpy as np
from sklearn import preprocessing
from sklearn.model_selection import train_test_split
import pandas as pd
import tensorflow as tf
import time

Neighbors = 4
Training_step=1

data_frame=pd.read_csv('./data/breast-cancer-wisconsin.csv',encoding='gbk')
# replace missing data with outlier inplace
data_frame.replace('?',-99999,inplace=True)
Y=np.array(data_frame['class'])

data_frame.drop(['id'],1,inplace=True)
X=np.array(data_frame.drop(['class'],1))

# splits dataset for cross validation
x_train,x_test,y_train,y_test=train_test_split(X,Y,test_size=0.3,random_state=0)
y_train.shape=(489,1)

# tf Graph Input
x_training = tf.placeholder("float",[None,9],name="x_training_ph")
y_training = tf.placeholder("float",[None,1],name="y_training_ph")
x_testing = tf.placeholder("float",[9],name="x_testing_ph")

eucli_distance = tf.negative(tf.sqrt(tf.reduce_sum(tf.square(tf.subtract((x_training), (x_testing))), axis=0)))

values, indices = tf.nn.top_k(eucli_distance, k=Neighbors, sorted=False)

nearest_neighbors = []
for i in range(Neighbors):
    #Returns the index with the largest value across axes of a tensor.
    nearest_neighbors.append(tf.argmax(y_training[indices[i]], 0))

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
init = tf.global_variables_initializer()

start_time=time.time()

# Launch the graph
with tf.Session() as sess:
    sess.run(init)

    # loop over test data
    for i in range(len(x_test)):
        # Get nearest neighbor
        # feed to place holder

        nn_index = sess.run(pred, feed_dict={x_training: x_train, y_training : y_train, x_testing: x_test[i, :]})
        distance = sess.run(eucli_distance, feed_dict={x_training: x_train, y_training : y_train, x_testing: x_test[i, :]})
        print("Distnace is ", len(distance), " ", distance)
        values = sess.run(values, feed_dict={x_training: x_train, y_training : y_train, x_testing: x_test[i, :]})
        print("Value is ", len(values), " ", values)
        print("Case:", i, "Prediction:", nn_index,
             "True label", np.argmax(y_test[i]))
        #Calculate accuracy
        if nn_index == np.argmax(y_test[i]):
            accuracy += 1. / len(x_test)
        else:
            print("Not matched")
    print("==========================================")
    print('Neighbors:',Neighbors)
    print('Training step:',Training_step)
    print("Time used: %s second" % (time.time() - start_time))
    print("Accuracy:", accuracy)
