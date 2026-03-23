import os
import django
import random
from datetime import datetime, timedelta

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'AnketStore.settings')
django.setup()

from polls.models import Question, Choice

def randomize_stats():
    questions = Question.objects.all()
    for q in questions:
        q.views = random.randint(50, 5000)
        q.save()
        for choice in q.choice_set.all():
            choice.votes = random.randint(0, 500)
            choice.save()
    print("All stats randomized!")

if __name__ == '__main__':
    randomize_stats()
