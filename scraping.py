import requests
from bs4 import BeautifulSoup
import sqlite3
import shutil

def main():
    #volunteer()
    jidoukaikan()
    


def volunteer():
    #URL = "https://activo.jp/hokkaido/children"
    URL = "https://activo.jp/searchresult?area[]=1&area_keywords=&genre[]=2&status[]=1"
    page = requests.get(URL)
    soup = BeautifulSoup(page.content, "html.parser")

    # 要素を検索する
    events = soup.select("#gtmMainSearch > article.resultBox.jsResultBox.isWideInside")
    #print(events)
    # スクレイピングしたデータを表示する
    for i,event in enumerate(events):
        title = event.find('h3').text
        location = event.find('li',class_='p_icon isGetAreas resultElementsItem').text
        date = event.find('li',class_='p_icon isGetDatesOrTerms resultElementsItem').text
        print(i,title,end=' | ')
        print(location,end=' | ')
        #print()
        print(date)

def jidoukaikan():

    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS jidoukaikan (id INTEGER PRIMARY KEY, name TEXT, region TEXT, location TEXT, access TEXT, tel TEXT,web TEXT)
    ''')

    for area in ['chuo','kita','minami','higashi','nishi','atsubetsu','toyohira','kiyota','teine','shiroishi']:
        
        URL = "https://g-kan.syaa.jp/jidoukaikan/?area=" + area
        page = requests.get(URL)
        soup = BeautifulSoup(page.content, "html.parser")

        # 要素を検索する
        jidoukaikan = soup.select("#search > section.jidoukaikanKaikan > div > section")


        for data in jidoukaikan:
            data.ruby.clear()
            name = data.find('h3',class_='jidoukaikanKaikanCard_head-ttl').text.strip()
            location = data.find('p',class_='address').text.rstrip()
            region = area
            access = data.find('p',class_='access dark-c-bk').text
            tel = data.find('p',class_='tel').text

            #不要な文字の削除
            location = location.replace("\r\n", "")
            location = location[9:]
            access = access.replace("\u3000","")
            access = access.replace("\t","")
            access = access.replace("\r\n","")
            tel = tel[4:]
            tel = '011-' + tel

            #データベースへの挿入
            cursor.execute('''
                INSERT INTO jidoukaikan (name,region,location,access,tel) VALUES (?, ?, ?, ?, ?)
            ''', (name, location, region, access, tel))

    conn.commit()
    cursor.execute('''
    SELECT * FROM jidoukaikan
    ''')
    for row in cursor.fetchall():
        print(row)
    conn.close()

if __name__ == "__main__":
    main()