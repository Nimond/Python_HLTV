import urllib.request
from bs4 import BeautifulSoup

pages = 0

teams = [] #names of teams
wons = []  #numbers of won of the teams[i] team
loses = [] #numbers of loses


def get_html(url):
    _request = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    response = urllib.request.urlopen(_request)
    return response.read()

def get_pages(html): #getting the number of pages with matches
    soup = BeautifulSoup(html)

    max_pages = soup.find('span', class_='pagination-data')
    max_pages_text = max_pages.text

    return int(max_pages_text[-6:]) - int(max_pages_text[-6:])%100 # '1 - 100 of 29107' we will get 29100 

def parse(html):
    soup = BeautifulSoup(html)

    scores_nf = soup.find_all('td', class_='result-score')   # no-filtred scores in case of tie
    scores = []                                              # list of scores without ties
    team_won = soup.find_all('div', class_='team team-won')  # list of winners names
    team_lose = soup.find_all('div', class_='team ')

    #start filtring ties
    for k in range(len(scores_nf)):
        if (len(scores_nf[k].text) == 7 and scores_nf[k].text[-2:] == scores_nf[k].text[:2]) or (len(scores_nf[k].text) == 5 and scores_nf[k].text[-1:] == scores_nf[k].text[:1]): #tie can be '1 : 1'(len 5) and '15 : 15'(len 7)
            team_lose.pop(k)    # very clever(not) pidarasu in hltv named <div> class for losers and tiers the same: 'team ' so we pop 2 elements from k place (where the tie found) 
            team_lose.pop(k+1)
        else:
            scores.append(scores_nf[k])
    #stop


    for i in range(len(team_won)):
        try:
            win = teams.index(team_won[i].text) # if we find the name of team we only ++ their wons, else we do new team with 1 won and 0 loses
        except ValueError:
            teams.append(team_won[i].text)
            wons.append(1)
            loses.append(0)
        else:
            wons[win]+=1
            
        try:
            lose = teams.index(team_lose[i].text) # the same of wons
        except ValueError:
            teams.append(team_lose[i].text)
            wons.append(0)
            loses.append(1)
        else:
            loses[lose]+=1


while pages<=get_pages(get_html('https://www.hltv.org/results?offset=0')): 
    parse(get_html('https://www.hltv.org/results?offset='+str(pages)))
    pages+=100

for i in range(len(teams)):
    print(teams[i]+' '+str(wons[i])+' '+str(loses[i]))
