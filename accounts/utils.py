from django.shortcuts import render
def Error(request):
    return render(request,'error.html')