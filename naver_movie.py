import requests
from bs4 import BeautifulSoup

movie_data = []
final_review_data = []

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
    code = data['code']
    params = (
        ('code', code),
        ('type', 'after'),
        ('isActualPointWriteExecute', 'false'),
        ('isMileageSubscriptionAlready', 'false'),
        ('isMileageSubscriptionReject', 'false'),
    )

    review_response = requests.get('https://movie.naver.com/movie/bi/mi/pointWriteFormList.nhn', params=params)
    review_soup = BeautifulSoup(review_response.text, 'html.parser')

    review_section = review_soup.select("div > div > div.score_result > ul > li")

    for review in review_section:
        score = review.select_one("div > em").text
        
        review_data = review.select_one("div.score_reple > p")
        review_txt = ""

        if review_data.select_one("span[id^=text_spo]"):
            review_txt = review_data.select_one("span[id^=_filtered_ment_]").text

        elif review_data.select_one("span > span"):
            review_txt = review_data.select_one("span > span > a")['data-src']

        else:
            review_txt = review_data.select_one("span[id^=_filtered_ment]").text

        final_review_data.append(
            {
                'code' : code,
                'score' : score,
                'review' : ' '.join(review_txt.split())
            }
        )

for data in final_review_data:
    print("평점 :", data['score'], "\n리뷰 :", data['review'], "\n")
