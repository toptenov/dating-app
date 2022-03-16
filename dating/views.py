from PIL import Image
from rest_framework import status
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apptrix import settings
from dating.models import Client, Match
from dating.serializers import ClientSerializer, MatchSerializer


def add_watermark(input_image_path):
    base_image = Image.open(input_image_path)
    watermark = Image.open(settings.MEDIA_ROOT + '/watermark/watermark.png')
    watermark.putalpha(120)
    width, height = base_image.size

    transparent = Image.new('RGB', (width, height), (0, 0, 0))
    transparent.paste(base_image, (0, 0))
    transparent.paste(watermark, (0, 0), mask=watermark)
    transparent.save(input_image_path)


class ClientAPIView(CreateAPIView):
    def post(self, request):
        serializer = ClientSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        # Set a hashed password:
        client = Client.objects.get(pk=serializer.data["id"])
        client.set_password(request.data.get("password"))
        client.save()

        input_image_path = settings.MEDIA_ROOT + '/' + str(client.avatar)
        add_watermark(input_image_path)

        return Response({'client': serializer.data})


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
