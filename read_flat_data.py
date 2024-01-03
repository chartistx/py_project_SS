import requests
from bs4 import BeautifulSoup
import re
import time
import pandas as pd

def get_flat_data(flat,region):
    specs = [region]
    for spec in flat.find_all('td',{'class':'msga2-o pp6'}):
        if spec.find("br"):#Fro address regian an adrees had <br> as separator, thus no space
            spec.find("br").replace_with(" ")# replace with space
        specs.append(spec.get_text())
    flat_data.append(specs)
def get_flats_from_region(link,region):
    page=1
    while True:
        response = requests.get('https://www.ss.lv/'+link+'all/page'+str(page)+'.html', allow_redirects=False)

        if response.status_code != 200:
            break
        print(region, page)
        #get flat from page
        page_data = BeautifulSoup(response.content, features="html.parser")
        page_regex = re.compile('.*tr_.*')  # izmantojam regex recomplile lai varētu meklēt pēc daļēja satura atbilstības
        for each_flat in page_data.find_all("tr", {"id": page_regex}):
            id = each_flat.get("id")
            if id == "tr_bnr_712":
                break
            get_flat_data(each_flat,region)
        page+=1
        time.sleep(0.25)#to not overload web server time delay is used before next request


#atrodam visus reģionus un linkus uz tiem
response = requests.get('https://www.ss.lv/lv/real-estate/flats/')
soup = BeautifulSoup(response.content,features="html.parser")

flat_data=[]
regex = re.compile('.*ahc_.*')#izmantojam regex recomplile lai varētu meklēt pēc daļēja satura atbilstības
for EachPart in soup.find_all("a", {"id" : regex}):
    link   = EachPart.get('href')
    region = EachPart.get_text()
    if link == '/lv/real-estate/flats/other/' or link == '/lv/real-estate/flats/flats-abroad-latvia/':
        continue
    get_flats_from_region(link,region)

#export data to csv
df = pd.DataFrame(flat_data,columns=['Region','Area','Nr of rooms','m2','Floor','House type','Price'])
df.to_csv('ss_flat_data.csv')



