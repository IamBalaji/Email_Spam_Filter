import glob
import numpy as np
from sklearn import metrics, naive_bayes
words = []
for i in range(10):
	folder_name = "part"+str(i+1)
	# print folder_name
	for mail in glob.glob(folder_name+"/*.txt"):
		# print mail
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
distinct_words = set(words)
c = 0
Vocabulary = list(distinct_words)
print len(Vocabulary)

#process train data

folders = [1,2,3,4,5,6,7,8,9,10]
precision = []
recall = []
f_measure = []
for count in range(5):
	TrainD = []
	TrainL = []
	TestD = []
	TestL = []
	print "Round "+str(count)
	current_folder = np.roll(folders,count*2)
	train_folders = current_folder[:8]
	test_folders = current_folder[8:]
	print train_folders
	print test_folders
	Number_of_docs = 0
	for i in train_folders:
		folder_name = "part"+str(i)
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
				freq = words.count(i)
				if(freq == 0):
					Frequency.append(0)
				else:
					Frequency.append(1)
			TrainD.append(Frequency)
			if("spmsg" in mail):
				TrainL.append(0)
			else:
				TrainL.append(1)
		print len(TrainD), cnt
		print len(TrainL)
	for i in test_folders:
		folder_name = "part"+str(i)
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
				freq = words.count(i)
				if(freq == 0):
					Frequency.append(0)
				else:
					Frequency.append(1)
			TestD.append(Frequency)
			if("spmsg" in mail):
				TestL.append(0)
			else:
				TestL.append(1)
		print len(TestD), cnt
		print len(TestL)

	print len(TrainD), len(TrainD[0]), len(TrainL)

	print len(TestD), len(TestD[0]), len(TestL)

	TrainD = np.array(TrainD)
	TrainL = np.array(TrainL)
	TestD = np.array(TestD)
	TestL = np.array(TestL)
	BernoulNB = naive_bayes.BernoulliNB(binarize = None)

	BernoulNB.fit(TrainD,TrainL)

	result  = BernoulNB.predict(TestD)
	
	x = metrics.precision_score(np.array(TestL),result, average = None)
	y = metrics.recall_score(np.array(TestL),result, average = None)
	z = metrics.f1_score(np.array(TestL), np.array(result), average = None)
	precision.append(x)
	recall.append(y)
	f_measure.append(z)
	print x, y, z

	count = count +1

precision = np.array(precision)
recall = np.array(recall)
f_measure = np.array(f_measure)

print "precision: "+str(precision[:,0:1].sum()/5)+"   "+str(precision[:,1:2].sum()/5)
print "recall: "+str(recall[:,0:1].sum()/5)+"   "+str(recall[:,1:2].sum()/5)
print "f_measure: "+str(f_measure[:,0:1].sum()/5)+"   "+str(f_measure[:,1:2].sum()/5)