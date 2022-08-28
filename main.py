
import bs4
import requests
import re

KEYWORDS = ['дизайн', 'фото', 'web', 'python','заметка', 'президент', 'привет', 'обзор', 'куки']
HEADERS = {
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3",
    "Connection": "keep-alive",
    "Cookie": "_ga=GA1.2.2063098236.1579294195; _ym_uid=1579294195381853071; _ym_d=1641302173; \
    __gads=ID=e487ff71e75ec085-22fcd4d2dfd300ee:T=1628432062:R:S=ALNI_Maq4eBOKN_tOJTG_gcolgCNCrCksQ; \
    cto_bundle=T5t0Xl9mUmVMRWFXVUlXTWJKZVRmNWRhbHpTWjJKMSUyQiUyRnExaGR4Tzd6cXFhQUZiJTJGNE1TVExSdHc2NVdkWU5qeTgxODJqazN5Wm1nNnV5dVhaUnZUVjkwRCUyRjYyRVRVS0FCQWJjUHVXSEVxS2M3b2hyZlJYY3BsY0lJODF1NEZ6TGF1VmclMkJBT0dKc3dpMUd3T3dyJTJCelB5ckNwZGclM0QlM0Q;\
    hl=ru; fl=ru; visited_articles=531472; _gid=GA1.2.1874216268.1655576523; habr_web_home_feed=/all/; _ym_isad=2",
    "Sec-Fetch-Dest": "document",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-Site": "none",
    "Sec-Fetch-User": "?1",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:101.0) Gecko/20100101 Firefox/101.0"
}
base_url = "https://habr.com"
url = base_url + "/ru/all/"

def clean_text(text):
    return re.sub(r'[?|$|.|!|,]',"",text) #удаляем некоторые спец. символы

def get_words_key(text_clean,keydict):
    return set(set(text_clean.lower().split())) & keydict

def main():

    response = requests.get(url, headers=HEADERS)
    text = response.text
    soup = bs4.BeautifulSoup(text, features= "html.parser")
    articles = soup.find_all("article")

    keydict = {value for value in KEYWORDS}


    for article in articles:

        previews = article.find_all(class_ = "tm-article-body tm-article-snippet__lead")

        title = article.find("h2").find("span").text
        href = article.find(class_="tm-article-snippet__title-link").attrs["href"]

        link = base_url + href

        date_str = article.find("time").attrs["title"]

        found = False

        for pr in previews:
            text_clean = clean_text(pr.text)
            words_preview = get_words_key(text_clean, keydict)

            if len(words_preview) > 0:
                print(f"{date_str[0:10]} - {title} - {link}, найденные ключевые слова: {words_preview}")
                found = True
                break

        if not found: #если не нашли в превью, то читаем всю статью
            article_link = requests.get(link, headers=HEADERS)
            if article_link.status_code == 200:
                link_text = article_link.text
                link_soup = bs4.BeautifulSoup(link_text, features="html.parser")
                content_post = link_soup.find_all(id = "post-content-body")
                for content in content_post:
                    text_clean = clean_text(content.text)
                    words_preview = get_words_key(text_clean, keydict)
                    if len(words_preview) > 0:
                        print(f"{date_str[0:10]} - {title} - {link} (нашли ключевое слово в статье), найденные ключевые слова: {words_preview}")
                        break

if __name__ == '__main__':
    main()

