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


def daily_task(request):
    if request.method == 'GET':
        rating = None
        if rating is None:
            rating = 1400
        codeforces_request = CodeforcesRequest()
        response = codeforces_request.get_problemset()

        now_date = date.today()
        result_task = None
        ''' GETTING DAILY TASK '''
        result_task = DailyTask.objects.filter(date=now_date, rating=rating).first()
        if result_task is None:
            print("result task doesn't exist yet")
            # getting all available new daily tasks
            available_problems = []
            for problem in response['result']['problems']:
                try:
                    if abs(problem['rating'] - rating) <= 0:
                        available_problems.append(problem)
                except:
                    pass
            # checker that this task wasn't already a daily task
            while True:
                result_task = available_problems[random.randint(0, len(available_problems))]
                same_task_in_db = DailyTask.objects.filter(rating=result_task['rating'], contestId=result_task['contestId'],
                                                       index=result_task['index']).first()
                if same_task_in_db is None:
                    break
            # creating db-element with this daily task
            DailyTask.objects.create(
                date=now_date,
                rating=result_task['rating'],
                contestId=result_task['contestId'],
                index=result_task['index']
            )
        else:
            task_rating = result_task.rating
            task_contestId = result_task.contestId
            task_index = result_task.index
            result_task = find_task_in_problemset(response['result']['problems'],
                                                  {'rating': task_rating, 'contestId': task_contestId,
                                                   'index': task_index})
        return JsonResponse({'result': result_task}, status=200)
