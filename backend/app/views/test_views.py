import json

from django.shortcuts import render
from ..classes import CodeforcesRequest


def show_list(request):
    codeforces_request = CodeforcesRequest()
    response = codeforces_request.get_problemset()
    result_response = []
    problems = response['result']['problems']
    for i in problems:
        print(i)
        if i['rating'] == 1400:
            result_response.append(i)
    return render(request, "test.html", {'response': problems})
