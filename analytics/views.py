from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.core.paginator import Paginator, EmptyPage
from .serializers import SongListSerializer
from .models import Song


# Create your views here.

@api_view(['GET'])
def list_songs(request):
    ''' send paginated list of songs list as response '''

    query =  request.GET.get('query', '')
    page_no = request.GET.get('page', 1)

    try:
        if query:
            paginator = Paginator(Song.objects.filter(title__icontains=query), 10)
        else:
            all_songs_queryset = Song.objects.all()
            paginator = Paginator(all_songs_queryset, 10)
        count = paginator.count
        try:
            result = paginator.page(page_no)
        except EmptyPage:
            result = paginator.page(paginator.num_pages)

        paginated_song_list = result.object_list

        normalize_data = SongListSerializer(paginated_song_list, many=True).data
        return Response({'count': count, 'data': normalize_data}, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({'message': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
def submit_song_rating(request):
    """ user can submit song rating """

    try:
        song_id = request.data.get('song_id', None)
        user_song_rating = request.data.get('rating', None)

        required_fields = ['song_id', 'rating']

        for field in required_fields:
            if field not in request.data:
                return Response({'message': f'{field} is Required'},status=status.HTTP_400_BAD_REQUEST)

        # todo song_rating validation

        song_to_update = Song.objects.get(song_id=song_id)
        song_to_update.song_rating = user_song_rating
        song_to_update.save()

        return Response( {'message': 'Updated Successfully'},status=status.HTTP_202_ACCEPTED)

    except Exception as e:
        return Response({'message': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
