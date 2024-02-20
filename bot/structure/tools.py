import datetime
import random
import time

import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
import datetime as dt
from PIL import Image


def generate_filename():
    now = datetime.datetime.now().strftime("%Y-%m-%d-%h-%M-%S")
    result = now + '-' + str(random.randint(1, 1000000000000))
    return result


def generate_rating_diagram(rating_changes: [[int, str]] = None, filepath: str = ""):
    y, x = [], []
    for i in rating_changes:
        y.append(i[0])
        x.append(i[1])

    x = [dt.datetime.strptime(i, "%Y-%m-%d") for i in x]
    print(x)
    print(y)

    plt.plot(x, y, color='blue', linewidth=2, markersize=8, marker='o', animated=True)
    plt.xticks(rotation=90)
    plt.savefig(filepath)
    plt.close()
