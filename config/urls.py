from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib import admin
from django.views.generic import TemplateView
from django.views import defaults as default_views
from human_services.organizations.viewsets import OrganizationViewSet
from human_services.locations.viewsets import LocationViewSet, LocationViewSetUnderOrganizations
from human_services.services.viewsets import ServiceViewSet
from rest_framework import routers
from rest_framework_swagger.views import get_swagger_view

def build_router():
    router = routers.DefaultRouter()
    router.register(r'organizations', OrganizationViewSet, base_name='organization')
    router.register(r'organizations/(?P<organization_id>\w+)/locations',
                    LocationViewSetUnderOrganizations, base_name='organization-location')
    router.register(r'locations', LocationViewSet, base_name='location')

    router.register(r'services', ServiceViewSet, base_name='service')
    router.register(r'organizations/(?P<organization_id>\w+)/services', ServiceViewSet, base_name='service')
    router.register(r'organizations/(?P<organization_id>\w+)/locations/(?P<location_id>\w+)/services', ServiceViewSet, base_name='service')
    router.register(r'locations/(?P<location_id>\w+)/services', ServiceViewSet, base_name='service')
    router.register(r'locations/(?P<location_id>\w+)/organizations/(?P<organization_id>\w+)/services', ServiceViewSet, base_name='service')

    return router

urlpatterns = [
    url(r'^$', TemplateView.as_view(template_name='pages/home.html'), name='home'),
    url(r'^about/$', TemplateView.as_view(template_name='pages/about.html'), name='about'),

    # Django Admin, use {% url 'admin:index' %}
    url(settings.ADMIN_URL, admin.site.urls),

    # User management
    url(r'^users/', include('users.urls', namespace='users')),
    url(r'^accounts/', include('allauth.urls')),

    # Your stuff: custom urls includes go here
    url(r'^v1/docs/', get_swagger_view(title='Pathways API')),
    url(r'^v1/', include(build_router().urls)),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    # This allows the error pages to be debugged during development, just visit
    # these url in browser to see how these error pages look like.
    urlpatterns += [
        url(r'^400/$', default_views.bad_request, kwargs={'exception': Exception('Bad Request!')}),
        url(r'^403/$', default_views.permission_denied, kwargs={'exception': Exception('Permission Denied')}),
        url(r'^404/$', default_views.page_not_found, kwargs={'exception': Exception('Page not Found')}),
        url(r'^500/$', default_views.server_error),
    ]
    if 'debug_toolbar' in settings.INSTALLED_APPS:
        import debug_toolbar
        urlpatterns = [
            url(r'^__debug__/', include(debug_toolbar.urls)),
        ] + urlpatterns
