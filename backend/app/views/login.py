import random
from datetime import date

from django.http import JsonResponse

from ..models import Profile, RatingChanges
from ..classes import check_daily_task_checking_done


def login(request):
    check_daily_task_checking_done()
    if request.method == 'GET':
        user_id = request.GET.get('user_id')
        print(user_id)
        try:
            profile = Profile.objects.filter(user_id=user_id).first()
            print(profile)
            if profile is None:
                return JsonResponse({'result': 'failed'}, status=400)
            rating_changes = []
            rating_changes_obj = RatingChanges.objects.filter(profile=profile).all()
            for i in rating_changes_obj:
                rating_changes.append((i.rating, i.date))
            result = {'rating': profile.rating, 'rating_changes': rating_changes, 'username': profile.codeforces_name, 'port': profile.port}
            return JsonResponse({'result': result}, status=200)
        except ():
            return JsonResponse({'result': 'failed'}, status=400)
    return JsonResponse({'result': 'failed'}, status=400)


def gen_port():
    while True:
        port = random.randint(0, 9999)
        try:
            user = Profile.objects.get(port=port)
            if user is None:
                return port
        except:
            return port


def create_account(request):
    if request.method == 'POST':
        user_id = request.POST.get('user_id')
        username = request.POST.get('username')

        now_date = date.today()
        profile = Profile.objects.create(user_id=user_id, codeforces_name=username, port=gen_port())
        rating_change = RatingChanges.objects.create(date=now_date, rating=800, profile=profile)
        return JsonResponse({'result': 'ok'}, status=200)
    return JsonResponse({'result': 'failed'}, status=400)
