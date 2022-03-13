from rest_framework.generics import CreateAPIView
from rest_framework.response import Response

from dating.models import Client
from dating.serializers import ClientSerializer


class ClientAPIView(CreateAPIView):
    def post(self, request):
        serializer = ClientSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            client = Client()
            client.email = request.data.get("email")
            client.set_password(request.data.get("password"))
            client.full_name = request.data.get("full_name")
            client.is_male = request.data.get("is_male")
            client.save()
            return Response({'client': ClientSerializer(client).data})
