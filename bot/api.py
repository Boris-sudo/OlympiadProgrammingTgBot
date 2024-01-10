import requests

api_url = 'http://localhost:8000/api/{}/'


def api(method, endpoint, data=None):
    resp = requests.request(method, api_url.format(endpoint), data=data)
    resp.raise_for_status()
    return resp


def send_phone_number(phone_number):
    return api('POST', 'login', data={'phone_number': phone_number}).text


def validate_code(tg_id, tg_code, tg_password=None):
    api("POST", "login/confirm", {"id": tg_id, "code": tg_code, "password": tg_password})


def get_account(user_id):
    return {
        'rating': 1400,
        'rating_changes': [(583, "2021-07-30"), (1213, "2022-10-03"), (1128, "2022-03-20"), (1073, "2022-05-02"),
                           (1177, "2022-05-23"), (1297, "2022-06-14"), (1367, "2022-06-25"), (1400, "2022-08-07")],
    }
    # return api("GET", f"{user_id}/account").json()


def get_daily_problem(user_id, rating):
    return api("GET", f"codeforces/daily-task", {'rating': rating}).json()
    # return api("GET", f"codeforces/{user_id}/daily-task", {'rating': rating}).json()


def get_problemset(user_id, rating):
    return api("GET", f"codeforces/problemset", {'rating': rating}).json()
    # return api("GET", f"/codeforces/{user_id}/problemset", data={'rating': rating}).json()


def get_olympiads():
    return api("GET", f'olympiads').json()


def get_topics():
    return api("GET", f'topics').json()