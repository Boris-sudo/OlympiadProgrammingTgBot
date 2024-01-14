from redis import Redis
from rq_scheduler import Scheduler
import time
import datetime

from backend.app.classes.codeforces_request import CodeforcesRequest
from backend.app.classes.rating_change import change_rating_by_daily_task
from backend.app.models import *


def daily_tasks_checker():
    daily_solvers = DailyTaskSolvers.objects.all()
    codeforces_request = CodeforcesRequest()
    yesterday = datetime.date.today() - datetime.timedelta(days=1)

    for daily_task_solver in daily_solvers:
        if daily_solvers.task.date == yesterday:
            profiles = Profile.objects.filter(daily_solver=daily_task_solver)
            task_contestId = daily_task_solver.task.contestId
            task_index = daily_task_solver.task.index

            for prof in profiles:
                last = 1
                done = True
                found = False
                tries_count = 0
                # finding task in last sends of this prof
                while done:
                    solved_tasks = codeforces_request.get_solved_tasks(prof.codeforces_name, last, 10)
                    last += 10
                    for solved_task in solved_tasks:
                        time_unix = solved_task['creationTime']
                        time_datetime = time.strftime("%Y-%m-%d", time.localtime(time_unix))
                        if time_datetime == yesterday:
                            if solved_task['verdict'] == 'OK' and solved_task['problem']['index'] == task_index and \
                                    solved_task['problem']['contestId'] == task_contestId:
                                found = True
                            elif solved_task['problem']['index'] == task_index and solved_tasks[
                                'contestId'] == task_contestId:
                                tries_count += 1
                        else:
                            done = False
                            break
                # changing rating of this prof
                new_rating = 0
                if found:
                    current_rating = prof['rating']
                    new_rating = change_rating_by_daily_task(current_rating, daily_task_solver.task.rating, done=True,
                                                             tries_count=tries_count)
                else:
                    current_rating = prof['rating']
                    new_rating = change_rating_by_daily_task(current_rating, daily_task_solver.task.rating, done=True,
                                                             tries_count=tries_count)
                rating_change = RatingChanges(date=yesterday, rating=new_rating, profile=prof)
                prof.rating = new_rating
                # clearing
                prof.daily_solver = None
            # clearing
            daily_solvers.delete()


def check_daily_task_checking_done():
    yesterday = datetime.date.today() - datetime.timedelta(days=1)
    daily_tasks_checking = DailyTaskChecking.objects.all()[0]
    if daily_tasks_checking.last_date == yesterday:
        return

    daily_tasks_checker()
    daily_tasks_checking.last_date = yesterday


# redis_conn = Redis()
# scheduler = Scheduler(connection=redis_conn)
# scheduler.schedule("18:25", daily_tasks_checker, repeat=None, interval=86400)
