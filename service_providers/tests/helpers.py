from decimal import Decimal
from service_providers import models

class ServiceProviderBuilder:
    def __init__(self):
        self.name = ''
        self.latitude = Decimal('0.0')
        self.longitude = Decimal('0.0')
        self.description = ''

    def with_name(self, name):
        self.name = name
        return self

    def with_latitude(self, latitude):
        self.latitude = latitude
        return self

    def with_longitude(self, longitude):
        self.longitude = longitude
        return self

    def with_description(self, description):
        self.description = description
        return self

    def build(self):
        result = models.ServiceProvider()
        result.name = self.name
        result.latitude = self.latitude
        result.longitude = self.longitude
        result.description = self.description
        return result