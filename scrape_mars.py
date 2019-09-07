import requests
from splinter import Browser
from bs4 import BeautifulSoup


def scrape():
    mars = {}

    executable_path = {'executable_path': 'chromedriver.exe'}

    browser = Browser('chrome', **executable_path)

    nasa_link = 'https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest'
    browser.visit(nasa_link)
    browser.is_element_present_by_css("ul.item_list li.slide", wait_time=5)

    response = requests.get(nasa_link)

    html = browser.html
    soup = BeautifulSoup(response.content, 'html.parser')

    article = soup.find_all('div', class_='content_title')

    mars['news_title'] = (article[0].text)
    # latest_date=article_date[0]

    article_body = soup.find_all('div', class_="rollover_description_inner")

    mars['news_p'] = article_body[0].text

    # Get current NASA Mars picture
    image = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'

    browser.visit(image)
    browser.find_by_id("full_image").click()
    browser.is_element_present_by_css('img.fancybox-image', wait_time=1)
    html = browser.html

    soup = BeautifulSoup(html, 'html.parser')

    mars_pic = soup.select('.fancybox-image')[0].get('src')

    mars['image'] = (mars_pic)

    home = 'https://www.jpl.nasa.gov'
    featured_image_url = (f"{home}{mars_pic}")
    featured_image_url

    # Mars Weather
    weather = 'https://twitter.com/marswxreport?lang=en'
    browser.visit(weather)

    # extract data from browser
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    weather_tweet = soup.find_all(
        'p', class_='TweetTextSize TweetTextSize--normal js-tweet-text tweet-text')
    mars['weather'] = weather_tweet[0].text

    # MARS FACTS
    import pandas as pd

    url = 'https://space-facts.com/mars/'

    tables = pd.read_html(url)
    tables

    type(tables)

    df = tables[0]
    df.columns = ['Comparison', 'Mars', 'Earth']
    df.head()

    mars['table'] = df.to_html()

    # MARS HEMISPHERE
    hemi = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(hemi)
    browser.is_element_present_by_css('img.thumb', wait_time=1)

    response = requests.get(hemi)

    # extract content from browser
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    # empty list to add horizon image results & titles
    img_link_list = []
    title_list = []

    for link in range(0, 4):
        browser.is_element_present_by_css('a.product-item h3', wait_time=1)
        browser.find_by_css("a.product-item h3")[link].click()
        browser.is_element_present_by_text('Sample', wait_time=1)
        img_link = browser.find_link_by_text('Sample').first
        img_link_list.append(img_link['href'])
        title_search = browser.find_by_css('h2.title').text
        title_list.append(title_search)
        browser.back()

    # links obtained from the loop
    img_link_list

    # image titles gotten from the loop
    title_list

    # Make hemisphere dictionary
    hemi_dic = dict(zip(img_link_list, title_list))
    hemi_dic

    hemisphere_image_urls = []
    for i in range(len(img_link_list)):
        link_dict = {}
        link_dict['title'] = title_list[i]
        link_dict['img_url'] = img_link_list[i]
        hemisphere_image_urls.append(link_dict)

    mars['hemis'] = (hemisphere_image_urls)

    print(mars)
    return mars
