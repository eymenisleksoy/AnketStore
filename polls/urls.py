from django.urls import path
from . import views

app_name = 'polls'
urlpatterns = [
    # Ana sayfa: /polls/
    path('', views.index, name='index'),
    
    # Anket listesi: /polls/list/
    path('list/', views.poll_list, name='list'),
    
    # Soru detayı: /polls/5/
    path('<int:question_id>/', views.detail, name='detail'),
    
    # Sonuçlar: /polls/5/results/
    path('<int:question_id>/results/', views.results, name='results'),
    
    # Oy verme işlemi: /polls/5/vote/
    path('<int:question_id>/vote/', views.vote, name='vote'),
]