# many of the ideas in this computation
# are from Ori Cohen translating Perl version
# from Thorsten Joachims.  Original Python code 
# found at the web address below
# https://www.cs.cornell.edu/people/tj/svm_light/svm2weight.py.txt

# This application creates two new data files (train and test)
# that can be used with svm light package to train and svm
# and test the model that traing gets

# This application uses weighted feature selection to pick
# m number of features to use to train/test samples

# call: python3 num_feat_file_maker.py <model_file> <# of features> <training data> <testing data> <new training file> <new testing file>

import os
import sys

#vars
# empty weight dictionary (attr #: weight)
num_features = 57
weights = {}

# file name
file_name = sys.argv[1]

#make sure file exists
if not os.path.exists(file_name):
  print(file_name + " does not exit");
  sys.exit(0)

#open the file
text_file = open(file_name)

#create a list of the lines
lines = text_file.readlines()

#close file
text_file.close()

for line in range(len(lines)):
  if line > 10:
    # only need to process data up to the "#"
    data = lines[line][:lines[line].find("#") - 1]

    # get the alpha value
    alpha = data[:data.find(" ")]

    # all data after the alpha is attr#:value
    features = data[data.find(" ") + 1:]

    #initial run through of this line is to 
    # add the feature number if not in dictionary
    for feature in features.split(" "):
      #get each key/value pair
      key, val = feature.split(":")

      # if the key (attr #) isn't in the 
      # weight dictionary yet, add it
      # with initial value of 0
      if not (int(key) in weights):
        weights[int(key)] = 0

    # go through features in this line again
    # to increment the value for each feature #
    for feature in features.split(" "):
      #get each key/val pair
      key, val = feature.split(":")

      #increment the value for that key
      weights[int(key)] += float(alpha) * float(val)

# list ordered feature number based on weight magnitude
# highest to lowest
for i in range(len(weights)):
  weights[i+1] = abs(weights[i+1])

order_num = [(val, key) for key, val in weights.items()]
order_num.sort()
order_num.reverse()
order_num = [key for val, key in order_num]

#keep highest weight features (num specified)

#number of weights to keep
m_weights = int(sys.argv[2])
delete_feature = order_num[m_weights:len(order_num)]

#format training data
file_name = sys.argv[3]
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
file_name = sys.argv[4]
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
file_name = sys.argv[5]
text_file = open(file_name, "w")

for i in range(len(training)):
  for j in range(len(training[i])):
    if training[i][j] == "\n":
      text_file.write(training[i][j])
    else:
      text_file.write(training[i][j] + " ")

text_file.close()

#write the new testing file
file_name = sys.argv[6]
text_file = open(file_name, "w")

for i in range(len(testing)):
  for j in range(len(testing[i])):
    if testing[i][j] == "\n":
      text_file.write(testing[i][j])
    else:
      text_file.write(testing[i][j] + " ")

text_file.close()



