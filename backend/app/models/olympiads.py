from django.db import models


def generate_olympiads():
    Olympiad.objects.create(name='ВОШ', link='https://vos.olimpiada.ru/')
    Olympiad.objects.create(name='Шаг в будущее', link='https://lk-olymp.bmstu.ru/availabletests')
    Olympiad.objects.create(name='Высшая проба', link='https://olymp.hse.ru/mmo/instr-reg')
    Olympiad.objects.create(name='Когнитивные технологии', link='https://olymp.misis.ru/')
    Olympiad.objects.create(name='ИТМО', link='https://olymp.itmo.ru/')
    Olympiad.objects.create(name='СПБГУ', link='https://olympiada.spbu.ru/')
    Olympiad.objects.create(name='Innopolis Open', link='https://dovuz.innopolis.university/io-informatika/')
    Olympiad.objects.create(name='Технокубок', link='https://techno-cup.ru/')
    Olympiad.objects.create(name='ВузАк олимпиада', link='https://sp.urfu.ru/vuzakadem/inform/2024/')
    Olympiad.objects.create(name='МОШ', link='https://mos-inf.olimpiada.ru/')
    Olympiad.objects.create(name='ИОИП', link='https://neerc.ifmo.ru/school/ioip/index.html')


class Olympiad(models.Model):
    name = models.CharField(max_length=1000, unique=True, blank=False, null=False, verbose_name="olympiad name")
    link = models.CharField(max_length=1000, blank=False, null=False, verbose_name="olympiad link")
    description = models.TextField(blank=False, null=False, verbose_name="olympiad description")

