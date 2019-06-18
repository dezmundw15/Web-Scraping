#!/usr/bin/env python
# coding: utf-8
from splinter import Browser
from bs4 import BeautifulSoup
import pandas as pd
import time
from pprint import pprint
import datetime as dt

def init_browser():
    

    #get_ipython().system('which chromedriver')

    executable_path = {'executable_path': '/usr/local/bin/chromedriver'}
    return Browser('chrome', **executable_path, headless=False)


def scrape_all():

    # Initiate headless driver for deployment
    browser = init_browser()
    news_title, news_paragraph = mars_news(browser)

    data = {
        "news_title": news_title,
        "news_paragraph": news_paragraph,
        "featured_image": featured_image(browser),
        "hemispheres": hemispheres(browser),
        "weather": twitter_weather(browser),
        "facts": mars_facts(),
        "last_modified": dt.datetime.now()
    }
    # Stop webdriver and return data
    browser.quit()
    return data

def mars_news (browser):
    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)
    time.sleep(2)

    html = browser.html

    soup = BeautifulSoup(html, 'html.parser')
    slideElement = soup.select_one('ul.item_list li.slide')
    slideElement
    News_Title= slideElement.find("div", class_='content_title').get_text()
    News_Paragraph = slideElement.find("div", class_='article_teaser_body').get_text()

    print (News_Paragraph, News_Title)
    return News_Title, News_Paragraph

def scrape_hemisphere(html_text):

   # Soupify the html text
   hemi_soup = BeautifulSoup(html_text, "html.parser")

   # Try to get href and text except if error.
   try:
       title_elem = hemi_soup.find("h2", class_="title").get_text()
       sample_elem = hemi_soup.find("a", text="Sample").get("href")

   except AttributeError:

       # Image error returns None for better front-end handling
       title_elem = None
       sample_elem = None

   hemisphere = {
       "title": title_elem,
       "img_url": sample_elem
   }

   return hemisphere

def hemispheres(browser):

    # A way to break up long strings
    url = (
        "https://astrogeology.usgs.gov/search/"
        "results?q=hemisphere+enhanced&k1=target&v1=Mars"
    )

    browser.visit(url)

    # Click the link, find the sample anchor, return the href
    hemisphere_image_urls = []
    for i in range(4):

        # Find the elements on each loop to avoid a stale element exception
        browser.find_by_css("a.product-item h3")[i].click()

        hemi_data = scrape_hemisphere(browser.html)

        # Append hemisphere object to list
        hemisphere_image_urls.append(hemi_data)

        # Finally, we navigate backwards
        browser.back()

    return hemisphere_image_urls


#Obtain Featured Image

def featured_image(browser):
    url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url)
    import time
    time.sleep(2)

    full_image_elem = browser.find_by_id('full_image')
    full_image_elem.click()

   
    time.sleep(3)

    more_info_elem = browser.find_link_by_partial_text('more info')
    more_info_elem.click()
    time.sleep(2)
    html2 = browser.html
    img_soup = BeautifulSoup(html2, 'html.parser')

    img_url_rel = img_soup.select_one('figure.lede a img').get("src")
    img_url_rel 

    category = img_soup.select_one('figure.lede')

    Partial_url = category.find('a')['href']

    Fullimage_url = 'https://www.jpl.nasa.gov' + Partial_url

    print (Fullimage_url)
    return Fullimage_url


    # A way to break up long strings

def mars_facts():    
    df = pd.read_html('http://space-facts.com/mars/')[0]
    df.columns=['description', 'value']
    df.set_index('description', inplace=True)
    print (df)
    # Add some bootstrap styling to <table>
    return df.to_html(classes="table table-striped")

    #df.to_html()

    #df_facts_html = df.to_html(classes="mars_facts table table-striped")
 
def twitter_weather(browser):
    url = 'https://twitter.com/marswxreport?lang=en'
    browser.visit(url)
    html = browser.html

    weather_soup = BeautifulSoup(html, 'html.parser')
    # First, find a tweet with the data-name `Mars Weather`
    mars_weather_tweet = weather_soup.find('div', attrs={"class": "tweet", "data-name": "Mars Weather"})
    mars_weather = mars_weather_tweet.find('p', 'tweet-text').get_text()
    print (mars_weather)
    return (mars_weather)

    
# Mainline code to test function mars_scrape()
#mars_data_result = scrape_all()
#pprint(mars_data_result)


