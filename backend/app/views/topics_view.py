from django.http import JsonResponse

from ..models import Topic, TopicArchive
from ..models.topic import generate_topics


def get_topics(request):
    if request.method == 'GET':
        topics = TopicArchive.objects.all()
        if len(topics) == 0:
            generate_topics()
            topics = TopicArchive.objects.all()
        result = []
        for topic in topics:
            result.append({'name': topic.name, 'children': []})
            for child in topic.children.all():
                result[-1]['children'].append({'name': child.name, 'link': child.link})
        return JsonResponse({'result': result}, status=200)
    return JsonResponse({'result': 'failed'}, status=400)
