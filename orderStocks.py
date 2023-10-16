import pandas as pd
import re

#https://www.geeksforgeeks.org/python-program-to-find-the-highest-3-values-in-a-dictionary/

df = pd.read_excel("23-24 Competition Stock List-FINAL.xlsx", usecols=["Company Name", "Ticker", "Exchange", "GICS Sector", "GICS Industry Group", "GICS Industry", "GICS Sub-Industry"]) #need headers??
industries = ["energy", "materials", "industrials", "discretionary", "staples", "health", "financials", "tech", "communication", "utilities", "estate"]
energy = {}
materials = {}
industrials = {}
discretionary = {}
staples = {}
health = {}
financials = {}
tech = {}
communication = {}
utilities = {}
estate = {}
bigList = [energy, materials, industrials, discretionary, staples, health, financials, tech, communication, utilities, estate]
overallFive = []
with open("Stocklist_search_underserved communities.txt", "r") as f: #append the number to the according industry
    for line in f.readlines():
        regex = re.compile('-?\d+(.\d+)') # Does the string have: Negative sign or not + 1 or more digits followed by . followed by one or more digits
        ticker = ""
        #num = regex.match(line)
        num = "-10000" #set companies with no info at back
        for l in line.split():
            if l[0] != '0' and l[0] != '1' and l != "N/A": #Not a number
                ticker += l + " "
            elif l[0] == '0' or l[0] == '1':
                if l != "N/A":
                    num = l
    
        ticker = ticker[0:len(ticker)-2] #remove colon at end of string
        tickerPos = [i for i in range(len(df)) if df.loc[i]["Company Name"] == ticker]
        industry = df["GICS Sector"].values[tickerPos]
        if len(industry) != 0:
            industry = industry[0]
            if industry == "Energy":
                energy.update({ticker: num})
            elif industry == "Materials":
                materials.update({ticker: num})
            elif industry == "Industrials":
                industrials.update({ticker: num})
            elif industry == "Consumer Discretionary":
                discretionary.update({ticker: num})
            elif industry == "Consumer Staples":
                staples.update({ticker: num})
            elif industry == "Health Care":
                health.update({ticker: num})
            elif industry == "Financials":
                financials.update({ticker: num})
            elif industry == "Information Technology":
                tech.update({ticker: num})
            elif industry == "Communication Services":
                communication.update({ticker: num})
            elif industry == "Utilities":
                utilities.update({ticker: num})
            elif industry == "Real Estate":
                estate.update({ticker: num})

for l in bigList:
    daList = list(l.values())
    daList.sort(reverse=True)
    topFive = []
    for k in daList:
        if len(topFive) == 5:
            break #exit out because we only want the top five for each industry
        if k != "N/A":
            key = [key for key in l if l[key] == k]
            #print(key)
            contender = [key[0], k] #key value
            inp = input(contender[0] + " @ " + contender[1])
            if inp == "" and len(topFive) <=5:
                topFive.append(contender)
    overallFive.append(topFive)
    print(f"{industries[bigList.index(l)]} top five is {topFive}\n\n")

print(overallFive)