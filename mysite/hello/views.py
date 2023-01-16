#import re
from django.utils.timezone import datetime
from django.shortcuts import render
from django.http import HttpResponse


#def home(request):
#    return HttpResponse("Hello, Django!")

""" def hello_there(request, name):
    now = datetime.now()
    formatted_now = now.strftime("%A, %d %B, %Y at %X")

    # Filter the name argument to letters only using regular expressions. URL arguments
    # can contain arbitrary text, so we restrict to safe characters only.
    match_object = re.match("[a-zA-Z]+", name)

    if match_object:
        clean_name = match_object.group(0)
    else:
        clean_name = "Friend"

    content = "Hello there, " + clean_name + "! It's " + formatted_now
    return HttpResponse(content) """

def hello_there(request, name):
    return render(
        request,
        'hello/hello_there.html',
        {
            'name': name,
            'date': datetime.now()
        }
    )
def home(request):
    num_visits=request.session.get('num_visits',0)+1
    request.session['num_visits'] = num_visits 
    if num_visits > 4 : request.session['num_visits']=1
    response = render(request,"hello/home.html",{'num_visits': request.session['num_visits']})  # django.http.HttpResponse
    response.set_cookie('dj4e_cookie', '32df267d', max_age=1000)
    return response

def about(request):
    return render(request, "hello/about.html")

def contact(request):
    return render(request, "hello/contact.html")
