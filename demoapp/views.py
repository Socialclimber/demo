from django.shortcuts import render
from bs4 import BeautifulSoup
import requests

# Create your views here.
def index(request):
    return render(request,'base.html')

def new_search(request):
    search = request.POST.get('search')
    stuff_for_front_end = {
        'search': search
    }
    return render(request,'demoapp/new_search.html', stuff_for_front_end)