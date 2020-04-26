from bs4 import BeautifulSoup as bs
import requests
from splinter import Browser
import pandas as pd
from flask import Flask, render_template
from selenium import webdriver
import time


def init_browser():
    executable_path = {'executable_path': r'C:/Users/Home Laptop/Downloads/chromedriver_win32/chromedriver.exe'}
    return Browser("chrome", **executable_path, headless=False)

def scrape():
    mars_data = {}
  
    # Mars news
    # Visit https://mars.nasa.gov/news/
    url='https://mars.nasa.gov/news/'
    response = requests.get(url)
    
    # Scrape mars news into Soup
    soup = bs(response.text, "html.parser")

    # # Retrieve the parent lists for all news
    results = soup.find_all('li', class_='slide')

    # # loop over results to get news' title,paragraphs
    for result in results:
        # scrape the news title
        news_title = result.find('div', class_='content_title').text
        # scrape the paragraph text
        news_p = result.find('div', class_='article_teaser_body').text

    # Visit https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars 
    # Featured Images
    browser = init_browser()
    
    url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url)
    html=browser.html
    soup = bs(html, 'html.parser')
    images = soup.find_all('a', class_ = "fancybox")

    url_li=[]
    for image in images:
        href = image['data-fancybox-href']

        if 'largesize' in href:
            image_url = 'https://www.jpl.nasa.gov' + href
            url_li.append(image_url)

    featured_image_url = url_li[0]
    browser.quit()
    
    # Visit https://twitter.com/marswxreport?lang=en
  
    url = 'https://twitter.com/marswxreport?lang=en'
    response = requests.get(url)
    # Scrape mars weather twitter page into Soup
    soup = bs(response.text, 'html.parser')
    
    weather_text = soup.find_all("div", class_="js-tweet-text-container")
    weather_tweets = []
    for weather in weather_text:
        tweet = weather.text
        weather_tweets.append(tweet)

    mars_current_weather = weather_tweets[0].strip().strip("pic.twitter.com/Xdbw8T0T0E")  

    # Visit https://space-facts.com/mars/
    # Mars Facts
    url = "https://space-facts.com/mars/"
    table = pd.read_html(url)
    df = table[0]
    df.columns = ['description', 'value']
    table_html = df.to_html(index=False)

    # Visit https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars
    # Mars Hemisphere
    url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    response = requests.get(url)
    soup = bs(response.text, 'html.parser')

    
    image_list = soup.find_all('a', class_="itemLink product-item")
    
    hemisphere_image_urls =[]

    for image in image_list:
        image_dict = {}

        title = image.find('h3').text
        image_dict['title'] = title.strip('Enhanced')

        temp_img_url = image['href']

        # scrape the website
        new_image_url = 'https://astrogeology.usgs.gov' + temp_img_url
        img_request = requests.get(new_image_url)
        full_img_soup = bs(img_request.text, 'lxml')
        img_tag = full_img_soup.find('div', class_ = 'downloads')
        img_url = img_tag.find('a')['href']
        image_dict['img_url'] = img_url

        hemisphere_image_urls.append(image_dict)
    
       # make a dictionary
    mars_data = {
        "news_title": news_title,
        'news_p' : news_p,
        'featured_image_url' : featured_image_url,
        'mars_current_weather' : mars_current_weather,
        'weather' : table_html,
        'hemisphere_image_urls' : hemisphere_image_urls
    }
        

    # Return results
    return mars_data


