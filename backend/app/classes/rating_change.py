"""
let's change rating  base on:
 - current rating
 - solved_task_rating
 - tries_count
"""


def change_rating_by_daily_task(current_rating: int, task_rating: int, done: bool = True, tries_count: int = 1):
    sign = 1 if done else -1
    new_rating = current_rating + sign * ((task_rating - current_rating + 200) / 100) * 25 / tries_count
    return new_rating
