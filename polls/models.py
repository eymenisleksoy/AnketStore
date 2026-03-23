from django.db import models

class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')
    views = models.IntegerField(default=0)
    image_url = models.URLField(max_length=500, blank=True, null=True)

    def __str__(self):
        return self.question_text
    
    def total_votes(self):
        return sum(choice.votes for choice in self.choice_set.all())

class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)
    image_url = models.URLField(max_length=500, blank=True, null=True)

    def __str__(self):
        return self.choice_text

class Comment(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='comments')
    author_name = models.CharField(max_length=100, default="Anonim")
    comment_text = models.TextField()
    rating = models.IntegerField(default=5)  # 1-5 arası puan
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.author_name} - {self.question.question_text}"
