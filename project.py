from enum import Flag
from typing import DefaultDict
import pandas as pd
import numpy as np
import re
import random
import math



DictPre = dict()
def CleanTweets(tweet):
    tweet = tweet.lower() #lower case each chacter
    tweet = re.sub(r'@[a-z0-9+]', '', tweet) #remove mention
    tweet = re.sub(r'#', '', tweet) #remove hashtag
    tweet = re.sub(r'http\S+', '', tweet) #remove url
    tweet = re.sub(r'www\S+', '', tweet) #remove url
    tweet = re.sub(r'[^\w\s]', '', tweet) #removing punctuations
    tweet = re.sub(' +', ' ', tweet) #trim extra spaces
    tweet = tweet.strip('\n') #remove \n from sentence 
    # remove colons from the end of the sentences (if any) after removing url
    tweet = tweet.strip()
    if len(tweet) > 0:
        if tweet[len(tweet) - 1] == ':':
            tweet = tweet[:len(tweet) - 1]
    return tweet

def Preprocessing(Input):
    Input = open(Input)
    Tweets = []
    for tweet in Input:
        cnt = 0
        #removing TimeStamp & ID
        for i in range(len(tweet)):
            if cnt == 2:
                tweet = tweet[i : ]
                break
            if tweet[i] == '|':
                cnt += 1
        T = CleanTweets(tweet)
        Tweets.append(T)
    return Tweets


def JaccardDistance(T1, T2):
    T1 = T1.split()
    T2 = T2.split()
    ST1 = set(T1).union(set(T2))
    ST2 = set(T1).intersection(set(T2))
    Union = len(ST1)
    Intersect = len(ST2)
    Dist = 1 - (Intersect / Union)
    return Dist       
        
        
def Clustering(Tweets, No_Clusters, centroids):
    Clusters = dict()
    N = len(Tweets)
    # Assign Centroids
    for j in range(len(centroids)):
        Clusters[j] = []

    for i in range(0, N):
        minDist = math.inf
        cID = -1
        for j in range(0,len(centroids)):
            dist = JaccardDistance(Tweets[i], centroids[j])
            if Tweets[i] == centroids[j]:
                cID = j
                minDist = 0
                break
            if dist < minDist:
                minDist = dist
                cID = j
        if minDist == 1:
            cID = random.randint(0, len(centroids) - 1)
        Clusters[cID].append([Tweets[i], minDist])
        if cID in DictPre:
            DictPre[cID] = centroids[cID] 
        else:
            DictPre[cID] = ""
    return Clusters


def UpdateClusters(Clusters):
    NewCentroids = []
    for idx in range(len(Clusters)):
        minDist = math.inf
        centerTweet = ''
        for i in range(0, len(Clusters[idx])):
            sumDist = 0
            for j in range(0, len(Clusters[idx])):   
                dist = JaccardDistance(Clusters[idx][i][0], Clusters[idx][j][0])
                sumDist += dist

            if sumDist < minDist:
                minDist = sumDist
                centerTweet = i
        x = Clusters[idx][centerTweet][0]             
        NewCentroids.append(Clusters[idx][centerTweet][0])

    return NewCentroids


def isConverged(old, new):
    if len(old) != len(new):
        return False
    for i in range(len(new)):
         if new[i] != old[i]:
                return False
    
    return True

def CalcSSE(Clusters):
    SSE = 0
    for CID in range(len(Clusters)):
        for T in range(len(Clusters[CID])):
            dist = Clusters[CID][T][1]
            SSE = SSE + (dist * dist)
    return SSE

def Kmeans(Tweets, No_Clusters, iterations):
    centroids = random.sample(Tweets, No_Clusters)
    old = []
    
    it = 0
    CS = dict()
    while((isConverged(old, centroids)) == False and it < iterations):
        print('it: ' + str(it))
        CS = Clustering(Tweets, No_Clusters, centroids)
        old = centroids
        centroids = UpdateClusters(CS)
        it = it + 1

    SSE = CalcSSE(CS)
    return SSE, CS


def Output(N, Tweets, E):
    OutputFile = []
    s = "Experiment No. " +  str(E)
    OutputFile.append(s)
    OutputFile.append("\n")
    SSE, Clust = Kmeans(Tweets, N, 50)
    s = "Value of K: " + str(N)
    #print(s)
    OutputFile.append(s)
    OutputFile.append("\n")
    s = "SSE: " + str(SSE)
    #print(s)
    OutputFile.append(s)
    OutputFile.append("\n")
    s = "Size of Each Cluster: "
    #print(s)
    OutputFile.append(s)
    OutputFile.append("\n")
    for i in Clust:
        x = i + 1
        s = str(x) + ": " + str(len(Clust[i])) + " Tweets"
        #print(s)
        OutputFile.append(s)
        OutputFile.append("\n")


    
    return Clust, OutputFile

def PrintTweets(Clusters, E):
    OutputTweets = []
    s = "Experiment No. " +  str(E)
    OutputTweets.append(s)
    OutputTweets.append("\n")
    for i in range(len(Clusters)):
        x = i + 1
        s = "Tweets of Cluster No. " +  str(x) + ": "
        OutputTweets.append(s)
        OutputTweets.append("\n")
        for j in range(len(Clusters[i])):
            y = j + 1
            s = str(y) + ": " + Clusters[i][j][0]
            OutputTweets.append(s)
            OutputTweets.append("\n")
    return OutputTweets

