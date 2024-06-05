import random
from datetime import date

from django.http import JsonResponse

from ..classes import CodeforcesRequest
from ..models import DailyTask, Profile, DailyTaskSolvers


def find_task_in_problemset(problems, task):
    for problem in problems:
        same = True
        for i in task:
            try:
                pi = problem[i]
                ti = task[i]
            except:
                same = False
                break
            if problem[i] != task[i]:
                same = False
                break
        if same:
            return problem


def problemset(request):
    if request.method == 'GET':
        rating = int(request.GET.get('rating'))
        codeforces_request = CodeforcesRequest()
        response = codeforces_request.get_problemset()
        result_response = []
        problems = response['problems']
        for problem in problems:
            try:
                if abs(problem['rating'] - rating) <= 200:
                    result_response.append(problem)
            except:
                pass
        return JsonResponse({'result': result_response}, status=200)


def daily_task(request):
    today = date.today()
    if request.method == 'GET':
        user_id = int(request.GET.get('user_id'))
        account = Profile.objects.filter(user_id=user_id).first()
        rating = account.rating
        if rating < 800:
            rating = 800
        codeforces_request = CodeforcesRequest()
        response = codeforces_request.get_problemset()

        ''' GETTING DAILY TASK '''
        result_task = DailyTask.objects.filter(date=today, rating=rating).first()
        if result_task is None:
            # getting all available new daily tasks
            available_problems = []
            for problem in response['problems']:
                try:
                    if abs(problem['rating'] - rating) <= 100:
                        available_problems.append(problem)
                except:
                    pass
            # checker that this task wasn't already a daily task
            while True:
                result_task = random.choice(available_problems)
                same_task_in_db = DailyTask.objects.filter(rating=result_task['rating'], contestId=result_task['contestId'],
                                                       index=result_task['index']).first()
                if same_task_in_db is None:
                    break
            # creating db-element with this daily task
            task = DailyTask.objects.create(
                date=today,
                rating=result_task['rating'],
                contestId=result_task['contestId'],
                index=result_task['index']
            )
            daily_task_solvers = DailyTaskSolvers.objects.create(
                task=task,
            )
            account.daily_solver = daily_task_solvers
            account.save()
        else:
            daily_task_solvers = DailyTaskSolvers.objects.filter(task=result_task).first()
            task_rating = result_task.rating
            task_contestId = result_task.contestId
            task_index = result_task.index
            result_task = find_task_in_problemset(response['problems'],
                                                  {'rating': task_rating, 'contestId': task_contestId,
                                                   'index': task_index})
            account.daily_solver = daily_task_solvers
            account.save()

        return JsonResponse({'result': result_task}, status=200)
    return JsonResponse({'result': 'failed'}, status=400)
