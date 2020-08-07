# Importing dependencies
from bs4 import BeautifulSoup
from splinter import Browser
from pprint import pprint
import pymongo
import pandas as pd
import requests
from flask import Flask, render_template
import time
import numpy as np
import json
from selenium import webdriver
from urllib.parse import urlsplit

#################################################

def scrape_all():

    executable_path = {"executable_path":"chromedriver.exe"}
    return Browser("chrome", **executable_path, headless = False)    
    news_title, news_paragraph = mars_news(browser)

    mars_data = {
        "news_title": news_title,
        "news_paragraph": news_paragraph,
        "featured_image": featured_image(browser),
        "hemispheres": hemispheres(browser),
        "weather": twitter_weather(browser),
        "facts": mars_facts(),
        "last_modified": dt.datetime.now()
    }
    return mars_data

#################################################

#NASA Mars News

 nasa = "https://mars.nasa.gov/news/"
    browser.visit(nasa)
    html = browser.html
    soup = BeautifulSoup(html,"html.parser")
    news_title = soup.find('div', attrs={'class':'content_title'})
    news_paragraph = soup.find('div', attrs={'class':'article_teaser_body'})
    
    mars_data['news_title'] = news_title
    mars_data['news_paragraph'] = news_paragraph

#################################################

#Mars Featured Image

    url_image = "https://www.jpl.nasa.gov/spaceimages/?search=&category=featured#submit"
    browser.visit(url_image)
    url_html = browser.html
    soup = BeautifulSoup(url_html, 'html.parser')
    fancybox = soup.find('a', class_ = 'button fancybox')
    img_link = fancybox['data-link']
    browser.visit(f'https://www.jpl.nasa.gov{img_link}')
    image_url = browser.html
    soup_ = BeautifulSoup(image_url, 'html.parser')
    full_image_url = soup_.find('img', class_ = "main_image")['src']
    full_image_url = (f'https://www.jpl.nasa.gov{full_image_url}')
    full_image_url
    mars_data['featured_image_link'] = full_image_url

#################################################

#Mars Weather

    url_weather = "https://twitter.com/marswxreport?lang=en"
    browser.visit(url_weather)
    html = browser.html
    tweets = soup.find_all(attrs={"data-testid": "tweet"})
    spans = soup.find_all('span', class_='css-901oao css-16my406 r-1qd0xha r-ad9z0x r-bcqeeo r-qvutc0')
    mars_weather = (tweets, spans)
    mars_data['weather'] = mars_weather

#################################################

#Mars Facts

    mars_facts_url = "https://space-facts.com/mars/"
    table = pd.read_html(mars_facts_url)
    table[0]
    df_mars_facts = table[0]
    df_mars_facts.columns = ["Facts", "Values"]
    df_mars_facts.set_index(["Facts"])
    mars_html_table = df_mars_facts.to_html()
    mars_html_table = mars_html_table.replace("\n", "")
    mars_data["mars_facts_table"] = mars_html_table

#################################################

#Mars Hemisperes

def hemispheres(browser):
    url = (
        "https://astrogeology.usgs.gov/search/"
        "results?q=hemisphere+enhanced&k1=target&v1=Mars"
    )
    browser.visit(url)
    hemisphere_image_urls = []
    for i in range(4):
        browser.find_by_css("a.product-item h3")[i].click()
        hemi_data = scrape_hemisphere(browser.html)
        hemisphere_image_urls.append(hemi_data)
        browser.back()
    return hemisphere_image_urls

def scrape_hemisphere(html_text):
    hemi_soup = BeautifulSoup(html_text, "html.parser")
    try:
        title_elem = hemi_soup.find("h2", class_="title").get_text()
        sample_elem = hemi_soup.find("a", text="Sample").get("href")
    except AttributeError:
        title_elem = None
        sample_elem = None
    hemisphere = {
        "title": title_elem,
        "img_url": sample_elem
    }
    return hemisphere
    print(scrape_all())

#################################################

    browser.quit()
    return mars_data