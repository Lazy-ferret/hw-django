from django_filters import DateFromToRangeFilter, FilterSet, ModelChoiceFilter
from django_filters.rest_framework import DjangoFilterBackend

from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from advertisements.models import Advertisement
from advertisements.permissions import IsOwnerOrReadOnly
from advertisements.serializers import AdvertisementSerializer

from django.contrib.auth import get_user_model

User = get_user_model()


class DateFilter(FilterSet):
    created_at = DateFromToRangeFilter()
    # creator = ModelChoiceFilter(queryset=Advertisement.objects.all())
    creator = ModelChoiceFilter(queryset=User.objects.all())
    # creator = DjangoFilterBackend()
    # status = DjangoFilterBackend()

    class Meta:
        model = Advertisement
        fields = ['created_at', 'creator', 'status']


class AdvertisementViewSet(ModelViewSet):
    """ViewSet для объявлений."""

    queryset = Advertisement.objects.all()
    serializer_class = AdvertisementSerializer
    # filter_backends = [DjangoFilterBackend]
    # filterset_fields = ['creator', 'status']
    filterset_class = DateFilter

    def get_permissions(self):
        """Получение прав для действий."""
        if self.action in ["create", "update", "partial_update", "destroy"]:
            return [IsAuthenticated(), IsOwnerOrReadOnly()]
        return []
