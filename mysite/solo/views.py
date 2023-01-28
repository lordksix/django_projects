from django.shortcuts import render

# Create your views here.

def index(request):
    print('get')
    strval=False
    if request.method =='POST':
        strval1=request.POST['search1'].strip()
        strval2=request.POST['search2'].strip()       
        strval=strval1+strval2
        strval=strval[::-1]
        strval.casefold()
        # Render the HTML template index.html with the data in the context variable.
        print(strval)
        
    return render(
            request,
            'solo/index.html',
            context={'result': strval},
        )

