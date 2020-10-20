from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework import mixins, generics
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.response import Response
from bonds.models import Bond
from bonds.serializer import BondSerializer
from rest_framework.renderers import JSONRenderer
from rest_framework import status
import requests
import json
from bonds.bonds_filter import BondFilter
from rest_framework.decorators import permission_classes
from django.contrib.auth.models import User


class HelloWorld(APIView):
    def get(self, request):
        return Response("Hello World")


def get_legal_name(data):
    GLEIF_URL = 'https://leilookup.gleif.org/api/v2/leirecords?lei={lei}'
    lei = data['lei']
    url = GLEIF_URL.format(lei=lei)
    response = requests.get(url)
    if response.status_code == 200:
        json_obj = json.loads(response.content)
        legal_name = ''
        for result in json_obj:
            legal_name = result['Entity']['LegalName']['$']
        return legal_name
    else:
        return None


def get_user(request):
    user = User.objects.get(id=request.user.id)
    return user


@permission_classes([IsAuthenticated])
class BondView(mixins.ListModelMixin, mixins.CreateModelMixin,
               generics.GenericAPIView):
    serializer_class = BondSerializer
    renderer_classes = [JSONRenderer]
    filter_backends = (DjangoFilterBackend,)
    filter_class = BondFilter

    def get_queryset(self):
        user = self.request.user
        return Bond.objects.filter(user=user)

    def create(self, request, *args, **kwargs):
        data = request.POST.copy()
        legal_name = get_legal_name(data)
        data['legal_name'] = legal_name
        user = get_user(request)
        data['user'] = user.id
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED,
                        headers=headers)

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)
