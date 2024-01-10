import random
from datetime import date

from django.http import JsonResponse

from ..models import Olympiad
from ..models.olympiads import generate_olympiads


def get_olyampiads(request):
    if request.method == 'GET':
        olympiads = Olympiad.objects.all()
        if len(olympiads) == 0:
            generate_olympiads()
            olympiads = Olympiad.objects.all()

        result = []
        for olympiad in olympiads:
            result.append({'name': olympiad.name, 'link': olympiad.link})
        print(result)
        print()
        print()
        return JsonResponse({'result': result}, status=200)
    return JsonResponse({'result': 'failed'}, status=400)
