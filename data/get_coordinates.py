import pandas as pd
from geopy.geocoders import ArcGIS
import os


#get path for data file
path_parent = os.path.join(os.getcwd(),os.pardir)
path_file = path_parent+'\\data\\ss_flat_data.csv'

df=pd.read_csv(path_file)
df_mod = df
df_mod['Area'] = df['Area'].str.split().str.get(0)
df_mod['Area'] = df_mod['Area'].str.replace('Maskavas','Maskavas Priešpilsēta')
df_mod = df_mod.assign(Reg_area=df_mod['Region']+' '+df_mod['Area'])
df_mod = df_mod[df_mod['Area']!='-']
df_mod=df_mod.drop_duplicates('Area')

df_values = df_mod.values
df_list = df_values.tolist()
size_list= len(df_values.tolist())

data = []
nom = ArcGIS()
count=0
print(str(count)+' / '+str(size_list))
for each in df_list:
    reg_lat_long = [each[1],each[2]]# Region , Area
    result = nom.geocode('Latvia '+each[8])#forward Latvia + Reg_area
    reg_lat_long.append(result.latitude)
    reg_lat_long.append(result.longitude)
    data.append(reg_lat_long)
    count+=1
    print(str(count) + ' / ' + str(size_list))

df_final = pd.DataFrame(data,columns=['Region','Area','Latitude','Longitude'])
df_final.to_excel('coordinates.xlsx', index=False)
print('Done')