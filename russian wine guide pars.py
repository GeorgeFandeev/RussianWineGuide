import requests 
from bs4 import BeautifulSoup
import pandas as pd
import regex
import datetime

#%%


def get_wines_list(url):

    r = requests.get(url)
    if r.status_code == 200:
        soup = BeautifulSoup(r.text)
        ns = soup.findAll('noscript')
        wl = ns[4].findAll('a')
        
    return wl 



def replace_commas(string):
    
    return regex.sub(',','.',string)



def get_first_element(l):
    if len(l)>0:
        l = l[0]
    else:
        l = '' 
        
    return l


def get_property(property_name,properties):
    for i,prop in enumerate(properties):
        if prop.text == property_name:
            return properties[i+1].text
    
    return ''
        


def get_wine(url,wine_type):
    
    wine = None
    

    r= requests.get(url)
    
     
    if r.status_code==200:
        s = BeautifulSoup(r.text)
        
        name = s.find('p', class_='product-subtitle').text
        
        price_per_value = s.find('span',class_="info-price").text
        
        price = regex.findall('\d*', price_per_value)
        price = get_first_element(price)
        
        price_for = regex.findall('\/0[,.]\d*',price_per_value)
        price_for = get_first_element(price_for)

        if len(price_for)>0:
            price_for = regex.sub('/','',price_for)
            price_for = replace_commas(price_for)
        
        
        properties = s.find('div',class_="properties")
        properties = properties.findAll('p')
        
        
        
        winery = get_property('Производитель',properties)#properties[1].text
        research_year = get_property('Год исследования',properties)#properties[3].text
        barcode = get_property('Штрихкод',properties)#properties[5].text
        vintage = get_property('Год урожая',properties)#properties[7].text
        sugar = get_property('Сахар',properties)#properties[9].text 
        color = get_property('Цвет',properties)#properties[11].text
        rating_gost = get_property('Оценка по ГОСТ 32051-2013',properties)#properties[11].text
        
        
        rating = s.find('div', class_ = 'starrating readonly d-inline-flex flex-row-reverse')
        rating = rating.findAll('span')[0].text
        
        
        wine = {'name':                 name,
                'wine_type':            wine_type,
                'barcode':              barcode,
                'winery':               winery,
                'research_year':        research_year,
                'vintage':              vintage,
                'sugar':                sugar,
                'color':                color,
                'price':                price,
                'price_for':            price_for,
                'rating_gost':          rating_gost,
                'rating':               rating   ,
                'wine_type':            wine_type,
                'url':                  url
            }
        
        return wine


def parse_wine_from_wine_list(winelist, wine_type):

    df=None
    k = 1
    l=str(len(winelist))
    for wine_page in winelist:
        
        print('Обрабатываем '+str(k) +' из ' +l)
            
        url = 'https://rskrf.ru/'+wine_page['href']
        
        print(url)
        
        new_wine = get_wine(url, wine_type)
        
        if type(df)==type(None):
            df = pd.DataFrame([new_wine])
        else:
            df = df.append(new_wine, ignore_index=True)
        
        k=k+1
        
    return df


#%%

wine_df = None 

winelist = get_wines_list('https://rskrf.ru/ratings/napitki/alkogolnye/krasnoe-vino/')
wine_df = parse_wine_from_wine_list(winelist,'Красное')


# winelist = get_wines_list('https://rskrf.ru/ratings/napitki/alkogolnye/beloe-vino/','Белое')
# winelist = get_wines_list('https://rskrf.ru/ratings/napitki/alkogolnye/likyernoe-vino/','Ликерное')
# winelist = get_wines_list('https://rskrf.ru/ratings/napitki/alkogolnye/rozovoe-vino/','Розовое')
# winelist = get_wines_list('https://rskrf.ru/ratings/napitki/alkogolnye/igristoe/','Игристое')

    
#%%
wine_df = wine_df.append(parse_wine_from_wine_list(get_wines_list('https://rskrf.ru/ratings/napitki/alkogolnye/beloe-vino/'),'Белое'))
wine_df = wine_df.append(parse_wine_from_wine_list(get_wines_list('https://rskrf.ru/ratings/napitki/alkogolnye/rozovoe-vino/'),'Розовое'))
wine_df = wine_df.append(parse_wine_from_wine_list(get_wines_list('https://rskrf.ru/ratings/napitki/alkogolnye/likyernoe-vino/'),'Ликерное'))
wine_df = wine_df.append(parse_wine_from_wine_list(get_wines_list('https://rskrf.ru/ratings/napitki/alkogolnye/igristoe/'),'Игристое'))

#%%
wine_df.to_csv('wines_df.csv')#+str(datetime.datetime.now())+'.csv')




#%%

print(winelist)

