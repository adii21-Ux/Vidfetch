from celery import shared_task
from .models import Video
from django.conf import settings
import requests
from datetime import datetime
from .serializers import VideoSerializer

@shared_task
def fetch_and_store_videos():
    videos_data = []
    url = 'https://www.googleapis.com/youtube/v3/search'
    
    params = {
        'part' : 'snippet',
        'q' : 'minecraft',
        'key' : settings.YOUTUBE_DATA_API_KEY,
        'type' : 'video',
        'maxResults' : 25
    }
    
    res = requests.get(url, params=params)
    response = res.json()
    print(response)
    for item in response['items']:
        video_data = {
            'video_id': item['id']['videoId'],
            'title': item['snippet']['title'],
            'description': item['snippet']['description'],
            'published_at': datetime.strptime(item['snippet']['publishedAt'], "%Y-%m-%dT%H:%M:%SZ"),
            'thumbnail_medium_url': item['snippet']['thumbnails']['medium']['url'],
            'channel_id': item['snippet']['channelId'],
            'channel_title': item['snippet']['channelTitle'],
        }
        
        videos_data.append(video_data)

    serializer = VideoSerializer(data=videos_data, many=True)
    if serializer.is_valid():
        serializer.save()
    else:
        print(serializer.error_messages)