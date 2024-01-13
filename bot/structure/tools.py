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

    print(x)
    print(y)
    x = [dt.datetime.strptime(i, "%Y-%m-%d") for i in x]
    df = pd.DataFrame({"date": x, "value": y})

    result = sns.lineplot(x='date', y='value', data=df, markers=True, dashes=False)
    plt.xticks(rotation=90)
    plt.tight_layout()
    plt.savefig(filepath)
