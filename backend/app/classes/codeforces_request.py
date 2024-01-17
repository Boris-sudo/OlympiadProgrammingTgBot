import requests


class CodeforcesRequest:
    api_url = 'https://codeforces.com/api/{}'

    def api(self, endpoint):
        resp = requests.request("GET", self.api_url.format(endpoint))
        resp.raise_for_status()
        return resp.json()

    def get_problemset(self):
        problemset = self.api('problemset.problems/')
        return problemset['result']

    def get_solved_tasks(self, username, from_num: int = 1, count_num: int = 100):
        result = self.api(f'user.status?handle={username}&from={from_num}&count={count_num}')['result']
        return result
