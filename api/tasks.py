from celery import shared_task
from .models import Video
from django.conf import settings
import requests
from datetime import datetime, timedelta
from django.db import transaction
import os
from dotenv import load_dotenv
from pytz import timezone as tz


load_dotenv(".env")
DEVELOPER_KEYS = os.getenv("YOUTUBE_DATA_API_KEYS").split(',')

def format_published_after(datetime_obj):
    return datetime_obj.strftime('%Y-%m-%dT%H:%M:%SZ')

@shared_task
def fetch_and_store_videos(search_query='minecraft', days_ago=7, max_results=50):
    # Get the most recent published_at value from the database
    last_published_at = None
    most_recent_video = Video.objects.order_by('-published_at').last()
    if most_recent_video:
        print(most_recent_video.published_at)
    published_after_datetime = most_recent_video.published_at if most_recent_video else datetime.utcnow() - timedelta(days=days_ago)
    
    videos_data = []
    
    for api_key in DEVELOPER_KEYS:
        # Set initial values for published_after and published_before
        if last_published_at is None:
            published_before = datetime.now()
            published_after = published_before - timedelta(days=20)
        else:
            published_before = last_published_at
            published_after = published_before - timedelta(days=20)

        # Convert datetime objects to formatted strings
        published_before_string = format_published_after(published_before)
        published_after_string = format_published_after(published_after)

        
        params = {
            'part': 'snippet',
            'q': search_query,
            'key': api_key,
            'type': 'video',
            'maxResults': max_results,
            'publishedAfter': published_after_string,
            'publishedBefore': published_before_string,
        }

        res = requests.get('https://www.googleapis.com/youtube/v3/search', params=params)
        response = res.json()
        # print(response)
        
        if 'error' in response and any(error.get('reason') == 'quotaExceeded' for error in response['error']['errors']):
            # Move to the next API key if quota is exceeded
            continue

        with transaction.atomic():
            for item in response['items']:
                video_id = item['id']['videoId']
                if not Video.objects.filter(video_id=video_id).exists():
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

            Video.objects.bulk_create([Video(**data) for data in videos_data])
            
        # Break the loop if videos are fetched successfully
        break
