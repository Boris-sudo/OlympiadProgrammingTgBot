import random
import json
import time
from multiprocessing.connection import Client

from django.db import models
from .profile import Profile
from ..classes.codeforces_request import CodeforcesRequest


def send_socket_text(text: str, address):
    while True:
        try:
            conn = Client(address)
            conn.send(text)
            print(text, ' send to', address)
            return
        except:
            pass


class Task(models.Model):
    contestId = models.IntegerField(blank=False, null=False)
    index = models.CharField(max_length=10, blank=False, null=False)
    name = models.CharField(max_length=100, blank=False, null=False)
    rating = models.IntegerField(blank=False, null=False)


class Fight(models.Model):
    class Status(models.IntegerChoices):
        NOT_STARTED = 0
        SEARCHING_FOR_OPPONENT = 1
        IN_PROGRESS = 2
        WINNER1 = 11
        WINNER2 = 12
        DRAW = 10

    user1 = models.ForeignKey(Profile, on_delete=models.DO_NOTHING, blank=False, null=False, related_name='user1')
    user2 = models.ForeignKey(Profile, on_delete=models.DO_NOTHING, blank=True, null=True, related_name='user2')
    task = models.ForeignKey(Task, on_delete=models.CASCADE, blank=True, null=True)
    status = models.IntegerField(choices=Status.choices, default=Status.SEARCHING_FOR_OPPONENT)

    def update_rating(self, done: bool, user):
        change = (1 if done else -1)
        rating_dif = self.user1.rating - self.user2.rating
        task_rating = self.task.rating

        if rating_dif < -150:
            rating_dif += 300
        elif rating_dif < 150:
            rating_dif += 200

        if user == self.user1:
            change *= rating_dif * task_rating / 800
        else:
            change *= -1 * rating_dif * task_rating / 800

        return change

    def __str__(self):
        try:
            return f"fight between {self.user1.codeforces_name} and {self.user2.codeforces_name}"
        except:
            return f'waiting for opponent {self.user1.codeforces_name}'

    def lose(self, user):
        print('giving up user: ', user)
        if user == self.user1:
            address1 = ('127.0.0.1', self.user1.port)
            address2 = ('127.0.0.1', self.user2.port)
            send_socket_text('finished', address1)
            send_socket_text('correct', address2)
            self.user1.rating += self.update_rating(False, self.user1)
            self.user2.rating += self.update_rating(True, self.user2)
        else:
            address1 = ('127.0.0.1', self.user1.port)
            address2 = ('127.0.0.1', self.user2.port)
            send_socket_text('correct', address1)
            send_socket_text('finished', address2)
            self.user1.rating += self.update_rating(True, self.user1)
            self.user2.rating += self.update_rating(False, self.user2)
        self.delete()
        print('gived up')

    def start(self, user2: Profile):
        address1 = ('127.0.0.1', self.user1.port)
        address2 = ('127.0.0.1', user2.port)
        send_socket_text('done', address1)
        send_socket_text('done', address2)
        self.user2 = user2
        self.status = self.Status.IN_PROGRESS
        self.task = self.find_task()
        self.save()

    def find_task(self):
        average_rating = (self.user1.rating + self.user2.rating) / 2
        codeforces_request = CodeforcesRequest()
        response = codeforces_request.get_problemset()
        result_response = []
        problems = response['problems']
        for problem in problems:
            try:
                print('===================================================================================================')
                print(problem)
                print(abs(problem['rating'] - average_rating))
                print(self.find_task_in_user(problem, self.user1.codeforces_name))
                print(self.find_task_in_user(problem, self.user2.codeforces_name))
                if (abs(problem['rating'] - average_rating) <= 200 and
                        self.find_task_in_user(problem, self.user1.codeforces_name) == 'not found' and
                        self.find_task_in_user(problem, self.user2.codeforces_name) == 'not found'):
                    result_response.append(problem)
                    break
            except:
                pass
        problem = random.choice(result_response)
        result_task = Task.objects.create(contestId=problem['contestId'], index=problem['index'], name=problem['name'],
                                          rating=problem['rating'])
        return result_task

    @staticmethod
    def find_task_in_user(task, username: str):

        codeforces = CodeforcesRequest()
        last_index = 1
        try:
            problemset = codeforces.get_solved_tasks(username, last_index, 10)
            last_index += 10
            for problem in problemset:
                try:
                    contestId = task['contestId']
                    index = task['index']
                    name = task['name']
                except:

                    contestId = task.contestId
                    index = task.index
                    name = task.name

                try:
                    print(contestId, index, name)
                    print(problem['problem'])
                    if problem['problem']['contestId'] == contestId and problem['problem']['index'] == index and problem['problem']['name'] == name:
                        return 'found'
                except:
                    pass
        except:
            return 'not found'
        return 'not found'

    def check_solution(self, user):
        resp = self.find_task_in_user(self.task, user.codeforces_name)
        print(resp)
        if resp == 'not found':
            address = ('127.0.0.1', user.port)
            send_socket_text('wrong', address)
        elif user == self.user1:
            address1 = ('127.0.0.1', self.user1.port)
            address2 = ('127.0.0.1', self.user2.port)
            send_socket_text('correct', address1)
            send_socket_text('finished', address2)
            self.user1.rating += self.update_rating(True, self.user1)
            self.user2.rating += self.update_rating(False, self.user2)
            self.delete()
        else:
            address1 = ('127.0.0.1', self.user1.port)
            address2 = ('127.0.0.1', self.user2.port)
            send_socket_text('finished', address1)
            send_socket_text('correct', address2)
            self.user1.rating += self.update_rating(False, self.user1)
            self.user2.rating += self.update_rating(True, self.user2)
            self.delete()


