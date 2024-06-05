import datetime
import random
import os
from pathlib import Path
import matplotlib.pyplot as plt
import datetime as dt


def generate_filename():
    now = datetime.datetime.now().strftime("%Y-%m-%d-%h-%M-%S")
    result = now + '-' + str(random.randint(1, 1000000000000))
    return result


def delete_files_in_folder(folder_path):
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        try:
            if os.path.isfile(file_path):
                os.remove(file_path)
        except Exception as e:
            print(f'Ошибка при удалении файла {file_path}. {e}')


def generate_rating_diagram(rating_changes: [[int, str]] = None, filepath: str = ""):
    folder = Path('/home/boriskiva/PycharmProjects/OlympiadProgrammingTgBot/bot/static/generated')
    if len(list(folder.iterdir())) >= 5:
        delete_files_in_folder('/home/boriskiva/PycharmProjects/OlympiadProgrammingTgBot/bot/static/generated')

    y, x = [], []
    for i in rating_changes:
        y.append(i[0])
        x.append(i[1])

    x = [dt.datetime.strptime(i, "%Y-%m-%d") for i in x]

    plt.plot(x, y, color='blue', linewidth=2, markersize=8, marker='o', animated=True)
    plt.xticks(rotation=90)
    plt.savefig(filepath)
    plt.close()
