from django.contrib import admin
from .models import Question, Choice, Comment

class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 3

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('question_text', 'pub_date', 'total_votes_display', 'views')
    search_fields = ['question_text']
    list_filter = ['pub_date']
    inlines = [ChoiceInline]

    def total_votes_display(self, obj):
        return obj.total_votes()
    total_votes_display.short_description = 'Toplam Oy'

@admin.register(Choice)
class ChoiceAdmin(admin.ModelAdmin):
    list_display = ('choice_text', 'question', 'votes')
    list_filter = ['question']
    search_fields = ['choice_text']

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('author_name', 'question', 'rating', 'created_at')
    list_filter = ['question', 'rating']
    search_fields = ['author_name', 'comment_text']