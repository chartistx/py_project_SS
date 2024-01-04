import requests
from bs4 import BeautifulSoup
import re
import time
import pandas as pd


def get_flat_data(flat,region):#function reads data about flat and stores it in a list.
    specs = [region]
    for spec in flat.find_all('td',{'class':'msga2-o pp6'}):
        if spec.find("br"):#area and adress had <br> as separator, thus no space
            spec.find("br").replace_with(" ")# replace with space
        specs.append(spec.get_text())
    flat_data.append(specs) #addin data from this flat to list with data from other flats


def get_flats_from_region(link,region):
    page=1
    while True:#while page exsist, read data
        response = requests.get('https://www.ss.lv/'+link+'all/page'+str(page)+'.html', allow_redirects=False)
        #check if page exist, request successful
        if response.status_code != 200:
            break
        print(region, page)#informative message to inform of scraping status
        #get flat from page
        page_data = BeautifulSoup(response.content, features="html.parser")
        page_regex = re.compile('.*tr_.*')  #using regex so that find on patial match can be used
        for each_flat in page_data.find_all("tr", {"id": page_regex}):
            id = each_flat.get("id")
            if id == "tr_bnr_712":
                break
            get_flat_data(each_flat,region)
        page+=1
        time.sleep(0.25)#to not overload web server time delay is used before next request


#find all regions
response = requests.get('https://www.ss.lv/lv/real-estate/flats/')
soup = BeautifulSoup(response.content,features="html.parser")

flat_data=[]#will hld all the scraped data about flats
regex = re.compile('.*ahc_.*') #using regex so that find on patial match can be used
for each_region in soup.find_all("a", {"id" : regex}):
    link   = each_region.get('href')
    region = each_region.get_text()
    if link == '/lv/real-estate/flats/other/' or link == '/lv/real-estate/flats/flats-abroad-latvia/':
        continue
    get_flats_from_region(link,region)

#export data to csv
df = pd.DataFrame(flat_data,columns=['Region','Area','Nr of rooms','m2','Floor','House type','Price'])
df.to_csv('ss_flat_data.csv')



