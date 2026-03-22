from django.contrib import admin
from .models import Question, Choice, Comment

class NoLogAdmin(admin.ModelAdmin):
    def log_addition(self, request, object, message):
        pass
    def log_change(self, request, object, message):
        pass
    def log_deletion(self, request, object, object_repr):
        pass

@admin.register(Question)
class QuestionAdmin(NoLogAdmin):
    pass

@admin.register(Choice)
class ChoiceAdmin(NoLogAdmin):
    pass

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    pass