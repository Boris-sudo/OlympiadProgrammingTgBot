import requests


class CodeforcesRequest:
    api_url = 'https://codeforces.com/api/{}/'

    def api(self, endpoint):
        resp = requests.request("GET", self.api_url.format(endpoint))
        resp.raise_for_status()
        return resp

    def get_problemset(self):
        problemset = self.api('problemset.problems')
        print(problemset)