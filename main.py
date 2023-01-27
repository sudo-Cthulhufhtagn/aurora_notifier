import os
import requests
import pandas as pd
from bs4 import BeautifulSoup
import json
from tabulate import tabulate

if not os.getenv('CI'):
    from dotenv import load_dotenv
    load_dotenv()

BOT_TOKEN = os.getenv('BOT_TOKEN')
CHAT_ID = os.getenv('CHAT_ID')

LINK_METEOBLUE = "https://www.meteoblue.com/en/weather/outdoorsports/seeing/tartu_estonia_588335"
LINK_SWPC = 'https://services.swpc.noaa.gov/products/noaa-planetary-k-index-forecast.json'


def parse_meateoblue(soup: BeautifulSoup):
    time_h = []
    data = []
    
    tbody = soup.find('tbody')

    print(len(tbody.find_all('tr', recursive=False)))
    print([0 for i in tbody.find_all('tr', recursive=False)])

    for tr in tbody.find_all('tr', recursive=False):
        # print(tr.get('class'))
        if not tr.get('class') or len(tr.get('class', []))==1:
            # print(tr)
            date = tr.find('td', {'class': 'new-day'}).text.split()[1]
            # print(date)
            # break

        if len(tr.get('class', []))==2:
            try:
                # print(tr.find('td', {'class': 'time'}).string.strip())
                data_row = [0 for i in range(4)]
                time_h.append(int(tr.find('td', {'class': 'time'}).string.strip()))
                for i, td in enumerate(tr.findAll('td')[:4]):
                    try:
                        # print(td.string.strip())
                        data_row[i]= int(td.string.strip())
                    except:
                        print(td)
                data_row.insert(0, date)
                data.append(data_row)
            except:
                pass
        
    df = pd.DataFrame(data, columns=['date', 'time', 'low', 'mid', 'high'])
    df['date_time'] = pd.to_datetime(df['date'] + ' ' + df['time'].astype(str)+':00:00', format="%Y-%m-%d %H:%M:%S")
    return df

def parse_swpc(response: json):
    df2 = pd.DataFrame(response.json())
    df2.columns = df2.iloc[0]
    df2 = df2[1:]
    df2['dt'] = pd.to_datetime(df2['time_tag'], format="%Y-%m-%d %H:%M:%S")
    return df2
    

    

if __name__=='__main__':
    html_content = requests.get(LINK_METEOBLUE).text
    soup = BeautifulSoup(html_content, 'html.parser')
    df_meteoblue = parse_meateoblue(soup=soup)

    response = requests.get(LINK_SWPC)
    df_swpc = parse_swpc(response=response)
    
    df_merged = pd.merge(
            left=df_meteoblue.drop(columns=['date', 'time']),
            right=df_swpc.drop(columns=['time_tag'])[df_swpc.kp.astype(float)>2], 
            how='inner', # outer
            left_on='date_time', 
            right_on='dt').drop(columns=['dt', 'noaa_scale'])

    message = tabulate(df_merged, headers='keys', tablefmt='psql',  showindex=False).replace("+",'*').replace('-','_')
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage?chat_id={CHAT_ID}&text={message}"
    print(requests.get(url).json())
    print(message)
