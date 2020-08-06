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
    
headers = {
    'authority': 'movie.naver.com',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-dest': 'iframe',
    'referer': 'https://movie.naver.com/movie/bi/mi/point.nhn?code=188909',
    'accept-language': 'ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7',
    'cookie': 'NNB=GPSLUSAV4WAV4; ASID=7478b5bd00000171406571ea00000070; NaverSuggestUse=use%26unuse; NRTK=ag#20s_gr#4_ma#2_si#2_en#2_sp#0; LOCALE=ko_KR; _ga_7VKFYR6RV1=GS1.1.1594817412.15.0.1594817412.60; MM_NEW=1; NFS=2; MM_NOW_COACH=1; _ga=GA1.2.2009599851.1585630107; NMUPOPEN=Y; EXT_V1=51169cc8-dea8-453b-a814-a5ceb39f872a; nx_ssl=2; NM_THUMB_PROMOTION_BLOCK=Y; NDARK=N; BMR=; nid_inf=-1487844176; NID_JKL=9gx3rgcpu8aEhHyKw4HbCJkdTKXrSI7bCld3AyNv66M=; page_uid=UyWNHwp0YiRssMqpsKZssssstPG-017481; _naver_usersession_=65s0sSq+BHcFoSeLHUaijw==; csrf_token=f525c1e9-6603-4e26-9c30-82f670a13a27',
}

for data in movie_data:
    code = data['code']
    params = (
        ('code', code),
        ('type', 'after'),
        ('isActualPointWriteExecute', 'false'),
        ('isMileageSubscriptionAlready', 'false'),
        ('isMileageSubscriptionReject', 'false'),
    )

    review_response = requests.get('https://movie.naver.com/movie/bi/mi/pointWriteFormList.nhn', headers=headers, params=params)
    review_soup = BeautifulSoup(review_response.text, 'html.parser')

    review_section = review_soup.select("div > div > div.score_result > ul > li")

    for review in review_section:
        score = review.select_one("div > em").text
        
        review_data = review.select_one("div.score_reple > p")
        review_txt = ""

        if review_data.select_one("span[id^=text_spo]"):
            review_txt = review_data.select_one("span[id^='_filtered_ment_']").text

        elif review_data.select_one("span > span"):
            review_txt = review_data.select_one("span > span > a")['data-src']

        else:
            review_txt = review_data.select_one("span[id^='_filtered_ment']").text

        final_review_data.append(
            {
                'code' : code,
                'score' : score,
                'review' : ' '.join(review_txt.split())
            }
        )

for data in final_review_data:
    print("평점 :", data['score'], "\n리뷰 :", data['review'], "\n")
