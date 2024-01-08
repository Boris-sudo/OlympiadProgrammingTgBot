import random
from datetime import date

from django.http import JsonResponse
from django.shortcuts import render

from ..classes import CodeforcesRequest
from ..models import DailyTask


def find_task_in_problemset(problemset, task):
    for problem in problemset:
        for i in task:
            same = True
            if problem[i] != task[i]:
                same = False
            if same:
                return problem


def problemset(request):
    if request.method == 'GET':
        # rating = request.data['rating']
        rating = None
        if rating is None:
            rating = 1400
        codeforces_request = CodeforcesRequest()
        response = codeforces_request.get_problemset()
        result_response = []
        problems = response['result']['problems']
        for problem in problems:
            try:
                if abs(problem['rating'] - rating) <= 200:
                    result_response.append(problem)
            except:
                pass
        return JsonResponse({'result': result_response}, status=200)


def daily_task(request):
    if request.method == 'GET':
        rating = None
        if rating is None:
            rating = 1400
        codeforces_request = CodeforcesRequest()
        response = codeforces_request.get_problemset()

        now_date = date.today()
        print(now_date)
        result_task = None
        ''' GETTING DAILY TASK '''
        result_task = DailyTask.objects.filter(date=now_date, rating=rating).first()
        print(result_task)
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
                try:
                    DailyTask.get(rating=result_task['rating'], contestId=result_task['contestId'],
                                  index=result_task['index'])
                except:
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
            result_task = find_task_in_problemset(response['result']['problems'], {'rating': task_rating, 'contestId': task_contestId, 'index': task_index})
            print(result_task)
        return JsonResponse({'result': result_task}, status=200)
