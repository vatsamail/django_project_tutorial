from django.http import HttpResponse, Http404, HttpResponseRedirect
from .models import Question, Choice
# from django.template import loader
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic

from django.utils import timezone

class IndexView(generic.ListView):
    template_name = 'polls/index.html' # overriding default polls/polls_index.html expectation
    context_object_name = 'latest_question_list' # overriding default question_list by latest_question_list
    def get_queryset(self):
        # return Question.objects.order_by('-pub_date')[:5]
        return Question.objects.filter(
            pub_date__lte=timezone.now() # less than or equal to
        ).order_by('-pub_date')[:5]

def index(request):
        #return HttpResponse("Hello, world! This is poll/index")
        latest_question_list = Question.objects.order_by('-pub_date')[:5]

        #temp_list = []
        #for lq in latest_question_list:
        #    temp_list.append(lq.question_text)
        #out = ', '.join(temp_list)

        #output = ', '.join([q.question_text for q in latest_question_list])
        #return HttpResponse(output)

        #template = loader.get_template('polls/index.html')

        '''
        corresponding index.html code:


          <li><a href="/polls/{{ question.id }}/">{{ question.question_text }}</a></li>
          <li><a href="{% url 'detail' question.id %}">{{ question.question_text }}</a></li>

        '''
        context = {
            'latest_question_list' : latest_question_list,
        }
        #return HttpResponse(template.render(context, request))
        return render(request, 'polls/index.html', context)



class DetailView(generic.DetailView):
    model = Question
    template_name = 'polls/detail.html'
    def get_queryset(self):
        """
        Excludes any questions that aren't published yet.
        """
        return Question.objects.filter(pub_date__lte=timezone.now())

def detail(request, question_id):
    # return HttpResponse("You're looking at question %s." % question_id)


    #try:
    #    question = Question.objects.get(id=question_id)
    #except Question.DoesNotExist:
    #    raise Http404("Question doesn't exist")
    #context = {
    #    'question': question,
    #}
    #render(request, 'polls/detail.html', context)

    '''
     corresponding detail.html code:

     <b>{{ question }}</b>


     <h1>{{ question.question_text }}</h1>
     <ul>
     {% for choice in question.choice_set.all %}
         <li>{{ choice.choice_text }}</li>
     {% endfor %}
     </ul>


    '''

    question = get_object_or_404(Question, id=question_id)
    context = {
        'question':question,
    }
    return (render(request, 'polls/detail.html', context))


class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'

def results(request, question_id):
    #response = "You're looking at the results of question %s."
    #return HttpResponse(response % question_id)
    question = get_object_or_404(Question, id=question_id)
    context = {
        'question': question,
    }
    return render(request, 'polls/results.html', context)


def vote(request, question_id):
    #return HttpResponse("You're voting on question %s." % question_id)
    question = get_object_or_404(Question, id=question_id)
    try:
        selected_choice = question.choice_set.get(id=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        context = {
            'question':question,
            'error_message': "You did not select a choice",
        }
        return render(request, 'polls/detail.html', context)
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))
