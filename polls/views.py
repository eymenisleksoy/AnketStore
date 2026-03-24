from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from .models import Question, Choice, Comment

from django.db.models import Sum

# 1. Ana Sayfa (Landing Page)
def index(request):
    total_polls = Question.objects.count()
    total_votes = Choice.objects.aggregate(Sum('votes'))['votes__sum'] or 0
    total_views = Question.objects.aggregate(Sum('views'))['views__sum'] or 0
    latest_poll = Question.objects.order_by('-pub_date').first()
    
    context = {
        'total_polls': total_polls,
        'total_votes': total_votes,
        'total_views': total_views,
        'latest_poll': latest_poll,
    }
    return render(request, 'polls/index.html', context)

# 2. Anket Listesi (Tüm anketleri listeler)
def poll_list(request):
    # En son eklenen 20 soruyu tarihe göre sıralayıp alıyoruz
    latest_question_list = Question.objects.order_by('-pub_date')[:20]
    context = {'latest_question_list': latest_question_list, 'title': 'Tüm Anketler'}
    return render(request, 'polls/list.html', context)

# 2.1 Trend Anketler (Rasgele anketler)
def trending_polls(request):
    # Rasgele 6 anket alıyoruz
    random_question_list = Question.objects.order_by('?')[:6]
    context = {'latest_question_list': random_question_list, 'title': 'Trend Anketler'}
    return render(request, 'polls/list.html', context)

# 2.2 Fotoğraflı Anketler
def photo_polls(request):
    # Sadece görseli olan anketleri alıyoruz
    photo_question_list = Question.objects.exclude(image_url__isnull=True).exclude(image_url='').order_by('-pub_date')
    context = {'latest_question_list': photo_question_list, 'title': 'Fotoğraflı Anketler'}
    return render(request, 'polls/list.html', context)

# 3. Soru Detayı (Tek bir soruyu ve seçeneklerini gösterir)
def detail(request, question_id):
    # Soru varsa getir, yoksa 404 Hata sayfası göster
    question = get_object_or_404(Question, pk=question_id)
    
    # Görüntülenme sayısını artır
    question.views += 1
    question.save()
    
    # İstatiksel bilgiler
    all_questions = list(Question.objects.order_by('id'))
    total_questions = len(all_questions)
    current_index = 0
    for i, q in enumerate(all_questions):
        if q.id == question.id:
            current_index = i + 1
            break
            
    progress = (current_index / total_questions) * 100 if total_questions > 0 else 0
    
    comments = question.comments.all().order_by('-created_at')
    
    return render(request, 'polls/detail.html', {
        'question': question,
        'comments': comments,
        'total_questions': total_questions,
        'current_index': current_index,
        'progress': progress
    })

# 4. Yorum Ekleme
def add_comment(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    if request.method == 'POST':
        name = request.POST.get('author_name', 'Anonim')
        text = request.POST.get('comment_text')
        rating = request.POST.get('rating', 5)
        
        if text:
            Comment.objects.create(
                question=question,
                author_name=name,
                comment_text=text,
                rating=int(rating)
            )
    return HttpResponseRedirect(reverse('polls:detail', args=(question.id,)))

# 5. Sonuçlar (Oylama sonrası sonuçları gösterir)
def results(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    # Bir sonraki soruyu bul
    next_question = Question.objects.filter(pk__gt=question.id).order_by('id').first()
    
    return render(request, 'polls/results.html', {
        'question': question,
        'next_question': next_question
    })

# 6. Tüm Sonuçlar (Tüm anketlerin sonuçlarını grid olarak gösterir)
def all_results(request):
    question_list = Question.objects.all().order_by('-pub_date')
    return render(request, 'polls/all_results.html', {'question_list': question_list})

# 7. Anket Serisini Başlat
def start_survey(request):
    # İlk anketin ID'sini al
    first_question = Question.objects.order_by('id').first()
    if first_question:
        return HttpResponseRedirect(reverse('polls:detail', args=(first_question.id,)))
    else:
        return HttpResponseRedirect(reverse('polls:index'))

def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        # Formdan gelen 'choice' verisini (ID'sini) alıyoruz
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # İstatiksel bilgiler
        all_questions = list(Question.objects.order_by('id'))
        total_questions = len(all_questions)
        current_index = 0
        for i, q in enumerate(all_questions):
            if q.id == question.id:
                current_index = i + 1
                break
        progress = (current_index / total_questions) * 100 if total_questions > 0 else 0
        
        # Eğer kullanıcı hiçbir şey seçmeden butona basarsa aynı sayfada hata gösteriyoruz
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "Lütfen bir seçenek işaretleyiniz.",
            'total_questions': total_questions,
            'current_index': current_index,
            'progress': progress
        })
    else:
        # Seçilen seçeneğin oy sayısını 1 artır ve veritabanına kaydet
        selected_choice.votes += 1
        selected_choice.save()
        
        # Bir sonraki soruyu bul
        next_question = Question.objects.filter(pk__gt=question.id).order_by('id').first()
        
        if next_question:
            # Sıradaki ankete git (Opsiyonel olarak bir başarı mesajı ile)
            return HttpResponseRedirect(reverse('polls:detail', args=(next_question.id,)) + '?voted=1')
        else:
            # Son anketti, genel sonuçlara veya mevcut sonuçlara git
            return HttpResponseRedirect(reverse('polls:results', args=(question.id,)) + '?final=1')