from django.shortcuts import render
from bs4 import BeautifulSoup
import requests
from requests.compat import quote_plus
from . import models

BASE_CRAIGSLIST_URL = 'https://losangeles.craigslist.org/search/?query={}'
BASE_IMAGE_URL = 'https://images.craigslist.org/{}_300x300.jpg' 
# Create your views here.
def index(request):
    return render(request,'base.html')

def new_search(request):
    search = request.POST.get('search')
    models.Search.objects.create(search=search)
    final_url = BASE_CRAIGSLIST_URL.format(quote_plus(search))
    response = requests.get(final_url)
    data = response.text
    # create a beautifulsoup object that returns an object of the results
    soup = BeautifulSoup(data, features='html.parser')
    # extract all the links with class 'result-title'
    post_listings = soup.find_all('li', {'class':'result-row'})
    
    final_post_listing = []
    for p in post_listings:
        post_url = p.find('a').get('href')
        post_title = p.find(class_='result-title').text
        if p.find(class_='result-price'):
            post_price = p.find(class_ ='result-price').text
        else:
            post_price ='N/A'

        if p.find(class_='result-image').get('data-ids'):
            post_image_id = p.find(class_='result-image').get('data-ids').split(',')[0].split(':')[1]
            post_image_url = BASE_IMAGE_URL.format(quote_plus(post_image_id))
            print(post_image_url)
        else:
            post_image_url = 'https://images.craigslist.org/images/peace.jpg'

        final_post_listing.append((post_title,post_url,post_price,post_image_url))
           
        



    stuff_for_front_end = {
        'search': search,
        'final_post_listing': final_post_listing
    }
    return render(request,'demoapp/new_search.html', stuff_for_front_end)