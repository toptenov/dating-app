from rest_framework import status
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from dating.models import Client
from dating.serializers import ClientSerializer


class ClientAPIView(CreateAPIView):
    def post(self, request):
        serializer = ClientSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            client = Client()
            client.email = request.data.get("email")
            client.set_password(request.data.get("password"))
            client.first_name = request.data.get("first_name")
            client.last_name = request.data.get("last_name")
            client.is_male = request.data.get("is_male")
            client.save()
            return Response({'client': ClientSerializer(client).data})


class ClientListAPIView(ListAPIView):
    def get(self, request):
        clients = Client.objects.all()
        if "is_male" in request.query_params:
            clients = clients.filter(is_male=bool(eval(request.query_params["is_male"].capitalize())))
        if "first_name" in request.query_params:
            clients = clients.filter(first_name=request.query_params["first_name"])
        if "last_name" in request.query_params:
            clients = clients.filter(last_name=request.query_params["last_name"])
        serializer = ClientSerializer(clients, many=True)
        return Response({'clients': serializer.data})

    permission_classes = (IsAuthenticated,)

class ClientRetrieveAPIView(RetrieveAPIView):
    def get(self, request, **kwargs):
        pk = kwargs["pk"]

        try:
            client = Client.objects.get(pk=pk)
            serializer = ClientSerializer(client)
        except:
            return Response({"error": "Нет такого клиента, ID =" + str(pk)})

        return Response({"client": serializer.data})

    permission_classes = (IsAuthenticated,)


class LogoutAPIView(APIView):
    def get(self, request, format=None):
        request.user.auth_token.delete()
        return Response(status=status.HTTP_200_OK)
