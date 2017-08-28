# call: python3 rand_feat_file_maker.py <# of features> <training data> <testing data> <new training file> <new testing file>

# This application creates two new data files (train and test)
# that can be used with svm light package to train and svm
# and test the model that traing gets

# This application uses random feature selection to pick
# m number of features to use to train/test samples


import os
import sys
import random

#vars
# empty weight dictionary (attr #: weight)
num_features = 57
weights = {}

#get a random feature selection
order_num = [i for i in range(1, 58)]
random.shuffle(order_num)

#keep number of features (num specified)

#number of weights to keep
m_weights = int(sys.argv[1])
delete_feature = order_num[m_weights:len(order_num)]

#format training data
file_name = sys.argv[2]
text_file = open(file_name, "r")
lines = text_file.readlines()
text_file.close()

training = []
for line in range(len(lines)):
  training.append(lines[line].split(" "))
  for feature in range(len(training[line]) - 2, 0, -1):
    idx = training[line][feature].find(":")
    if int(training[line][feature][:idx]) in delete_feature:
      del training[line][feature]

#format testing data
file_name = sys.argv[3]
text_file = open(file_name, "r")
lines = text_file.readlines()
text_file.close()

testing = []
for line in range(len(lines)):
  testing.append(lines[line].split(" "))
  for feature in range(len(testing[line]) - 2, 0, -1):
    idx = testing[line][feature].find(":")
    if int(testing[line][feature][:idx]) in delete_feature:
      del testing[line][feature]

#write the new train files
file_name = sys.argv[4]
text_file = open(file_name, "w")

for i in range(len(training)):
  for j in range(len(training[i])):
    if training[i][j] == "\n":
      text_file.write(training[i][j])
    else:
      text_file.write(training[i][j] + " ")

text_file.close()

#write the new testing file
file_name = sys.argv[5]
text_file = open(file_name, "w")

for i in range(len(testing)):
  for j in range(len(testing[i])):
    if testing[i][j] == "\n":
      text_file.write(testing[i][j])
    else:
      text_file.write(testing[i][j] + " ")

text_file.close()
