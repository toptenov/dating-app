from rest_framework import status
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from dating.models import Client, Match
from dating.serializers import ClientSerializer, MatchSerializer


class ClientAPIView(CreateAPIView):
    def post(self, request):
        serializer = ClientSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            client = Client()
            client.email = request.data.get("email")
            client.set_password(request.data.get("password"))
            client.first_name = request.data.get("first_name")
            client.last_name = request.data.get("last_name")
            client.avatar = request.data.get("avatar")
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


class MatchCreateAPIView(CreateAPIView):
    def post(self, request, pk):
        serializer = MatchSerializer(data={"subject_id": request.user.pk, "object_id": pk})
        serializer.is_valid(raise_exception=True)
        serializer.save()

        try:
            match = Match.objects.filter(subject=serializer.instance.object,
                                         object=serializer.instance.subject)
        finally:
            if match:
                full_name = serializer.instance.object.first_name + serializer.instance.object.last_name
                Client.objects.get(pk=pk).email_user(
                    subject="There's a new match!",
                    message=f"Вы понравились {full_name}! Почта участника: {serializer.instance.object.email}",
                    from_email=serializer.instance.object.email
                )
                return Response({'match': serializer.instance.object.email})
            else:
                return Response({'match': serializer.data})


class LogoutAPIView(APIView):
    def get(self, request, format=None):
        request.user.auth_token.delete()
        return Response(status=status.HTTP_200_OK)
