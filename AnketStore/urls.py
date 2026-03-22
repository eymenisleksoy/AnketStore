from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView

admin.site.site_header = "AnketStore Admin"
admin.site.site_title = "AnketStore Admin Portalı"
admin.site.index_title = "Anket Yönetimine Hoş Geldiniz"

urlpatterns = [
    path('admin/', admin.site.urls),
    path('polls/', include('polls.urls')),
    path('', RedirectView.as_view(url='/polls/', permanent=True)),
]