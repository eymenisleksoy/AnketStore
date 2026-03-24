import os
import django
import random
from datetime import datetime, timedelta
from django.utils import timezone

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'AnketStore.settings')
django.setup()

from polls.models import Question, Choice

all_topics = [
    ("En Sevdiğiniz Tatlı Hangisi?", ["Baklava", "Künefe", "Sütlaç", "Kazandibi"]),
    ("Hangi Süper Güce Sahip Olmak İsterdiniz?", ["Uçmak", "Görünmezlik", "Işınlanma", "Zihin Okuma"]),
    ("En Çok Tercih Ettiğiniz Spor Dalı?", ["Futbol", "Basketbol", "Voleybol", "Yüzme"]),
    ("Hangi Mevsim Sizi Daha Çok Yansıtıyor?", ["İlkbahar", "Yaz", "Sonbahar", "Kış"]),
    ("Kahvaltının Olmazsa Olmazı Nedir?", ["Peynir", "Zeytin", "Yumurta", "Sucuk"]),
    ("Hangi Şehirde Yaşamak İsterdiniz?", ["İstanbul", "İzmir", "Antalya", "Ankara"]),
    ("En Çok Hangi Film Türünü Seviyorsunuz?", ["Bilim Kurgu", "Komedi", "Korku", "Aksiyon"]),
    ("Hangi Teknolojiyi Daha Çok Kullanıyorsunuz?", ["Akıllı Telefon", "Laptop", "Tablet", "Oyun Konsolu"]),
    ("En Sevdiğiniz İçecek?", ["Çay", "Kahve", "Meyve Suyu", "Su"]),
    ("Tatil Rotanız Neresi Olur?", ["Deniz Kenarı", "Doğa Yürüyüşü", "Kültür Turu", "Kamp"]),
    ("Hangi Hayvanı Daha Çok Seviyorsunuz?", ["Kedi", "Köpek", "Kuş", "Balık"]),
    ("En Sevdiğiniz Oyun Türü?", ["RPG", "FPS", "Strateji", "Spor"]),
    ("Hangi Fast Food?", ["Hamburger", "Pizza", "Döner", "Lahmacun"]),
    ("Gelecekte Ulaşım Nasıl Olmalı?", ["Uçan Araba", "Işınlanma", "Hızlı Tren", "Elektrikli Araç"]),
    ("En İyi Programlama Dili?", ["Python", "JavaScript", "C++", "Java"]),
    ("Hangi Sosyal Medya Platformu?", ["Instagram", "Twitter / X", "TikTok", "Reddit"]),
    ("Kitap mı Film mi?", ["Kitap Okumak", "Film İzlemek", "İkisi de", "Hiçbiri"]),
    ("En İyi Tatil Mevsimi?", ["Yaz", "Kış", "İlkbahar", "Sonbahar"]),
    ("Hangi Akıllı Saat Markası?", ["Apple", "Samsung", "Huawei", "Diğer"]),
    ("En Sevdiğiniz Renk?", ["Mavi", "Kırmızı", "Yeşil", "Siyah"]),
    ("Hangi Müzik Türü?", ["Pop", "Rock", "Rap", "Klasik"]),
    ("Sabah mı Gece mi?", ["Sabah İnsanı", "Gece Kuşu", "Öğleci", "Uykucu"]),
    ("En İyi Kripto Para?", ["Bitcoin", "Ethereum", "Solana", "Dogecoin"]),
    ("Hangi Yapay Zeka?", ["ChatGPT", "Gemini", "Claude", "Llama"]),
    ("En Popüler Hobi?", ["Fotoğrafçılık", "Bahçecilik", "Yemek Yapmak", "Seyahat"]),
]

def populate():
    print("Deleting old questions...")
    Question.objects.all().delete()
    print("Populating database...")
    for idx, (q_text, c_texts) in enumerate(all_topics):
        pub_date = timezone.now() - timedelta(days=random.randint(0, 30))
        views = random.randint(100, 10000)
        
        q = Question.objects.create(
            question_text=q_text,
            pub_date=pub_date,
            views=views,
            image_url="" # REMOVED IMAGES
        )
        
        for c_text in c_texts:
            Choice.objects.create(
                question=q,
                choice_text=c_text,
                votes=random.randint(0, 1000),
                image_url="" # REMOVED IMAGES
            )
        print(f"Added poll: {q_text}")
    print("Done!")

if __name__ == '__main__':
    populate()
