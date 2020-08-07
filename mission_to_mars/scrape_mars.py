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


def init_browser():
    executable_path = {"executable_path":"chromedriver.exe"}
    return Browser("chrome", **executable_path, headless = False)

def scrape():
    browser = init_browser()
    mars_data = {}

    #NASA Mars News
    nasa = "https://mars.nasa.gov/news/"
    browser.visit(nasa)
    html = browser.html
    soup = BeautifulSoup(html,"html.parser")
    news_title = soup.find('div', attrs={'class':'content_title'})
    news_paragraph = soup.find('div', attrs={'class':'article_teaser_body'})
    
    mars_data['news_title'] = news_title
    mars_data['news_paragraph'] = news_paragraph

    
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
    
    
    #Mars Weather
    url_weather = "https://twitter.com/marswxreport?lang=en"
    browser.visit(url_weather)
    
    tweets = soup.find_all(attrs={"data-testid": "tweet"})
    spans = soup.find_all('span', class_='css-901oao css-16my406 r-1qd0xha r-ad9z0x r-bcqeeo r-qvutc0')
    mars_weather = (tweets, spans)
    mars_data['weather'] = mars_weather
    
    
    #Mars Facts
    url_facts = "https://space-facts.com/mars/"
    table = pd.read_html(url_facts)
    table[0]

    df_mars_facts = table[0]
    df_mars_facts.columns = ["Parameter", "Values"]
    clean_table = df_mars_facts.set_index(["Parameter"])
    mars_html_table = clean_table.to_html()
    mars_html_table = mars_html_table.replace("\n", "")
    mars_data["mars_facts_table"] = mars_html_table

    
    
    #Mars Hemisperes
    url_hemisphere = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(url_hemisphere)
    hemisphere_base_url = "{0.scheme}://{0.netloc}/".format(urlsplit(url_hemisphere))


    #Cerberus-Hemisphere-image-url
    hemisphere_img_urls = []
    results = browser.find_by_xpath( "//*[@id='product-section']/div[2]/div[1]/a/img").click()
    cerberus_open_click = browser.find_by_xpath( "//*[@id='wide-image-toggle']").click()
    cerberus_image = browser.html
    soup = BeautifulSoup(cerberus_image, "html.parser")
    cerberus_url = soup.find("img", class_="wide-image")["src"]
    cerberus_img_url = hemisphere_base_url + cerberus_url
    cerberus_title = soup.find("h2",class_="title").text
    back_button = browser.find_by_xpath("//*[@id='splashy']/div[1]/div[1]/div[3]/section/a").click()
    cerberus = {"image title":cerberus_title, "image url": cerberus_image_url}
    hemisphere_image_urls.append(cerberus)


    #Schiaparelli-Hemisphere-image-url
    results1 = browser.find_by_xpath( "//*[@id='product-section']/div[2]/div[2]/a/img").click()
    schiaparelli_open_click = browser.find_by_xpath( "//*[@id='wide-image-toggle']").click()
    schiaparelli_image = browser.html
    soup = BeautifulSoup(schiaparelli_image, "html.parser")
    schiaparelli_url = soup.find("img", class_="wide-image")["src"]
    schiaparelli_img_url = hemisphere_base_url + schiaparelli_url
    schiaparelli_title = soup.find("h2",class_="title").text
    back_button = browser.find_by_xpath("//*[@id='splashy']/div[1]/div[1]/div[3]/section/a").click()
    schiaparelli = {"image title":schiaparelli_title, "image url": schiaparelli_image_url}
    hemisphere_image_urls.append(schiaparelli)


    #Syrtis Major Hemisphere
    results1 = browser.find_by_xpath( "//*[@id='product-section']/div[2]/div[3]/a/img").click()
    syrtis_major_open_click = browser.find_by_xpath( "//*[@id='wide-image-toggle']").click()
    syrtis_major_image = browser.html
    soup = BeautifulSoup(syrtis_major_image, "html.parser")
    syrtis_major_url = soup.find("img", class_="wide-image")["src"]
    syrtis_major_img_url = hemisphere_base_url + syrtis_major_url
    syrtis_major_title = soup.find("h2",class_="title").text
    back_button = browser.find_by_xpath("//*[@id='splashy']/div[1]/div[1]/div[3]/section/a").click()
    syrtis_major = {"image title":syrtis_major_title, "image url": syrtis_major_image_url}
    hemisphere_image_urls.append(syrtis_major)


    #Valles Marineris Hemisphere
    results1 = browser.find_by_xpath( "//*[@id='product-section']/div[2]/div[4]/a/img").click()
    valles_marineris_open_click = browser.find_by_xpath( "//*[@id='wide-image-toggle']").click()
    valles_marineris_image = browser.html
    soup = BeautifulSoup(valles_marineris_image, "html.parser")
    valles_marineris_url = soup.find("img", class_="wide-image")["src"]
    valles_marineris_img_url = hemisphere_base_url + syrtis_major_url
    valles_marineris_title = soup.find("h2",class_="title").text
    back_button = browser.find_by_xpath("//*[@id='splashy']/div[1]/div[1]/div[3]/section/a").click()
    valles_marineris = {"image title":valles_marineris_title, "image url": valles_marineris_image_url}
    hemisphere_image_urls.append(valles_marineris)


    mars_data["hemisphere_image_url"] = hemisphere_image_urls

    
    browser.quit()
    return mars_data