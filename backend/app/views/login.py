from rest_framework import viewsets, permissions, views, status
from rest_framework.response import Response



class LoginView(views.APIView):
    def post(self, request, **kwargs):
        attempt = LoginAttempt(phone_number=request.data['phone_number'])
        attempt.save()
        return Response(attempt.id)