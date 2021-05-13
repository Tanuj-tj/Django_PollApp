from django.http import Http404
from django.http.response import HttpResponseRedirect
from django.shortcuts import get_object_or_404,render
from django.http import HttpResponse
from django.template import loader
from .models import Question,Choice
from django.urls import reverse

from django.views import generic

class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        return Question.objects.order_by('-pub_date')[:5]

# def index(request):
#     latest_question_list = Question.objects.order_by('-pub_date')[:5]
#     template = loader.get_template('polls/index.html')
#     context = {
#         'latest_question_list':latest_question_list,
#     }
#     #output = ', '.join([q.question_text for q in latest_question_list]) 
#     #return HttpResponse(template.render(context,request))
#     return render(request,'polls/index.html',context)

class DetailView(generic.DetailView):
    model = Question
    template_name = 'polls/detail.html'

# def detail(request,question_id):
#     question = get_object_or_404(Question,pk=question_id)
#     # try:
#     #     question = Question.objets.get(pk=question_id)
#     # except Question.DoesNotExist:
#     #     raise Http404("Question does not exist")
#     #return HttpResponse("You're looking at question %s." % question_id)
#     return render(request,'polls/detail.html',{'question':question})

class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/result.html'

# def results(request,question_id):
#     question = get_object_or_404(Question,pk=question_id)
#     # response = "You're looking at the results of question %s."
#     #return HttpResponse(response % question_id)
#     return render(request,'polls/result.html',{'question':question})

def vote(request,question_id):
    question = get_object_or_404(Question,pk=question_id)
    try:
        
        # request.POST is a dictionary-like object that lets you access submitted data by key name. 
        # In this case, request.POST['choice'] returns the ID of the selected choice, as a string. 
        # request.POST values are always strings.

        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except(KeyError, Choice.DoesNotExist):
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

        # reverse() call will return a string like this  '/polls/3/results/'

        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))

    #return HttpResponse("You're voting on question %s." % question_id)




