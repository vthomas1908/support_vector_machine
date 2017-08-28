import sys
import os
import math

# call: python3 roc_finder.py <predictions file> <model file>
# model file is generated from svm_learn

#This application prints to stdout the TPR and FPR for
#the given prediction and model files derived from svm_light package

#parameters:
#[1]: predictions file
#[2]: vectors file

#vars
thresh = .45775889
bias = 1 - thresh

#get the files
prediction_file = sys.argv[1]
actuals_file = sys.argv[2]

#make sure files exist
if not os.path.exists(prediction_file):
  print(preiction_file, " does not exist")
  sys.exit(0)
if not os.path.exists(actuals_file):
  print(actuals_file, " does not exist")
  sys.exit(0)

# start with prediction file
text_file = open(prediction_file)

# create a list of the lines
predictions = text_file.readlines()

# close file
text_file.close()

# and the actual data
text_file = open(actuals_file)
actual_lines = text_file.readlines()
text_file.close()

# format list of predictions including
# removing the original bias
for i in range(len(predictions)):
  predictions[i] = (float(predictions[i]) - bias)

# format list of actual classes
actuals = []
for line in actual_lines:
  actuals.append(line.split(" "))

for i in range(len(actuals)):
  actuals[i] = float(actuals[i][0])

# find the min and max
max_val = max(predictions)
min_val = min(predictions)
step = (max_val - min_val)/200
b = min_val
# for 200 evenly spaced thresholds
# get plot points for ROC curve
tp = []
tn = []
fp = []
fn = []
tpr = []
fpr = []
for x in range(200):
  #initialize t/f pos and neg count
  tp.append(0)
  tn.append(0)
  fp.append(0)
  fn.append(0)
  tpr.append(0)
  fpr.append(0)
  # add bias to the classifier calc
  for j in range(len(predictions)):
    if x < 1:
      predictions[j] = predictions[j] + b
    else:
      predictions[j] = predictions[j] + step
    # increment appropriate counter
    if predictions[j] > 0:
      if actuals[j] > 0:
        tp[x] += 1
      else:
        fp[x] += 1
    else:
      if actuals[j] < 0:
        tn[x] += 1
      else:
        fn[x] += 1
    #calc TPR and FPR for this thresh
    if tp[x] != 0:
      tpr[x] = tp[x]/(tp[x] + fn[x])
    if fp[x] != 0:
      fpr[x] = fp[x]/(tn[x] + fp[x])

print("TPR: " + str(tpr))
print("FPR: " + str(fpr))
