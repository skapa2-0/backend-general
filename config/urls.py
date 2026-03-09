from django.contrib import admin
from django.http import JsonResponse
from django.urls import include, path


def api_root(request):
    return JsonResponse({
        'name': 'Skapa API',
        'version': '1.0.0',
        'status': 'running',
        'environment': 'dev',
        'endpoints': {
            'core': '/api/v1/',
            'audit': '/api/v1/audit/',
            'epersona': '/api/v1/epersona/',
            'developpeur': '/api/v1/developpeur/',
            'userstory': '/api/v1/userstory/',
            'designsystem': '/api/v1/designsystem/',
            'coachpm': '/api/v1/coachpm/',
            'analyseterrain': '/api/v1/analyseterrain/',
            'admin': '/admin/',
        },
        'documentation': 'https://dev-api.skapa.design/api/v1/',
    })


urlpatterns = [
    path('', api_root, name='api-root'),
    path('admin/', admin.site.urls),
    path('api/v1/', include('core.urls')),
    path('api/v1/audit/', include('audit.urls')),
    path('api/v1/epersona/', include('epersona.urls')),
    path('api/v1/developpeur/', include('developpeur.urls')),
    path('api/v1/userstory/', include('userstory.urls')),
    path('api/v1/designsystem/', include('designsystem.urls')),
    path('api/v1/coachpm/', include('coachpm.urls')),
    path('api/v1/analyseterrain/', include('analyseterrain.urls')),
]
