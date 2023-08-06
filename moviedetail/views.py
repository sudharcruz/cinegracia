from django.shortcuts import render,get_object_or_404

from django.contrib.auth.models import User

from websiteapp.models import *

from django.http import HttpResponse

def moviedetail(request,movieid):

    detail = moviedetailpage.objects.all()

    det = moviedetailpage.objects.get(pk=movieid)

    context = {'detail':detail}
     
    return render (request,'movie-details/movie-details.html',context,{'det':det})

def toprating (request,id):

    futail = toprated.objects.all()

    fut = get_object_or_404(toprated,pk=id)

    context = {'futail':futail}

    context = {'fut':fut}

    return render (request,'websiteapp/movie-details.html',context)



