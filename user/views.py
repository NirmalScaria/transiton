from django.shortcuts import render
from django.http import HttpResponse

from . import sample
import sys
sys.path.append("..")
from searchfunctions import *
def homePage(request):
    return render(request,'user/index.html')

def search_results(request):
    context=sample.demoresult
    fromid=request.GET.get("fromid","1")
    toid=request.GET.get("toid","1")
    context=formattedsearchres(fromid,toid,"1900-01-01 "+request.GET.get("mytime","09:30")+":00")


    response = render(request,"user/search.html", context)
    response['Access-Control-Allow-Origin'] = '*'
    return response

def wake_up(request):
    response =  render(request,'user/wake_up.html')
    response['Access-Control-Allow-Origin'] = '*'
    return response