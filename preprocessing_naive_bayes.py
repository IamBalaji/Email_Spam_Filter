import glob
import numpy as np
from sklearn import metrics
words = []
for i in range(10):
	folder_name = "part"+str(i+1)
	# print folder_name
	for mail in glob.glob(folder_name+"/*.txt"):
		# print mail
		with open(mail, 'r') as fin:
			pp = fin.read().split("\n")
			# print pp
			# exit()
			del pp[1]
			del pp[-1]
			string = pp[0].split(": ")[1:]
			del pp[0]
			if(not(len(string) == 1 and string.count('') == 1)):
				pp.insert(0,string[0])
			# words = pp[0].split(" ")
			# for i in pp[1].split(" "):
			# 	words.append(i)
			# print words
			for elem in pp:
				lst = elem.split(" ")
				for i in lst:
					words.append(int(i))
					
			# print Vocabulary
			# temp = set(words)
			# for i in words:
			# 	if(i in temp):
			# 		continue
			# 	else:
			# 		print "not found"
			# print "done checking"
distinct_words = set(words)
c = 0
Vocabulary = list(distinct_words)
print len(Vocabulary)

#process train data
TrainD = []
TrainL = []
TestD = []
TestL = []
Number_of_docs = 0
for i in range(8):
	folder_name = "part"+str(i+1)
	print folder_name
	cnt  = 0
	for mail in glob.glob(folder_name+"/*.txt"):
		cnt = cnt +1
		Number_of_docs = Number_of_docs + 1;
		words = []
		with open(mail, 'r') as fin:
			pp = fin.read().split("\n")
			del pp[1]
			del pp[-1]
			string = pp[0].split(": ")[1:]
			del pp[0]
			if(not(len(string) == 1 and string.count('') == 1)):
				pp.insert(0,string[0])
			for elem in pp:
				lst = elem.split(" ")
				for i in lst:
					words.append(int(i))
		Frequency = []
		for i in Vocabulary:
			Frequency.append(words.count(i))
		TrainD.append(Frequency)
		if("spmsg" in mail):
			TrainL.append(0)
		else:
			TrainL.append(1)
	print len(TrainD), cnt
	print len(TrainL)
	# exit(0)
print TrainL
# exit(0)
for i in range(2):
	folder_name = "part"+str(i+9)
	print folder_name
	cnt  = 0
	for mail in glob.glob(folder_name+"/*.txt"):
		words = []
		cnt = cnt + 1
		with open(mail, 'r') as fin:
			pp = fin.read().split("\n")
			del pp[1]
			del pp[-1]
			string = pp[0].split(": ")[1:]
			del pp[0]
			if(not(len(string) == 1 and string.count('') == 1)):
				pp.insert(0,string[0])
			for elem in pp:
				lst = elem.split(" ")
				for i in lst:
					words.append(int(i))
		Frequency = []
		for i in Vocabulary:
			Frequency.append(words.count(i))
		TestD.append(Frequency)
		if("spmsg" in mail):
			TestL.append(0)
		else:
			TestL.append(1)
	print len(TestD), cnt
	print len(TestL)
print TestL
print len(TrainD), len(TrainD[0]), len(TrainL)

print len(TestD), len(TestD[0]), len(TestL)

Classes = [0,1]
TrainD = np.array(TrainD)
# TrainL = np.array(TrainL)
TestD = np.array(TestD)
# TestL = np.array(TestL)
Prior = []
Conditional_probs = []
for cls in Classes:
	Class_probs = []
	p = TrainL.count(cls) / float(Number_of_docs)
	Prior.append(p)
	Tct = []
	x = 0
	for index in range(len(Vocabulary)):
		for lbl in range(len(TrainD)):
			if(TrainL[lbl] == cls):
				x = x + TrainD[lbl][index]
		x = x+1
		Tct.append(x)
	Tct = np.array(Tct)
	for index in range(len(Vocabulary)):
		Class_probs.append((Tct[index])/float(Tct.sum()))
	Conditional_probs.append(Class_probs)
# Testing..
c = 0
result  = []
for test_case in TestD:
	Score = []
	for cls in Classes:
		clas_score = np.log10(Prior[cls])
		for index in range(len(test_case)):
			if(test_case[index] != 0):
				clas_score = clas_score + np.log10(Conditional_probs[cls][index])
		Score.append(clas_score)
	if(Score[0] > Score[1]):
		result.append(0)
	else:
		result.append(1)

	# print "True label is " + str(TestL[c])
	c = c+1

print TestL
print result
print metrics.precision_score(np.array(TestL),result, average = 'binary')
print metrics.recall_score(np.array(TestL),result, average = 'binary')
print metrics.f1_score(np.array(TestL), np.array(result), average = 'binary')