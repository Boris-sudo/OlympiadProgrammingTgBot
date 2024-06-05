from multiprocessing.connection import Client

from django.http import JsonResponse, QueryDict

from ..models import Profile, Fight
from ..models.fight_user import send_socket_text


def register(request):
    if request.method == 'POST':
        user_id = int(request.POST.get('user_id'))
        user = Profile.objects.get(user_id=user_id)

        for fight in Fight.objects.all():
            if abs(fight.user1.rating - user.rating) <= 200 and fight.user2 is None:
                fight.start(user)
                return JsonResponse({'resp': 'waiting'}, status=200)

        fight = Fight.objects.create(user1=user)
        return JsonResponse({'resp': 'waiting'}, status=200)
    elif request.method == 'DELETE':
        put = QueryDict(request.body)
        user_id = int(put.get('user_id'))
        user = Profile.objects.get(user_id=user_id)

        for fight in Fight.objects.all():
            print(fight.user1)
        fight = Fight.objects.get(user1=user)
        fight.delete()
        address = ('127.0.0.1', user.port)
        send_socket_text('aborted', address)
        return JsonResponse({'resp': 'ok'}, status=200)
    return JsonResponse({'resp': 'failed'}, status=200)


def give_up_fight(request):
    print('give up function')
    user_id = request.POST.get('user_id')
    user = Profile.objects.get(user_id=user_id)
    try:
        fight = Fight.objects.get(user1=user)
    except:
        fight = Fight.objects.get(user2=user)
    fight.lose(user)
    return JsonResponse({}, status=200)


def get_task(request):
    user_id = request.POST.get('user_id')
    user = Profile.objects.get(user_id=user_id)
    try:
        fight = Fight.objects.get(user1=user)
    except:
        fight = Fight.objects.get(user2=user)
    print(fight)
    print(fight.task)
    return JsonResponse({'task': {'name': fight.task.name, 'contestId': fight.task.contestId, 'index': fight.task.index}}, status=200)


def check_fight(request):
    user_id = request.POST.get('user_id')
    user = Profile.objects.get(user_id=user_id)
    try:
        fight = Fight.objects.get(user1=user)
    except:
        fight = Fight.objects.get(user2=user)

    fight.check_solution(user)

    return JsonResponse({}, status=200)


def check_user_in_fight(request):
    user_id = request.POST.get('user_id')
    user = Profile.objects.get(user_id=user_id)
    try:
        fight = Fight.objects.get(user1=user)
        return JsonResponse({'exist': '1'}, status=200)
    except:
        try:
            fight = Fight.objects.get(user2=user)
            return JsonResponse({'exist': '1'}, status=200)
        except:
            return JsonResponse({'exist': '0'}, status=200)
    return  JsonResponse({'exist':'0'}, status=200)
