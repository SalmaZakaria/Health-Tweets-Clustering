import project as P

Experiments = 5


Input = input('Please Enter File URL: ')
NClusters = 3
Val = input('Do you want to change the initial number of Clusters ? Y/N ')
if Val == 'Y' or Val == 'y':
    NClusters = int(input('Enter Initial Number of Clusters ') )

Val2 = input('Do you want to change the number of Experiments ? Y/N ')
if Val2 == 'Y' or Val == 'y':
    Experiments = int(input('Enter Number of Experiments '))

for E in range(0, Experiments):
    OutputTxt = open('output.txt', 'a')
    OutputTweetsTxt = open('Tweets.txt', 'a')
    x = E + 1
    print("Experiment No. " +  str(x) + ": ")
    Tweets = P.Preprocessing(Input)
    Clust, OutputFile = P.Output(NClusters, Tweets, x)
    OutputTxt.writelines(OutputFile)
    #OutputTweets = P.PrintTweets(Clust, x)
    #OutputTweetsTxt.writelines(OutputTweets)
    NClusters = NClusters + 1