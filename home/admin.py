from django.contrib import admin
from . models import *

class AnswerAdmin(admin.StackedInline):
    model = Answer
    
class QuestionAdmin(admin.ModelAdmin):
    inlines = (AnswerAdmin,)



admin.site.register(Question,QuestionAdmin)
admin.site.register((Category,Answer,Quiz,GivenQuizQuestions))

