# To add a new cell, type '# %%'
# To add a new markdown cell, type '# %% [markdown]'
# %%
from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
import pandas as pd
import os
import datetime 
import time
from dateutil.relativedelta import relativedelta
import re


# %%
def split_delimeter(word):
#     "Home Team","Home Win","Draw","away Team","Away win",'site'
    delimiters = " - ", " v ",'\n'
    regexPattern = '|'.join(map(re.escape, delimiters))
    wordArray = re.split(regexPattern, word)  
    result = [a for a in wordArray if len(str(a).replace('  ','').lstrip()) > 1 ]
    matchOdd = list()
    matchOdd.append(sanitize_name(result[6]))
    matchOdd.append(result[7])
    matchOdd.append(result[9])
    matchOdd.append(sanitize_name(result[-3]))
    matchOdd.append(result[-2])
    matchOdd.append('betika')
    return matchOdd
        


# %%
def sanitize_name(name):
    name = name.lower()
    name = name.replace('fc','')
    name = name.replace('man ','manchester ')
    name = name.replace('club','')
    name = name.replace('cf','')
    name = name.replace(' sc','')
    name = name.replace('1.','')
    name = name.replace('.',' ')
    name = name.replace('  ',' ')
    name = name.replace("'", " ")
    name = name.replace("utd", "united")
    return name.strip()
def remove_egames(name):
    if name.find("(") > -1:
        return 1
    return int(-1)


# %%
def get_betika(filename="betika.csv",log="logs/log_betika.txt"):
    
    if(os.path.exists("data/"+filename)):
        f = open(log, "r")
        logContent = f.read()
        start_dt = datetime.datetime.strptime(logContent.split("\t")[0], '%c')
        end_dt = datetime.datetime.now()
        timedelta_obj = relativedelta(end_dt,start_dt)
        if(timedelta_obj.days < 12):
            df = pd.read_csv ("data/"+filename,sep='\t')
            return df.drop(["Unnamed: 0"],axis=1)
        else:
            with open(log, "r+") as f:
                old = f.read() # read everything in the file
                f.seek(0) # rewind
                start =datetime.datetime.now()
                f.write(start.strftime("%c")+"\tfetch\n")
    
    print("fetching odds from Betika...")
    driver = webdriver.Chrome(executable_path=r"C:/chromeDriver/chromedriver.exe")
    driver.get("https://www.betika.com/")
    content = driver.page_source
    soup = BeautifulSoup(content,'html.parser')
    odd_div = soup.find_all(attrs={"class": "home__matches__match"})
    odds= list()
    
    for odd in odd_div:
        odds_arr = split_delimeter(odd.text) ;
        odds.append(odds_arr)
        continue
    df_betika = pd.DataFrame(np.array(odds).reshape(np.array(odds).shape[0],6),columns=['Home Team','Home Win','Draw','Away Team','Away Win','site']) 
    df_betika.to_csv("data/"+filename,sep='\t', encoding='utf-8')
    f = open(log, "w")
    start =datetime.datetime.now()
    f.write(start.strftime("%c")+"\tfetch\n")
    f.close()
    return df_betika


# %%
def get_mbet(filename="mbet.csv",log="logs/log_mbet.txt"):
    
    if(os.path.exists("data/"+filename)):
        f = open(log, "r")
        logContent = f.read()
        start_dt = datetime.datetime.strptime(logContent.split("\t")[0], '%c')
        end_dt = datetime.datetime.now()
        timedelta_obj = relativedelta(end_dt,start_dt)
        if(timedelta_obj.days < 12):
            df = pd.read_csv ("data/"+filename,sep='\t')
            return df.drop(["Unnamed: 0"],axis=1)
        else:
            with open(log, "r+") as f:
                old = f.read() # read everything in the file
                f.seek(0) # rewind
                start =datetime.datetime.now()
                f.write(start.strftime("%c")+"\tfetch\n")
    
    print("fetching odds from mbet...")
    driver = webdriver.Chrome(executable_path=r"C:/chromeDriver/chromedriver.exe")
    driver.get('https://m-bet.co.ke/ke')
    elementsList = driver.find_elements_by_css_selector('.fixture-items-wrapper')
    odds = list()
    print("Preparing data",end="")
    for i in  range(len(elementsList)):
        print('.',end='')
        elements = elementsList[i].text.split("\n")
        date = elements[0]
        elements.remove(date)

        for iter in range(int(len(elements)/ 10)):
            matchList = list()
            match = elements[iter * 10 : (iter * 10) + 10 ]
            matchList.append(sanitize_name(match[0].split( "VS. ")[0]))
            matchList.append(sanitize_name(match[0].split( "VS. ")[1]))
            matchList.append(match[6])
            matchList.append(match[7])
            matchList.append(match[8])
            matchList.append('mbet')
            odds.append(matchList)
    df = pd.DataFrame(odds,columns=['Home Team','Away Team','Home Win','Draw','Away Win','site'])
    df.to_csv("data/"+filename,sep='\t', encoding='utf-8')
    f = open(log, "w")
    start =datetime.datetime.now()
    f.write(start.strftime("%c")+"\tfetch\n")
    f.close()
    return df


# %%
def get_mozzat(filename="mozzat.csv",log="logs/log_mozzat.txt"):
    if(os.path.exists("data/"+filename)):
        f = open(log, "r")
        logContent = f.read()
        start_dt = datetime.datetime.strptime(logContent.split("\t")[0], '%c')
        end_dt = datetime.datetime.now()
        timedelta_obj = relativedelta(end_dt,start_dt)
        if(timedelta_obj.days < 12):
            df = pd.read_csv ("data/"+filename,sep='\t')
            return df.drop(["Unnamed: 0"],axis=1)
        else:
            with open(log, "r+") as f:
                old = f.read() # read everything in the file
                f.seek(0) # rewind
                start =datetime.datetime.now()
                f.write(start.strftime("%c")+"\tfetch\n")
                
                        
    print("fetching odds from mozzat...")
    driver = webdriver.Chrome(executable_path=r"C:/chromeDriver/chromedriver.exe")
    driver.get("https://www.mozzartbet.co.ke/en#/")
    elements = driver.find_elements_by_css_selector('.bettingMatchRow')
    odds = list()
    print("Preparing data",end="")
    for el in elements:
        print('.',end='')
        match = el.text.split("\n")
        match.append('mozzat')
        match[1] = sanitize_name(match[1])
        match[2] = sanitize_name(match[2])
        odds.append(match)
    df = pd.DataFrame(odds,columns=["Time",'Home Team','Away Team','Home Win','Draw','Away Win','site'])
    df.to_csv("data/"+filename,sep='\t', encoding='utf-8')
    f = open(log, "w")
    start =datetime.datetime.now()
    f.write(start.strftime("%c")+"\tfetch\n")
    f.close()
    return df.drop(['Time'],axis=1,inplace=False)


# %%
def get_betway(filename="betway.csv",log="logs/log_betway.txt"):
    if(os.path.exists("data/"+filename)):
        f = open(log, "r")
        logContent = f.read()
        start_dt = datetime.datetime.strptime(logContent.split("\t")[0], '%c')
        end_dt = datetime.datetime.now()
        timedelta_obj = relativedelta(end_dt,start_dt)
        if(timedelta_obj.days < 12):
            df = pd.read_csv ("data/"+filename,sep='\t')
            return df.drop(["Unnamed: 0"],axis=1)
        else:
            with open(log, "r+") as f:
                old = f.read() # read everything in the file
                f.seek(0) # rewind
                start =datetime.datetime.now()
                f.write(start.strftime("%c")+"\tfetch\n")
                
                        
    print("fetching odds from Betway...")
    driver = webdriver.Chrome(executable_path=r"C:/chromeDriver/chromedriver.exe")
    driver.get("https://www.betway.co.ke/")
    elements = driver.find_elements_by_css_selector('.outcomes')
    odds = list()
    for els in elements:
        matchList = list()

        match = els.text.split('\n')
        if(len(match) > 1):
            matchList.append(sanitize_name(match[0]))
            matchList.append(sanitize_name(match[-2]))
            matchList.append(match[1])
            matchList.append(match[3])
            matchList.append(match[-1])
            matchList.append('betway')
            odds.append(matchList)
        else:
            continue
    df= pd.DataFrame(odds,columns=['Home Team','Away Team','Home Win','Draw','Away Win','site'])  
    df.to_csv("data/"+filename,sep='\t', encoding='utf-8')
    f = open(log, "w")
    start =datetime.datetime.now()
    f.write(start.strftime("%c")+"\tfetch\n")
    f.close()
    return df


# %%
def get_odiBet(filename="odibet.csv",log="logs/log_odibet.txt"):
    if(os.path.exists("data/"+filename)):
        f = open(log, "r")
        logContent = f.read()
        start_dt = datetime.datetime.strptime(logContent.split("\t")[0], '%c')
        end_dt = datetime.datetime.now()
        timedelta_obj = relativedelta(end_dt,start_dt)
        if(timedelta_obj.days < 12):
            df = pd.read_csv ("data/"+filename,sep='\t')
            return df.drop(["Unnamed: 0"],axis=1)
        else:
            with open(log, "r+") as f:
                old = f.read() # read everything in the file
                f.seek(0) # rewind
                start =datetime.datetime.now()
                f.write(start.strftime("%c")+"\tfetch\n")
    print("fetching odds from OdiBet...")
    driver = webdriver.Chrome(executable_path=r"C:/chromeDriver/chromedriver.exe")
    driver.get("https://odibets.com/")
    elementsList = driver.find_elements_by_css_selector('.l-events-games')
    
    odds = list()
    for i in range(len(elementsList)):
        
        matchOdds = elementsList[i].text.split('\n')
        matchOdds.remove(matchOdds[0])
        if(len(matchOdds) % 10 == 0 ):
             for iter in range(int((len(elementsList[i].text.split('\n'))-1) / 10)):
                matchList = list()
                match = matchOdds[iter * 10 : (iter *10) + 10]
                matchList.append(sanitize_name(match[0]))
                matchList.append(sanitize_name(match[1]))
                matchList.append(match[4])
                matchList.append(match[6])
                matchList.append(match[8])
                matchList.append('odiBet')
                odds.append(matchList) 
        elif (len(matchOdds) % 15 == 0 ):
            for iter in range(int((len(elementsList[i].text.split('\n'))-1) / 15)):
                matchList = list()
                match = matchOdds[iter * 15 : (iter *15) + 15]
                matchList.append(sanitize_name(match[0]))
                matchList.append(sanitize_name(match[1]))
                matchList.append(match[4])
                matchList.append(match[6])
                matchList.append(match[8])
                matchList.append('odiBet')
                odds.append(matchList)
        
          
    df = pd.DataFrame(odds,columns =['Home Team','Away Team','Home Win','Draw','Away Win','site'])
    df.drop_duplicates(keep='first',inplace=True)
    df.to_csv("data/"+filename,sep='\t', encoding='utf-8')
    f = open(log, "w")
    start =datetime.datetime.now()
    f.write(start.strftime("%c")+"\tfetch\n")
    f.close()
    return  df 

    
    


# %%
def abitrageCalculator(dataFrame):
    AbitrageBetSlip = list()
    final_df = dataFrame.sort_values(['Home Team','Away Team'],ascending= True)
    distinct = final_df['Home Team'].unique()
    for distinctVal in distinct:
        df = final_df[final_df['Home Team'] == distinctVal]
        mostWinOdd = df.loc[df['Home Win'].idxmax()]
        mostWinBook = mostWinOdd['site']
        mostDrawOdd = df.loc[df['Draw'].idxmax()]
        mostDrawBook = mostDrawOdd['site']
        mostLossOdd = df.loc[df['Away Win'].idxmax()]
        mostLossBook = mostLossOdd['site']
        
        inverseWinOdd= 1/float(mostWinOdd['Home Win']) 
        inverseDrawOdd = 1/float(mostWinOdd['Draw'])
        inverseLossOdd = 1/float(mostWinOdd['Away Win'])
        
        sumInverse = inverseWinOdd + inverseDrawOdd + inverseLossOdd
        estimatedProbWin = inverseWinOdd / sumInverse
        estimatedProbDraw = inverseDrawOdd / sumInverse
        estimatedProbLoss = inverseLossOdd / sumInverse
        
        fairOddWin = np.reciprocal(estimatedProbWin)
        fairOddDraw = np.reciprocal(estimatedProbDraw)
        fairOddLoss = np.reciprocal(estimatedProbLoss)
        
        AbitrageBet = list()
        AbitrageBet.append(distinctVal)
        AbitrageBet.append(mostWinOdd['Away Team'])
        AbitrageBet.append(np.float(mostWinOdd['Home Win']))
        AbitrageBet.append(np.float(mostWinOdd['Draw']))
        AbitrageBet.append(np.float(mostWinOdd['Away Win']))
        AbitrageBet.append(np.float(inverseWinOdd))
        AbitrageBet.append(np.float(inverseDrawOdd))
        AbitrageBet.append(np.float(inverseLossOdd))
        AbitrageBet.append(np.float(sumInverse))
        AbitrageBet.append(np.float(estimatedProbWin))
        AbitrageBet.append(np.float(estimatedProbDraw))
        AbitrageBet.append(np.float(estimatedProbLoss))
        AbitrageBet.append(np.float(estimatedProbLoss + estimatedProbDraw + estimatedProbWin))
        AbitrageBet.append(np.float(fairOddWin))
        AbitrageBet.append(np.float(fairOddDraw))
        AbitrageBet.append(np.float(fairOddLoss))    
        AbitrageBet.append(mostWinBook)
        AbitrageBet.append(mostDrawBook)
        AbitrageBet.append(mostLossBook)
        AbitrageBetSlip.append(AbitrageBet)
        
    columns = ['Home Team','Away Team','Win','Draw','loss','1/win','1/draw','1/loss','sum inverse','est Prob Win','est Prob Draw','est Prob Loss','Total est Prob','fair win','fair Draw','fair Loss','win Bookmaker','draw Bookmaker','loss Bookmaker']
    return pd.DataFrame(AbitrageBetSlip,columns = columns) 


# %%
def validate_step1(all_df,synony):
    distinct = all_df['Home Team'].unique()
    for distinctVal in distinct:
        feature = distinctVal
        delimiters = " ", ".","  "
        regexPattern = '|'.join(map(re.escape, delimiters))
        splitHomeName=re.split(regexPattern, distinctVal)
        for splitName in splitHomeName:
            if(len(splitName) >= 3):
                for distinctVal_2 in distinct:
                    if(distinctVal_2.strip().lower() == distinctVal.strip().lower()):
                        continue
                    feature_2 = distinctVal_2
                    if( distinctVal_2.lower().strip().find(splitName.lower().strip()) == -1):
                        continue

                    else:
                        if distinctVal in synony:
                            if feature_2 not in synony[feature]:
                                synony[feature].append(feature_2)

                        else:
                            synony[feature] = list()
                            synony[feature].append(feature_2)


# %%
def validate_step2(all_df,synony):
    synonyKeys = list(synony)
    for key in  list(synonyKeys):
        if key in synonyKeys:
            awayTeam = all_df[all_df['Home Team'] == key]['Away Team']
            for val in list(synony[key]):
                match = False
                keysplit = key.split(" ")
                valsplit = val.split(" ")

                if(len(keysplit) == 2 and len(valsplit) == 2 ):
                    if (valsplit[0][0:2] == keysplit[0][0:2] and valsplit[1].find(keysplit[1][0:3]) != -1) == False:
                        synony[key].remove(val)
                        continue

                delimiters = " ",".","-"
                regexPattern = '|'.join(map(re.escape, delimiters))
                awayTeamSplit = re.split(regexPattern, list(awayTeam)[0].lower().strip())
                synAwaySplit = re.split(regexPattern, list(all_df[all_df['Home Team'] == val]['Away Team'])[0].lower().strip())


                if len(awayTeamSplit) ==  1 and len(synAwaySplit) ==  1:
                    if awayTeamSplit[0].lower().strip() != synAwaySplit[0].lower().strip():
                        synony[key].remove(val)
                        continue
                    else:
                        match = (match | True )



                if len(awayTeamSplit) >  1 and len(synAwaySplit) ==  1:
                    match == False
                    for awySplit in awayTeamSplit:
                        if(len(awySplit)< 3):
                            continue
                        if awySplit.lower().strip() == synAwaySplit[0].lower().strip():
                            match = match | True
                    if match == False:
                        synony[key].remove(val)
                        continue



                if len(awayTeamSplit) ==  1 and len(synAwaySplit) >  1:
                    match == False
                    for awySplit in synAwaySplit:
                        if(len(awySplit)< 3):
                            continue
                        if awySplit.lower().strip() == awayTeamSplit[0].lower().strip():
                            match = match | True
                    if match == False:
                        synony[key].remove(val)
                        continue



                if len(awayTeamSplit) >  1 and len(synAwaySplit) >  1:

                        if len(awayTeamSplit) > len(synAwaySplit) :
                            minAwayName = synAwaySplit
                            maxAwayName = awayTeamSplit
                        else:
                            minAwayName = awayTeamSplit
                            maxAwayName = synAwaySplit

                        for min_iter in range(len(minAwayName)):
                            match = False
                            if(len(minAwayName[min_iter]) < 3):
                                continue
                            if(maxAwayName[min_iter].find(minAwayName[min_iter]) != -1):
                                match = (match | True)
                        if match == False:
                            synony[key].remove(val)
                            continue

                if val in synonyKeys :
                    synonyKeys.remove(val)
                    del synony[val]


# %%
def get_sportsOdds():
    odiBet = get_odiBet()

    betway = get_betway()

    mozzat = get_mozzat()
    mozzat['Home Win'] = mozzat['Home Win'].astype(float)
    mozzat['Draw'] = mozzat['Draw'].astype(float)
    mozzat['Away Win'] = mozzat['Away Win'].astype(float)
    mozzat[['Home Win','Draw','Away Win']].iloc[:].apply(lambda x : 1/x,axis=1)

    betika = get_betika()

    mbet = get_mbet()

    all_df = pd.concat([mbet,betika,betway,mozzat,odiBet],axis=0)
    all_df = all_df.reset_index().drop(['index'],axis=1)
    e_games = all_df.apply(lambda x : remove_egames(x['Away Team']),axis=1)
    indices = [i for i, x in enumerate(list(e_games)) if x == 1]
    all_df = all_df.drop(indices,axis=0)

    synony = dict()
    validate_step1(all_df,synony)
    validate_step2(all_df,synony)
    
    for key in synony.keys():
        for val in synony[key]:
            indices = list(all_df[all_df['Home Team'] == val].index.values)
            if len(indices) > 0:
                all_df.loc[indices,'Home Team'] = key
                
    return all_df


def entry_prog(amount:int):
    odds_df = get_sportsOdds()
    
    abitrage_df = abitrageCalculator(odds_df)
    
    oppor_df = abitrage_df[abitrage_df['sum inverse'] < 1]
    oppor_df["weight_win"]    = oppor_df['1/win'] / oppor_df['sum inverse']
    oppor_df["weight_draw"]   = oppor_df['1/draw'] / oppor_df['sum inverse']
    oppor_df["weight_loss"]   = oppor_df['1/loss'] / oppor_df['sum inverse']
    columns = ['Home Team','Away Team','Win','Draw','loss','win Bookmaker','draw Bookmaker','loss Bookmaker',"weight_win","weight_draw","weight_loss"]
    
    abbList = np.array(oppor_df[columns]).tolist()
    if len(abbList) > 0 :
        message = ''
        for abb in abbList:
            message += str(abb[0]).upper() + "- Win @ odds : "+ str(abb[2])+" stake : "+str(amount * abb[-3]) + " from "+str(abb[5])+"\n"
            message +=  "Draw".upper()+" @ odds: "+ str(abb[3])+" stake : "+str(amount * abb[-2]) + " from "+str(abb[6])+"\n"
            message += str(abb[1]).upper() + "- Win @ odds: "+ str(abb[4])+" stake : "+str(amount * abb[-1]) + " from "+str(abb[7])+"\n\n\n"
    else:
        message = "There aren't abitrage opportunities currently keep trying"
    return message




