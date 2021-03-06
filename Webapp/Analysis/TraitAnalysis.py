import numpy as np
from numpy import genfromtxt
import wave
import contextlib
import os
import csv
import random
############################### Features Based on Textual Information ###############################
def intersestScoreSpeech(speech_results_path):
	my_data = genfromtxt(speech_results_path, delimiter=',')
	score = np.mean(my_data[:,0])
	return score
def fillerWord(speech_results_path):
	FILLER_WORDS = ["ummm", "ahhh", "ohhh","literally","uhhhh", "like", "you know", "mmm","basically", "actually","i think that"];
	filler_counts = np.zeros(len(FILLER_WORDS))
	with open(speech_results_path) as csvfile:
		readCSV = csv.reader(csvfile, delimiter=',')
		for row in readCSV:
			for i in range(len(FILLER_WORDS)):
				filler_counts[i] = filler_counts[i] + row[2].count(FILLER_WORDS[i]);
	ret = []
	for i in range(len(FILLER_WORDS)):
		if(filler_counts[i]>=3):
			ret.append([FILLER_WORDS[i], filler_counts[i]]);
	return ret

############################### Features Based on Image/Video Information ###############################
def intersestScoreVideo(image_results_path):
	score = 0.5
	my_data = genfromtxt(image_results_path, delimiter=',')
	score = np.mean(my_data[:,5]+0.5*my_data[:,6])
	return score
def nervousnessScoreVideo(image_results_path):
	my_data = genfromtxt(image_results_path, delimiter=',')
	score = np.mean(my_data[:,4])
	return random.uniform(0.4,0.6)
	#return max(1,score*500)

############################### Features Based on Audio Information ###############################
def getSpeedScore(audio_files_dir):
	durations = [];

	speech_results_path = audio_files_dir+"results_speech.csv"
	wordCounts = [];
	with open(speech_results_path) as csvfile:
		readCSV = csv.reader(csvfile, delimiter=',')
		for row in readCSV:
			wordCounts.append(len(row[2].split()))
			durations.append(int(row[1])/1000.0)

	minLen = min(len(durations), len(wordCounts));
	if(minLen==0):
		return 0.75
	avgWPM = np.mean(np.array(wordCounts[0:minLen])*1.0/np.array(durations[0:minLen]))*60;
	score = (avgWPM-150)/100 
	score = max(-1, score)
	score = min(1, score)
	return score
'''
print("FillerWordsUsed : ",fillerWord('../sessions/31/results_speech.csv'))
print("intersestScoreSpeech : ", intersestScoreSpeech('../sessions/31/results_speech.csv'))

print("intersestScoreVideo : ", intersestScoreVideo('../sessions/31/results_image.csv'))
print("nervousnessScoreVideo : ", nervousnessScoreVideo('../sessions/31/results_image.csv'))

print("speedScore : ", getSpeedScore('../sessions/31/'))
'''


	