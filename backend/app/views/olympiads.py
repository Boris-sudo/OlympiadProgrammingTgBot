import random
from datetime import date

from django.http import JsonResponse

from ..models import Olympiad
from ..models.olympiads import generate_olympiads


def get_olyampiads(request):
    if request.method == 'GET':
        result = Olympiad.objects.get_all()
        if result is None:
            generate_olympiads()
            result = Olympiad.objects.get_all()
        print(result)
        return JsonResponse({'result': result}, status=200)
    return JsonResponse({'result': 'failed'}, status=400)
