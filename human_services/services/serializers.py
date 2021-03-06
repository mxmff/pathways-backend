from rest_framework import serializers
from human_services.services import models


class ServiceSerializer(serializers.HyperlinkedModelSerializer):
    organization_url = serializers.CharField(read_only=True, source='organization.website')
    organization_email = serializers.CharField(read_only=True, source='organization.email')

    class Meta:
        model = models.Service
        fields = ('id', 'name', 'organization_id', 'description', 'organization_url', 'organization_email')
