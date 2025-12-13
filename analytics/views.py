from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.core.paginator import Paginator, EmptyPage
from unicodedata import normalize
from .serializers import SongListSerializer

from .models import Song


# Create your views here.

@api_view(['GET'])
def list_songs(request):
    '''send paginated list of songs list as response '''

    query =  request.GET.get('query', '')
    all_songs_queryset = Song.objects.all()
    paginator = Paginator(all_songs_queryset, 10)
    count = paginator.count
    try:
        result = paginator.page(1)
    except EmptyPage:
        result = paginator.page(paginator.num_pages)

    paginated_song_list = result.object_list

    normalize_data = SongListSerializer(paginated_song_list, many=True).data
    return Response({'count': count, 'data':normalize_data})