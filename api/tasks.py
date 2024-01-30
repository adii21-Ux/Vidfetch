from celery import shared_task
from .models import Video
from django.conf import settings
import requests
from datetime import datetime, timedelta
from django.db import transaction
import os
from dotenv import load_dotenv

load_dotenv(".env")
DEVELOPER_KEYS = os.getenv("YOUTUBE_DATA_API_KEYS").split(',')

def format_published_after(datetime_obj):
    return datetime_obj.isoformat() + "Z"

@shared_task
def fetch_and_store_videos(search_query='minecraft', days_ago=7, max_results=25):
    videos_data = []
    
    for api_key in DEVELOPER_KEYS:
        # Calculate publishedAfter datetime
        published_after_datetime = datetime.utcnow() - timedelta(days=days_ago)
        published_after_string = format_published_after(published_after_datetime)
        print(api_key)
        params = {
            'part': 'snippet',
            'q': search_query,
            'key': api_key,
            'type': 'video',
            'maxResults': max_results,
            'publishedAfter': published_after_string,
        }

        res = requests.get('https://www.googleapis.com/youtube/v3/search', params=params)
        response = res.json()

        if 'error' in response:
            error_reason = response['error']['errors'][0]['reason']
            if error_reason == 'rateLimitExceeded':
                # Move to the next API key if rate limit is exceeded
                continue

        with transaction.atomic():
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

            # Bulk create videos without using a serializer
            Video.objects.bulk_create([Video(**data) for data in videos_data])
            
        # Break the loop if videos are fetched successfully
        break
