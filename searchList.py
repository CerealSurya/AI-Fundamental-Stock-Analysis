from bs4 import BeautifulSoup  
from googlesearch import search
import pandas as pd
import requests
from textblob import TextBlob
# import nltk
# nltk.download('punkt')


df = pd.read_excel("23-24 Competition Stock List-FINAL.xlsx", usecols=["Company Name", "Ticker", "Exchange", "GICS Sector", "GICS Industry Group", "GICS Industry", "GICS Sub-Industry"])
# ^^^ Read in stock list as pandas dataframe
query = input("Enter paramater: ") #Get the parameter from user

feedback = []
def urlFunc(url):
    r = requests.get(url, timeout=25) #Pull html content from url
    score = 0
    counter = 0
    if int(r.status_code) == 200:
        soup = BeautifulSoup(r.text,'lxml') #Get the text content from the html pulled
        content = soup.body.get_text(' ', strip=True)
        sesame = TextBlob(content) #turn content into textblob obj
        for sentence in sesame.sentences:
            score += sentence.sentiment.polarity #run sentiment analysis on each sentence
            counter += 1
    return [score, counter]

# def urlFunc(r, *args, **kwargs):
    # score = 0
    # counter = 0
    # if int(r.status_code) == 200:
    #     soup = BeautifulSoup(r.text,'lxml')
    #     content = soup.body.get_text(' ', strip=True)
    #     sesame = TextBlob(content)
    #     for sentence in sesame.sentences:
    #         score += sentence.sentiment.polarity
    #         counter += 1
    # thread.set()
    # return [score, counter]

for name in df.loc[:, "Company Name"]:
    urls = []
    score = 0
    counter = 0

    #TODO: add timeout for the search
    for j in search(f"{name} {query} news", tld="co.in", num=3, stop=3, pause=2): #Ping google api for top 3 urls for our query
        urls.append(j)

    for url in urls:
        try:
            # requests.get(url, hooks={'response': urlfunc}) <--- Used for async
            l = urlFunc(url)
            score += l[0]
            counter += l[1]
        except:
            print(f"Error occured on {name} on {url}") #this occurs when url request for html content was unable to go through
    if counter != 0:
        print(name, "   ", score / counter)
        feedback.append(score / counter) #append sentiment score average to feedback list
    else:
        feedback.append("N/A")

with open(f'Stocklist_search_{query}.txt', 'w') as f: #Write the score avg to txt file
    counter = 0
    for i in feedback:
        f.write(f'{df.loc[counter]["Company Name"]}: {i}\n')
        counter += 1