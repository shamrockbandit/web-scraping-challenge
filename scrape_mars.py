# To add a new cell, type '# %%'
# To add a new markdown cell, type '# %% [markdown]'
# %%
from bs4 import BeautifulSoup as bs
from splinter import Browser
import pandas as pd
import datetime as dt
# %%
executable_path = {'executable_path': '/usr/local/bin/chromedriver'}
browser = Browser('chrome', **executable_path, headless=False)


def mars_news(browser):
    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)
    html = browser.html
    soup = bs(html, "html.parser")

    try: 
        article = soup.find("div", class_='list_text')
        headline = article.find("div", class_="content_title").text
        blurb = article.find("div", class_ ="article_teaser_body").text
        print(headline)
        print("----------")
        print(blurb)
    except AttributeError:
        return None, None

    return article, headline
# %%
def featured_image(browser): 
    img_url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(img_url)
    image_loc = browser.find_by_id('full_image')
    image_loc.click()
    browser.is_element_present_by_text("more info", wait_time=1)
    more_info = browser.find_link_by_partial_text("more info")
    more_info.click()
    html = browser.html
    img_bs = bs(html, 'html.parser')

    try: 
        img_url_ri = img_bs.select_one('figure.lede a img').get("src")
    except AttributeError: 
        return None

    complete_url = f'https://www.jpl.nasa.gov{img_url_ri}'
    return complete_url
# %%
def mars_weather(browser):
    weather_url = "https://twitter.com/marswxreport?lang=en"
    browser.visit(weather_url)
    html = browser.html
    weather_bs = bs(html, 'html.parser')
    weather_tweet = weather_bs.find("div", attrs={"class": "tweet", "data-name": "Mars Weather"})
    try:
        weather_text = weather_tweet.find("p", "tweet-text").get_text()
    except AttributeError:
        return None
    return weather_text
# %%
def mars_facts(browser):
    try:    
        mars_df = pd.read_html('https://space-facts.com/mars/')[0]
    except BaseException:
        return None
    mars_df.columns=['description', 'value']
    mars_df.set_index('description', inplace=True)
    return mars_df.to_html(classes="table table-striped")
# %%
def hemisphere(browser):
    hemi_url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(hemi_url)
    hemi_links = []
    mars_hemis = browser.find_by_css("a.product-item h3")

    for i in range(len(mars_hemis)):
        hemi = {}
        browser.find_by_css("a.product-item h3")[i].click()
        sample_image = browser.find_link_by_text('Sample').first
        hemi['img_url'] = sample_image['href']
        hemi['title'] = browser.find_by_css("h2.title").text
        hemi_links.append(hemi)
        browser.back()
    hemi_links   
# %%
def scrape_hemisphere(html_text):
    hemi_html = bs(html_text, "html.parser")
    try:
        title = hemi_html.find("h2", class_="title").get_text()
        sample = hemi_html.find("a", text="Sample").get("href")
    except AttributeError:
        title = None
        sample = None
    hemisphere = {
        "title": title,
        "img_url": sample
    }
    return hemisphere


