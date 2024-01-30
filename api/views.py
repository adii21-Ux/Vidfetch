from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import VideoSerializer
from .models import Video
from rest_framework.pagination import PageNumberPagination

class CustomPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100
    
class AllVideoListView(APIView):
    def get(self, request):
        videos = Video.objects.all().order_by('-published_at')
        serializer = VideoSerializer(videos, many=True)
        return Response(serializer.data)

class VideoListView(APIView):
    pagination_class = CustomPagination

    def get(self, request):
        paginator = self.pagination_class()
        videos = Video.objects.all().order_by('-published_at')
        result_page = paginator.paginate_queryset(videos, request)
        serializer = VideoSerializer(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)

class FilteredVideoListView(APIView):
    pagination_class = CustomPagination

    def get(self, request):
        field = request.query_params.get('field', 'published_at')
        order = request.query_params.get('order', 'desc')

        if order not in ['asc', 'desc']:
            return Response({'error': 'Invalid order parameter. Use "asc" or "desc".'}, status=status.HTTP_400_BAD_REQUEST)

        videos = Video.objects.all()

        if field == 'published_at':
            field = '-published_at' if order == 'desc' else 'published_at'
        else:
            field = f'{field}' if order == 'asc' else f'-{field}'

        videos = videos.order_by(field)

        # Paginate the results
        paginator = self.pagination_class()
        result_page = paginator.paginate_queryset(videos, request)
        serializer = VideoSerializer(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)


class DeleteAllVideosView(APIView):
    def delete(self, request):
        try:
            # Delete all videos from the database
            Video.objects.all().delete()
            return Response({'message': 'All videos deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
