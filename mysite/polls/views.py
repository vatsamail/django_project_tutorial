from django.http import HttpResponse, Http404
from .models import Question
# from django.template import loader
from django.shortcuts import get_object_or_404, render

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
        context = {
            'latest_question_list' : latest_question_list,
        }
        #return HttpResponse(template.render(context, request))
        return render(request, 'polls/index.html', context)




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

    question = get_object_or_404(Question, id=question_id)
    context = {
        'question':question,
    }
    return (render(request, 'polls/detail.html', context))


def results(request, question_id):
    response = "You're looking at the results of question %s."
    return HttpResponse(response % question_id)

def vote(request, question_id):
    return HttpResponse("You're voting on question %s." % question_id)
