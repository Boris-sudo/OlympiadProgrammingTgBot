import requests

api_url = 'https://localhost:8000/api/{}/'


def api(method, endpoint, data=None):
    resp = requests.request(method, api_url.format(endpoint), data=data)
    resp.raise_for_status()
    return resp
