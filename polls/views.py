from django.shortcuts import get_object_or_404, redirect, render
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.urls import reverse
from django.contrib.auth.models import User
from datetime import datetime   

from .models import Choice, Question

def delete(request):
	q = Question.objects.get(pk=request.POST.get('id'))
	if 1 == 1:
		q.delete()
	return redirect('/polls/')

def add(request):
    print(request.GET)
    question = Question(owner=request.user, question_text=request.GET['question_text'], pub_date=datetime.now())
    question.save()
    return redirect('/polls/')

def index(request):
    questions = Question.objects.filter(owner=request.user)
    latest_question_list = questions.order_by('-pub_date')[:10]
    print()
    context = {'latest_question_list': latest_question_list}
    return render(request, 'polls/index.html', context)

def detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/detail.html', {'question': question})
    
def results(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/results.html', {'question': question})

def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.GET['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))