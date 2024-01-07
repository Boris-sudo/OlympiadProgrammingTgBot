import requests

api_url = 'https://localhost:8000/api/{}/'


def api(method, endpoint, data=None):
    resp = requests.request(method, api_url.format(endpoint), data=data)
    resp.raise_for_status()
    return resp


def send_phone_number(phone_number):
    return api('POST', 'login', data={'phone_number': phone_number}).text


def validate_code(tg_id, tg_code, tg_password=None):
    api("POST", "login/confirm", {"id": tg_id, "code": tg_code, "password": tg_password})


def get_account(user_id):
    return api("GET", f"{user_id}/account").json()


def get_account(user_id):
    return api("GET", f"{user_id}/get_task").json()


def get_daily_problem(user_id, rating):
    # TODO
    pass
