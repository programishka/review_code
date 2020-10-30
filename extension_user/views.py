from django.contrib.auth import get_user_model
from rest_framework import viewsets, permissions, status
from rest_framework.response import Response

from extension_user.serializers import UserSerializer, TransferMoneySerializer
from processing.forms import TransferMoneyForm


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = get_user_model().objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]


class TransferMoneyViewSet(viewsets.ViewSet):
    serializer_class = TransferMoneySerializer
    permission_classes = (permissions.IsAuthenticated, )

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        form = TransferMoneyForm(serializer.data)
        if form.is_valid():
            form.save()

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response('error transfer')
