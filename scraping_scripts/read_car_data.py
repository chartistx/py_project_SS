import requests
from bs4 import BeautifulSoup
import re
import time
import pandas as pd
import os

#get path for data file
path_parent = os.path.join(os.getcwd(),os.pardir)

def get_car_data(car,manufacturer):#function reads data about car and stores it in a list.
    specs = [manufacturer]
    regex_specs = re.compile('.*msga2-.*')  # using regex so that find on patial match can be used
    for spec in car.find_all('td',{'class':regex_specs}):
        if spec.find("br"):#in category other manufacturers, manufacturer and model had no space
            spec.find("br").replace_with(" ")# replace with space
        specs.append(spec.get_text())
    car_data.append(specs) #addin data from this car to list with data from other cars

def get_cars_from_manufacturer(link,manufacturer):#parses though all pages in current manufacturer category and saves data abput all cars
    page=1
    while True:#while page exsist, read data
        response = requests.get('https://www.ss.lv/'+link+'all/page'+str(page)+'.html', allow_redirects=False)
        #check if page exist, request successful
        if response.status_code != 200:
            break
        print(manufacturer, page)#informative message to inform of scraping status
        #get car from page
        page_data = BeautifulSoup(response.content, features="html.parser")
        page_regex = re.compile('.*tr_.*')  #using regex so that find on patial match can be used
        for each_car in page_data.find_all("tr", {"id": page_regex}):
            id = each_car.get("id")
            if id == "tr_bnr_712":
                break
            get_car_data(each_car,manufacturer)

        page+=1
        time.sleep(0.25)#to not overload web server time delay is used before next request

#find all manufacturers
response = requests.get('https://www.ss.lv/lv/transport/cars/')
soup = BeautifulSoup(response.content,features="html.parser")

car_data=[]#will hold all the scraped data about cars
regex = re.compile('.*ahc_.*') #using regex so that find on patial match can be used
skip_list=['Citas markas','Ekskluzīvas automašīnas','Elektromobīļi', 'Retro automašīnas',
           'Sporta automašīnas', 'Tūningotas automašīnas', 'Vieglo auto maiņa',
           'Auto ar defektiem vai pēc avārijas', 'Auto remonts un apkalpošana',
           'Autoevakuācija', 'Autonoma', 'Piekabes un treileri',
           'Rezerves daļas', 'Riepas', 'Transports invalīdiem', 'Tūnings']#categories to skip
for each_manufacturer in soup.find_all("a", {"id" : regex}):
    link   = each_manufacturer.get('href')
    manufacturer = each_manufacturer.get_text()
    if manufacturer not in skip_list:
        get_cars_from_manufacturer(link, manufacturer)

#export data to csv
df = pd.DataFrame(car_data,columns=['Manufacturer','Model','Year','Motor Liters','Milage','Price'])
df.to_csv(path_parent+'\\data\\ss_car_data.csv')

print('Done')



