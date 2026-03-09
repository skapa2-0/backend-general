from django.contrib import admin
from django.urls import include, path

urlpatterns = [
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
