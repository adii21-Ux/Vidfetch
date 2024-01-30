from rest_framework.decorators import api_view
from rest_framework.response import Response

from background_scheduler.video_fetch import fetch_videos
# Create your views here.

@api_view(['GET'])
def getData(request):
    response = fetch_videos()
    return Response(response)
