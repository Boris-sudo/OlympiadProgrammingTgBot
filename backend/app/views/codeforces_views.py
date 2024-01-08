import random

from django.http import JsonResponse
from django.shortcuts import render

from ..classes import CodeforcesRequest


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

        # TODO check that problem is not solved
        available_problems = []
        for problem in response['result']['problems']:
            try:
                if abs(problem['rating'] - rating) <= 200:
                    available_problems.append(problem)
            except:
                pass
        return JsonResponse({'result': available_problems[random.randint(0,len(available_problems))]}, status=200)
