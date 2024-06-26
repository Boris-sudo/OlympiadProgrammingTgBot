import requests

api_url = 'http://localhost:8000/api/{}/'


def api(method, endpoint, **kwargs):
    resp = requests.request(method, api_url.format(endpoint), **kwargs)
    resp.raise_for_status()
    return resp


def create_account(user_id, username):
    result = api('POST', f"create-account", data={'user_id': user_id, 'username': username})
    return result


def get_account(user_id):
    result = api("GET", f"login", params={'user_id': user_id}).json()
    return result['result']


def get_opponent(user_id):
    return api("GET", f"get_opponent", params={'user_id': user_id})


def get_daily_problem(user_id):
    result = api("GET", f"codeforces/daily-task", params={'user_id': user_id}).json()
    return result['result']


def get_problemset(user_id, rating):
    result = api("GET", f"codeforces/problemset", params={'rating': rating, 'user_id': user_id}).json()
    return result['result']


def get_olympiads():
    result = api("GET", f'olympiads').json()
    return result['result']


def get_topics():
    result = api("GET", f'topics').json()
    return result['result']


def create_new_fight(user_id):
    result = api('POST', f"fight", data={'user_id': user_id})
    return result


def delete_fight(user_id):
    result = api('DELETE', f"fight", data={'user_id': user_id})
    return result


def give_up_fight(user_id):
    result = api('POST', f"fight/give-up", data={'user_id': user_id})
    return result


def check_solution(user_id):
    result = api('POST', f"fight/check", data={'user_id': user_id})
    return result


def get_task(user_id):
    result = api('POST', f"fight/task", data={'user_id': user_id})
    return result


def check_user_in_figth(user_id):
    result = api('POST', f"fight/exist", data={'user_id': user_id})
    return result
