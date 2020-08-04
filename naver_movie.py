import requests
from bs4 import BeautifulSoup

movie_data = []

url = "https://movie.naver.com/movie/running/current.nhn#"

response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')

section = soup.select("div[id='wrap'] > div[id='container'] > div[id='content'] > div.article > div.obj_section > div.lst_wrap > ul > li")

for movie in section:
    movie_link = movie.select_one('dl > dt > a')
    movie_data.append(

        {
            'title' : movie_link.text, 
            'code' : movie_link['href'].split('=')[1]
        }

    )
for data in movie_data:
    print(data)