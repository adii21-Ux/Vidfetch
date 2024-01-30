import requests
from django.conf import settings

def fetch_videos():
    url = 'https://www.googleapis.com/youtube/v3/search'
    
    params = {
        'part' : 'snippet',
        'q' : 'minecraft',
        'key' : settings.YOUTUBE_DATA_API_KEY
    }
    
    res = requests.get(url, params=params)
    print(res.json())
    return res.json()