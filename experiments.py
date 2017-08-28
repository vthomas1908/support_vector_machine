#call: python3 experiments.py <order file maker> <random file maker> <model> <directory> <train file> <test file> <learn file> <classify file> 
#This script
#1. uses the order file maker to make weighted feature selection
#2. uses the random file maker to make random feature selection
#3. creates new train/test files to use in the svm light package
#   and saves files to given directory
#4. runs the svm_learn and saves stdout and model to given directory
#5. runs svm_classify and saves stdout and predictions to directory
#6. calculates accuracy for both ordered and random selection
#7. prints accuracy to stdout

import sys
import os 

ord_file_maker = sys.argv[1]
rand_file_maker = sys.argv[2]
model_file = sys.argv[3]
directory = sys.argv[4]
train_file = sys.argv[5]
test_file = sys.argv[6]
learn_file = sys.argv[7]
classify_file = sys.argv[8]

num = 58
weighted = []
rand = []


for m in range(2, num):
  print(".", end="")
  #weighted test first
  #make new file names for weighted feature selection
  new_train = directory + "ordered/" + str(m) + "_train"
  new_test = directory + "ordered/" + str(m) + "_test"
  new_learn_output = directory + "ordered/" + str(m) + "_train_acc"
  new_classify_output = directory + "ordered/" + str(m) + "_test_acc"
  new_model = directory + "ordered/" + str(m) + "_model"
  new_predictions = directory + "ordered/" + str(m) + "_predictions"

  #call the order file maker to make new training and testing
  string = "python3 " + ord_file_maker + " " + model_file + " " + str(m) + " " + train_file + " " + test_file + " " + new_train + " " + new_test
  os.system(string)

  #call learning process
  os.system("./" + learn_file + " " + new_train + " " + new_model + " > " + new_learn_output)

  # call classify
  os.system("./" + classify_file + " " + new_test + " " + new_model + " " + new_predictions + " > " + new_classify_output)

  #open the test accuracy file, get lines, close
  text_file = open(new_classify_output)
  lines = text_file.readlines()
  text_file.close()

  #get the accuracy
  start_idx = lines[3].find(":") + 2
  end_idx = lines[3].find("%")
  accuracy = float(lines[3][start_idx:end_idx])
  weighted.append(accuracy)
  


  #now do the random feature test
  #make new file names for random
  new_train = directory + "random/" + str(m) + "_train"
  new_test = directory + "random/" + str(m) + "_test"
  new_learn_output = directory + "random/" + str(m) + "_train_acc"
  new_classify_output = directory + "random/" + str(m) + "_test_acc"
  new_model = directory + "random/" + str(m) + "_model"
  new_predictions = directory + "random/" + str(m) + "_predictions"

  #call the rand file maker to make new training and testing
  string = "python3 " + rand_file_maker + " " + str(m) + " " + train_file + " " + test_file + " " + new_train + " " + new_test
  os.system(string)

  #call learning process
  os.system("./" + learn_file + " " + new_train + " " + new_model + " > " + new_learn_output)

  # call classify
  os.system("./" + classify_file + " " + new_test + " " + new_model + " " + new_predictions + " > " + new_classify_output)

  #open the test accuracy file, get lines, close
  text_file = open(new_classify_output)
  lines = text_file.readlines()
  text_file.close()

  #get the accuracy
  start_idx = lines[3].find(":") + 2
  end_idx = lines[3].find("%")
  accuracy = float(lines[3][start_idx:end_idx])
  rand.append(accuracy)

print()
print("Accuracy\n...........")
print("Weighted: ")
for i in range(len(weighted)):
  print(weighted[i], end=" ")
print()
print("Random: ")
for i in range(len(rand)):
  print(rand[i], end=" ")
print()

