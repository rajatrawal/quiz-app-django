from django.shortcuts import render, HttpResponse, redirect
from . models import *
from django.http import JsonResponse
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.db.models import Q


# Create your views here.

@login_required
def index(request):
    categories = Category.objects.all()
    context = {'categories': categories, 'homeactive': True}
    category_text = request.GET.get('category')
    if category_text:
        user = request.user
        quiz_query = Quiz.objects.filter(
            Q(user=user) & Q(category__name=category_text)
        )

        if not quiz_query.exists():
            category = Category.objects.get(name=category_text)
            quiz = Quiz.objects.create(
                user=user, total_marks=0, category=category, marks=0)
            quiz.save()
        else:
            quiz = quiz_query.first()
        return redirect(f'quiz/?category={category_text}')

    return render(request, 'home/index.html', context)


@login_required
def check_answer(request, uid, createObj):
    try:
        payload = {'status': 200}
        answer = Answer.objects.get(uid=str(uid))
        if createObj == 'true':
            question = GivenQuizQuestions.objects.get_or_create(
                question=answer.question, answer=answer)[0]
            quiz = Quiz.objects.get(
                user=request.user, category=answer.question.category)
            is_already_given = Quiz.objects.filter(
                Q(user=request.user) & Q(
                    given_question__question=question.question)
            ).exists()

            if not is_already_given:
                quiz.given_question.add(question)
                quiz.save()
            else:
                payload = {'status': 404}
            payload['marks'] = quiz.marks
        else:
            payload = {'status': 404}
        if answer.is_correct:
            payload['is_correct'] = 'true'
        else:
            payload['is_correct'] = 'false'

        return JsonResponse(payload)
    except Exception as e:

        return JsonResponse({'status': 404})


def quiz(request):
    try:
        questions = Question.objects.all()
        category = request.GET.get('category')

        if category:
            quiz = Quiz.objects.get(user=request.user, category__name=category)
            quiz.calculateMarks()
            quiz.category.get_total()
            quiz.save()
            quiz.category.save()
            questions = questions.filter(category__name__icontains=category)
        p = Paginator(questions, 1)

        page_no = request.GET.get('page')

        if not page_no:
            page_no = 1
        try:
            page_obj = p.get_page(page_no)
        except:
            page_obj = p.get_page(1)

        context = {'page_obj': page_obj, 'category': category,
                   'quiz': quiz, 'homeactive': True}
        return render(request, 'home/quiz.html', context)
    except Exception as e:
        return HttpResponse("Something Went Wrong --->")


def sign_up(request):

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password1']
        if not User.objects.filter(username=username).exists():
            user = User.objects.create_user(
                username=username, password=password)
            user.save()
            messages.success(request, 'Signuped successfully.')
            return redirect('sign_in')
        messages.error(
            request, 'User already exist try with different username.')
    return render(request, 'home/signup.html', {'sign_up_active': True})


def sign_in(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if (user):
            login(request, user)
            messages.success(request, 'Signined Successfully.')
            return redirect('index')
        messages.error(request, 'Enter valid username or password.')
    return render(request, 'home/signin.html', {'sign_in_active': True})


def sign_out(request):
    logout(request)
    return redirect('/')


def loadAttendedQuestionData(request, uid):
    context = {}
    try:
        givenQuiz = Quiz.objects.filter(
            Q(user=request.user) & Q(given_question__question__uid=uid)
        )
        is_question_attened = givenQuiz.exists()

        payload = []
        context['status'] = 404
        if is_question_attened:
            context['status'] = 200
            quiz = givenQuiz[0]
            all_given_questions = quiz.given_question.all()
            all_given_questions = all_given_questions.filter(question__uid=uid)
            given_answer = all_given_questions.first().answer
            for i in all_given_questions.first().question.answers.all():
                if i == given_answer:
                    payload.append({'uid': str(i.uid), 'isCorrect': str(
                        i.is_correct), 'isSelected': 'true'})
                else:
                    payload.append({'uid': str(i.uid), 'isCorrect': str(
                        i.is_correct), 'isSelected': 'false'})
        context['payload'] = payload

    except:
        context['status'] = 404
    return JsonResponse(context)
