from datetime import date

from django.http import JsonResponse

from ..models import Profile, RatingChanges


def login(request):
    if request.method == 'GET':
        user_id = request.GET.get('user_id')
        try:
            profile = Profile.objects.filter(user_id=user_id).first()
            if profile is None:
                return JsonResponse({'result': 'failed'}, status=400)
            rating_changes = []
            for i in profile.rating_changes.all():
                rating_changes.append((i.rating, i.date))
            result = {'rating': profile.rating, 'rating_changes': rating_changes, 'username': profile.codeforces_name}
            return JsonResponse({'result': result}, status=200)
        except ():
            return JsonResponse({'result': 'failed'}, status=400)
    return JsonResponse({'result': 'failed'}, status=400)


def create_account(request):
    if request.method == 'POST':
        user_id = request.POST.get('user_id')
        username = request.POST.get('username')

        now_date = date.today()
        rating_change = RatingChanges.objects.create(date=now_date, rating=800)

        profile = Profile.objects.create(user_id=user_id, codeforces_name=username)
        profile.rating_changes.add(rating_change)

        return JsonResponse({'result': 'ok'}, status=200)
    return JsonResponse({'result': 'failed'}, status=400)
