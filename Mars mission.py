#!/usr/bin/env python
# coding: utf-8

# In[1]:


from splinter import Browser
from bs4 import BeautifulSoup


# In[2]:


get_ipython().system('which chromedriver')


# In[3]:


executable_path = {'executable_path': '/usr/local/bin/chromedriver'}
browser = Browser('chrome', **executable_path, headless=False)


# In[4]:


url = 'https://mars.nasa.gov/news/'
browser.visit(url)


# In[5]:


html = browser.html


# In[6]:


soup = BeautifulSoup(html, 'html.parser')


# In[7]:


slideElement = soup.select_one('ul.item_list li.slide')
slideElement


# In[8]:


New_Title= slideElement.find("div", class_='content_title').get_text()


# In[9]:


New_Paragraph = slideElement.find("div", class_='article_teaser_body').get_text()

New_Paragraph


# In[10]:


url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
browser.visit(url)


# In[11]:


full_image_elem = browser.find_by_id('full_image')
full_image_elem.click()


# In[12]:


import time
time.sleep(3)


# In[13]:


more_info_elem = browser.find_link_by_partial_text('more info')
more_info_elem.click()
html2 = browser.html
img_soup = BeautifulSoup(html2, 'html.parser')


# In[14]:


img_url_rel = img_soup.select_one('figure.lede a img').get("src")
img_url_rel 



# In[15]:


category = img_soup.select_one('figure.lede')


Partial_url = category.find('a')['href']


# In[16]:


Fullimage_url = 'https://www.jpl.nasa.gov' + Partial_url

Fullimage_url


# In[17]:


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


# In[18]:


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


# In[19]:


print (hemisphere_image_urls)


# In[20]:


import pandas as pd
df = pd.read_html('http://space-facts.com/mars/')[0]
df.columns=['description', 'value']
df.set_index('description', inplace=True)
df


# In[ ]:





# In[21]:


df.to_html()


# In[22]:


url = 'https://twitter.com/marswxreport?lang=en'
browser.visit(url)

html = browser.html


# In[23]:


weather_soup = BeautifulSoup(html, 'html.parser')
# First, find a tweet with the data-name `Mars Weather`
mars_weather_tweet = weather_soup.find('div', attrs={"class": "tweet", "data-name": "Mars Weather"})
mars_weather = mars_weather_tweet.find('p', 'tweet-text').get_text()
mars_weather


# In[ ]:




