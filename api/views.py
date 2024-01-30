from rest_framework.decorators import api_view
from rest_framework.response import Response
from datetime import datetime
from .serializers import VideoSerializer
from .models import Video
from rest_framework import status

@api_view(['GET'])
def getData(request):
    videos = Video.objects.all()
    serializer = VideoSerializer(videos, many=True)
    return Response(serializer.data)

@api_view(['DELETE'])
def delete_all_videos(request):
    try:
        # Delete all videos from the database
        Video.objects.all().delete()
        return Response({'message': 'All videos deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)