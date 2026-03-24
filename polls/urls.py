from django.urls import path
from . import views

app_name = 'polls'
urlpatterns = [
    # Ana sayfa: /polls/
    path('', views.index, name='index'),
    
    # Anket listesi: /polls/list/
    path('list/', views.poll_list, name='list'),
    
    # Trend anketler: /polls/trending/
    path('trending/', views.trending_polls, name='trending'),
    
    # Fotoğraflı anketler: /polls/photos/
    path('photos/', views.photo_polls, name='photos'),
    
    # Soru detayı: /polls/5/
    path('<int:question_id>/', views.detail, name='detail'),
    
    # Sonuçlar: /polls/5/results/
    path('<int:question_id>/results/', views.results, name='results'),
    
    # Oy verme işlemi: /polls/5/vote/
    path('<int:question_id>/vote/', views.vote, name='vote'),

    # Tüm sonuçlar: /polls/all-results/
    path('all-results/', views.all_results, name='all_results'),
    
    # Yorum ekleme: /polls/5/comment/
    path('<int:question_id>/comment/', views.add_comment, name='add_comment'),

    # Anket serisini başlat
    path('start/', views.start_survey, name='start_survey'),
]