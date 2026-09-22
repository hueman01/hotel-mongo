from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path, re_path
from django.views.static import serve
from TipoHabitacion import views as hotel_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('TipoHabitacion.urls')),
]

# Servir archivos media en desarrollo (DEBUG=True)
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# Servir archivos media en producción (DEBUG=False) - para Render
urlpatterns += [
    re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
]

handler404 = hotel_views.custom_404