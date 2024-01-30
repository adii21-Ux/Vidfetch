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
def fetch_and_store_videos(search_query='minecraft', days_ago=200, max_results=25):
    # latest_video_published_at = Video.objects.order_by('-published_at').first()
    # # print(latest_video_published_at.published_at)
    
    # if latest_video_published_at:
    #     # If there are existing videos in the database, set the publishedAfter parameter
    #     latest_date = str(latest_video_published_at.published_at)
    #     latest_video_published_at = datetime.fromisoformat(latest_date).replace(tzinfo=None)
    #     current_datetime = datetime.strptime(str(datetime.utcnow()), "%Y-%m-%d %H:%M:%S.%f") 
        
    #     delta_days = (current_datetime - latest_video_published_at).days
    #     # days_ago = timedelta(days=delta_days)
    #     # print("delta_days", delta_days)
    #     # print("days_ago", days_ago)
    
    # Get the most recent published_at value from the database
    most_recent_video = Video.objects.order_by('-published_at').first()
    published_after_datetime = most_recent_video.published_at if most_recent_video else datetime.utcnow() - timedelta(days=7)
    
    videos_data = []
    
    for api_key in DEVELOPER_KEYS:
        # Calculate publishedAfter datetime
        # published_after_datetime = datetime.utcnow() - timedelta(days=delta_days)
        published_after_string = format_published_after(published_after_datetime)
        
        print("published_after_string",published_after_string)
        print("published_after_string",published_after_datetime)
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
        print(response)
        
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

            Video.objects.bulk_create([Video(**data) for data in videos_data])
            
        # Break the loop if videos are fetched successfully
        break
