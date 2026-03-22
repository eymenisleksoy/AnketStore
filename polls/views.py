from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from .models import Question, Choice

# 1. Ana Sayfa (Landing Page)
def index(request):
    return render(request, 'polls/index.html')

# 2. Anket Listesi (Tüm anketleri listeler)
def poll_list(request):
    # En son eklenen 20 soruyu tarihe göre sıralayıp alıyoruz
    latest_question_list = Question.objects.order_by('-pub_date')[:20]
    context = {'latest_question_list': latest_question_list}
    return render(request, 'polls/list.html', context)

# 3. Soru Detayı (Tek bir soruyu ve seçeneklerini gösterir)
def detail(request, question_id):
    # Soru varsa getir, yoksa 404 Hata sayfası göster
    question = get_object_or_404(Question, pk=question_id)
    
    # Görüntülenme sayısını artır
    question.views += 1
    question.save()
    
    return render(request, 'polls/detail.html', {'question': question})

# 3. Sonuçlar (Oylama sonrası sonuçları gösterir)
def results(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/results.html', {'question': question})

def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        # Formdan gelen 'choice' verisini (ID'sini) alıyoruz
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Eğer kullanıcı hiçbir şey seçmeden butona basarsa aynı sayfada hata gösteriyoruz
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "Herhangi bir seçenek seçmediniz.",
        })
    else:
        # Seçilen seçeneğin oy sayısını 1 artır ve veritabanına kaydet
        selected_choice.votes += 1
        selected_choice.save()
        
        # Başarılı oylamadan sonra kullanıcıyı sonuçlar sayfasına yönlendir.
        # HttpResponseRedirect kullanmak, sayfa yenilendiğinde oyun iki kere gitmesini engeller!
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))