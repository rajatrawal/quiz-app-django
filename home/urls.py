
from django.contrib import admin
from django.urls import path,include
from . views import *
urlpatterns = [
  path('',index,name="index"),
  path('checkAnswer/<uid>/<str:createObj>',check_answer,name='check_answer'),
  path('quiz/',quiz,name="quiz"),
  path('signUp/',sign_up,name='sign_up'),
  path('signIn/',sign_in,name='sign_in'),
  path('signOut/',sign_out,name='sign_out'),
  path('loadAttendedQuestionData/<uid>',loadAttendedQuestionData,name='load_attended_question_data')
]

