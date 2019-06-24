import csv
from maclookup import ApiClient
import json
import pandas as pd

#import wifi data
wigle_wifi = pd.read_csv('WigleWifi_all.csv', encoding='utf-8')
df = pd.DataFrame(wigle_wifi)
wifiList = list(df['MAC'])

#establish client to maclookup
client = ApiClient('at_vsEFrkTL6alaO3fzbu3JgaaWnb2j1')

#create a dictionary to hold frequency of oui found
dict = {}

#process the csv, extract the mac
for counter, value in enumerate(wifiList):

    #call maclookup using the mac
    mac = value
    print(f'Looking up {mac}')
    response = client.get(mac)
    oui = response.vendor_details.oui
    name = response.vendor_details.company_name

    #update the data frame by adding the meta data
    df.loc[:, 'OUI'] = oui
    df.loc[:, 'NAME'] = name

    #update dictionary
    if(oui in dict):
        dict[oui] += 1
    else:
        dict[oui] = 1

#output the new data frame containing the meta data to csv
df.to_csv('output.csv')

#sort the dictonary, output the top 10
rank = 1
sorted(dict.values(), reverse=True)
for key, value in dict.items():
    print(f'RANK {rank}  OUI: {key}   FREQUENCY: {value}' )
    rank += 1

    if(rank == 10):
        break


