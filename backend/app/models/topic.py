from django.db import models


class Topic(models.Model):
    name = models.CharField(max_length=1000, blank=False, null=False, verbose_name='topic name')
    link = models.CharField(max_length=1000, blank=False, null=False, verbose_name='topic link')


class TopicArchive(models.Model):
    name = models.CharField(max_length=1000, blank=False, null=False, verbose_name='topic archive name')
    children = models.ManyToManyField(Topic, blank=True, verbose_name='topic archive children')


def generate_topics():
    # data structures
    DO = Topic.objects.create(name='Дерево отрезков', link='https://e-maxx.ru/algo/segment_tree')
    Sqrt = Topic.objects.create(name='Sqrt-декомпозиция', link='https://e-maxx.ru/algo/sqrt_decomposition')
    Fenvik = Topic.objects.create(name='Дерево Фенвика', link='https://e-maxx.ru/algo/fenwick_tree')
    SNM = Topic.objects.create(name='СНМ', link='https://e-maxx.ru/algo/dsu')
    DekD = Topic.objects.create(name='Декартово дерево', link='https://e-maxx.ru/algo/treap')
    RandSh = Topic.objects.create(name='Рандомизированная куча', link='https://e-maxx.ru/algo/randomized_heap')

    struct = TopicArchive.objects.create(name='Структуры данных')
    struct.children.set([DO, Sqrt, Fenvik, SNM, DekD, RandSh])
    # strigns
    ZFun = Topic.objects.create(name='Z-функция', link='https://e-maxx.ru/algo/z_function')
    PrefFun = Topic.objects.create(name='Перфикс-функция', link='https://e-maxx.ru/algo/prefix_function')
    HashAlgs = Topic.objects.create(name='Алгоритмы хэширования', link='https://e-maxx.ru/algo/string_hashes')
    RabinKarp = Topic.objects.create(name='Алгоритм Рабин-Карпа', link='https://e-maxx.ru/algo/rabin_karp')
    SufMass = Topic.objects.create(name='Суффиксный массив', link='https://e-maxx.ru/algo/suffix_array')
    SufAuto = Topic.objects.create(name='Суффиксный автомат', link='https://e-maxx.ru/algo/suffix_automata')
    Pal = Topic.objects.create(name='Нахождение всех подпалиндромов', link='https://e-maxx.ru/algo/palindromes_count')
    AhoKar = Topic.objects.create(name='Ахо-Корасик', link='https://e-maxx.ru/algo/aho_corasick')
    SufTree = Topic.objects.create(name='Суффиксное дерево', link='https://e-maxx.ru/algo/ukkonen')

    strings = TopicArchive.objects.create(name='Алгоритмы на строках')
    strings.children.set([ZFun, PrefFun, HashAlgs, RabinKarp, SufAuto, SufMass, Pal, AhoKar, SufTree])
    # graphs
