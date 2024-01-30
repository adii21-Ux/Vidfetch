from rest_framework.decorators import api_view
from rest_framework.response import Response
from datetime import datetime
from .serializers import VideoSerializer
from .models import Video
# Create your views here.


@api_view(['GET'])
def getData(request):
    videos = Video.objects.all()
    serializer = VideoSerializer(videos, many=True)
    return Response(serializer.data)

