from rest_framework import viewsets
from human_services.locations import models, serializers
from common.filters import ServiceAtLocationProximityFilter

# pylint: disable=too-many-ancestors
class LocationViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = models.Location.objects.all()
    serializer_class = serializers.LocationSerializer


# pylint: disable=too-many-ancestors
class LocationViewSetUnderOrganizations(viewsets.ReadOnlyModelViewSet):
    def get_queryset(self):
        organization_id = self.kwargs['organization_id']
        return models.Location.objects.filter(organization=organization_id)

    serializer_class = serializers.LocationSerializer


class ServiceAtLocationViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = models.ServiceAtLocation.objects.all()
    search_fields = ('location__translations__name', 'service__translations__name')
    serializer_class = serializers.ServiceAtLocationSerializer
    filter_backends = (ServiceAtLocationProximityFilter,)
