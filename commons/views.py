from django.http import HttpResponse
from rest_framework import status

# Create your views here.
def health_check(request):
    return HttpResponse('Success', status=status.HTTP_200_OK, content_type='application/json')