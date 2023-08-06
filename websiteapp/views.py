from typing import Any
from django.forms.models import BaseModelForm
from django.shortcuts import render,get_object_or_404
from django.contrib.auth.models import User
from django.contrib import messages
from .models import *
from django.contrib.auth.views import PasswordChangeView,PasswordResetCompleteView
from django.contrib import auth
from.forms import commentsform,ratingform,profileform,profileupdate,commentform,rateform
from django.urls import reverse_lazy,reverse
from django.views.generic import DetailView,CreateView,View, UpdateView
from django.views import generic
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from register.views import register
from django.db.models import Q,Avg,Func
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect , JsonResponse
from django.template.loader import render_to_string
from.forms import commentsform
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserChangeForm
import requests
from django.core.paginator import Paginator
from django.conf import settings
from django.contrib.auth import get_user_model
import os

key = os.environ.get('TMDB_API')


def error_404(request,exception):
    return render(request,'websiteapp/movie-not-found.html')


class profileupdateview(LoginRequiredMixin,generic.UpdateView):

    model = profile
    template_name = 'websiteapp/updateprofile.html'
    fields = ['bio', 'dp', 'insta_url', 'fb_url','twitter_url','youtube_url','github_url']
    success_url = reverse_lazy('websiteapp:index')

    def get_object(self, queryset=None):
        return self.request.user.profile



def usercomment(request,videoid):

    if request.method == 'POST':

        form = commentsform(request.POST)

        if form.is_valid :

            form.save()
            messages.success(request,'Posted succesfully')
            
            return HttpResponseRedirect('/usercomment')
    else:


        form = commentsform

    sut = get_object_or_404(topseries,video=videoid)

    sure = topseries.objects.all()


    return render(request,'websiteapp/usercomment.html',{'form':form,'sut':sut,'sure':sure})


def index(request):

    User = get_user_model()

    superuser = User.objects.filter(is_superuser=True).first()


    detail = newmovies.objects.all()

    futail = topmovies.objects.all()[:8]

    series = topseries.objects.all()[:4]

    anime = topanimes.objects.all()[:4]

    
    api_urls = [
        f'https://api.themoviedb.org/3/movie/popular?api_key={key}',
        # Add more API URLs here for additional movie details
    ]
    genre_url = f'https://api.themoviedb.org/3/genre/movie/list?api_key={key}'
    genre_serie_url = f'https://api.themoviedb.org/3/genre/tv/list?api_key={key}'
    series_api = f'https://api.themoviedb.org/3/tv/top_rated?api_key={key}'
    lan_url_m = f'https://api.themoviedb.org/3/configuration/languages?api_key={key}'
    lan_response = requests.get(lan_url_m)
    lan_data = lan_response.json()
    
    lan_list = []
    for lan in lan_data:
        lan_details = {
            
            'iso_639_1': lan['iso_639_1'],
            'english_name' : lan['english_name'],
            'name' : lan['name'],
        }
        lan_list.append(lan_details)
    response = requests.get(series_api)
    series_data = response.json()
    series = series_data['results']
    
    genre_response = requests.get(genre_url)

    genre_data = genre_response.json()
    genres = genre_data['genres']

    genre_res = requests.get(genre_serie_url)

    genres_data = genre_res.json()

    genress = genres_data['genres']

    upcoming_url = f'https://api.themoviedb.org/3/movie/upcoming?api_key={key}'
    upcoming_response = requests.get(upcoming_url)
    upcoming_data = upcoming_response.json()
    upcomings = upcoming_data['results']
    movie_list = []
    series_list = []
    upcoming_list = []
    genre_list = []
    genre_list_2 = []
    base_image_url = 'https://image.tmdb.org/t/p/w500'
    
    
    for genre in genres:
        
        genre_details = {
            'id' : genre['id'],
            'name' : genre['name'],
        }
        genre_list.append(genre_details)
    
    for gen in genress:
         
        genres_details = {
            'id' : gen['id'],
            'name' : gen['name'],
        }
        genre_list_2.append(genres_details)

    for api_url in api_urls:
        response = requests.get(api_url)
        movie_data = response.json()
        movies = movie_data['results']  # Assuming the movie list is under 'results' key

        for movie in movies:
            poster_path = movie.get('poster_path')
            backdrop_path = movie.get('backdrop_path')
            #print(backdrop_path,poster_path)
            #complete_poster_url = base_image_url + poster_path  # Complete URL for the movie poster
            #complete_poster_url_2 = base_image_url + backdrop_path
            #print(f"Movie: {movie['title']}")
            #print(f"Poster URL: {complete_poster_url}")

            movie_details = {
                
                'id' : movie['id'],
                'title': movie['title'],
                'vote_average': movie['vote_average'],
                'release_date': movie['release_date'],
                'poster_path': base_image_url+ str(movie.get('poster_path')),
                'backdrop_path' : base_image_url+ str(movie.get('backdrop_path')),
                'overview' : movie['overview'],
                'popularity' : movie['popularity'],
            }
            movie_list.append(movie_details)

    for serie in series:

                poster = serie['poster_path']
                backdrop_path = serie['backdrop_path']
                complete_poster_url = base_image_url + poster 
                complete_poster_url_2 = base_image_url + backdrop_path

                series_details = {
                    'id' : serie['id'],
                    'title': serie['name'],
                    'vote_average': serie['vote_average'],
                    'release_date': serie['first_air_date'],
                    'poster_path': complete_poster_url,
                    'backdrop_path' : complete_poster_url_2,
                    'overview' : serie['overview'],
                    'popularity' : serie['popularity'],
                    #'genre_names' : genre_names,
                }

                series_list.append(series_details)
    
    for upcoming in upcomings:
         
            upcoming_details = {
                    'id' : upcoming['id'],
                    'title': upcoming['title'],
                    'vote_average': upcoming['vote_average'],
                    'release_date': upcoming['release_date'],
                    'poster_path': base_image_url + str(upcoming.get('poster_path')),
                    'backdrop_path' : base_image_url + str(upcoming.get('backdrop_path')),
                    'overview' : upcoming['overview'],
                    'popularity' : upcoming['popularity'],
            }
            upcoming_list.append(upcoming_details)

    context = {'detail': detail,'futail':futail,'series':series,'anime':anime,'movies': movie_list,'series':series_list,'upcomings':upcoming_list,'genres':genre_list,'genress':genre_list_2,'lan_m':lan_list,'suser':superuser}

    return render(request, 'websiteapp/index.html',context)

def register(request):

    return render(request,'register/register.html')

def discover(request,genre_name,genreid,section):

    time = 'day'

    genre_url = f'https://api.themoviedb.org/3/discover/movie?api_key={key}&with_genres={genreid},'

    genre_serie = f'https://api.themoviedb.org/3/discover/tv?api_key={key}&with_genres={genreid}'

    movie_sort = f'https://api.themoviedb.org/3/discover/movie?api_key={key}&with_original_language={genre_name}'

    series_sort = f'https://api.themoviedb.org/3/discover/tv?api_key={key}&with_original_language={genre_name}'

    trend_url = f'https://api.themoviedb.org/3/trending/movie/{time}?api_key={key}'

    trend_u = f'https://api.themoviedb.org/3/trending/tv/{time}?api_key={key}'


    base_image_url = 'https://image.tmdb.org/t/p/w500'

    genre_list = []
    genre_list_serie =[]
    lan_list_m = []
    lan_list_s = []
    trend_m = []
    trend_s = []

    trend = requests.get(trend_u)

    trend_data = trend.json()

    trend_series = trend_data['results']

    trend_response = requests.get(trend_url)

    trend_Data = trend_response.json()

    trend_movies = trend_Data['results']

    genre_response = requests.get(genre_url)

    genre_data = genre_response.json()

    genres = genre_data['results']

    genre_res =requests.get(genre_serie)

    genre_res_data = genre_res.json()

    genre_series = genre_res_data['results']

    language_response = requests.get(movie_sort)
    language_data = language_response.json()
    language_m = language_data['results']

    lan_response = requests.get(series_sort)
    lan_data = lan_response.json()
    lan_s = lan_data['results']

    for m in trend_movies:
        details = {
                    'id' : m['id'],
                    'title': m['title'],
                    'vote_average': m['vote_average'],
                    'release_date': m.get('release_date'),
                    'poster_path': base_image_url + str(m.get('poster_path')),
                    'backdrop_path' : base_image_url + str(m.get('backdrop_path')),
                    'overview' : m['overview'],
                    'popularity' : m['popularity'],
        }
        trend_m.append(details)

    tm = Paginator(trend_m,8)

    page = request.GET.get('page')

    trend_movie = tm.get_page(page)   

    for s in trend_series:
        
            detail = {
                    'id' : s['id'],
                    'title': s['name'],
                    'vote_average': s['vote_average'],
                    'release_date': s.get('first_air_date'),
                    'poster_path': base_image_url + str(s.get('poster_path')),
                    'backdrop_path' : base_image_url + str(s.get('backdrop_path')),
                    'popularity' : s['popularity'],
            }
            trend_s.append(detail)
    ts = Paginator(trend_s,8)

    page = request.GET.get('page')

    trend_serie = ts.get_page(page)              

    for la in lan_s:
        
            language_detail = {
                    'id' : la['id'],
                    'title': la['name'],
                    'vote_average': la['vote_average'],
                    'release_date': la.get('first_air_date'),
                    'poster_path': base_image_url + str(la.get('poster_path')),
                    'backdrop_path' : base_image_url + str(la.get('backdrop_path')),
                    'overview' : la['overview'],
                    'popularity' : la['popularity'],
            }
            lan_list_s.append(language_detail)
            

    
    for lan in language_m:
        
            language_details = {
                    'id' : lan['id'],
                    'title': lan['title'],
                    'vote_average': lan['vote_average'],
                    'release_date': lan.get('release_date'),
                    'poster_path': base_image_url + str(lan.get('poster_path')),
                    'backdrop_path' : base_image_url + str(lan.get('backdrop_path')),
                    'overview' : lan['overview'],
                    'popularity' : lan['popularity'],
            }
            lan_list_m.append(language_details)
    
    for gen_serie in genre_series:
        
            genre_details_ser = {
                    'media_type' : 'tv',
                    'id' : gen_serie['id'],
                    'title': gen_serie['name'],
                    'vote_average': gen_serie['vote_average'],
                    'release_date': gen_serie['first_air_date'],
                    'poster_path': base_image_url + str(gen_serie.get('poster_path')),
                    'backdrop_path' : base_image_url + str(gen_serie.get('backdrop_path')),
                    'overview' : gen_serie['overview'],
                    'popularity' : gen_serie['popularity'],

            }
            genre_list_serie.append(genre_details_ser)
        
    for genre in genres:
            genre_details = {
                    'media_type' : 'movie',
                    'id' : genre['id'],
                    'title': genre['title'],
                    'vote_average': genre['vote_average'],
                    'release_date': genre['release_date'],
                    'poster_path': base_image_url + str(genre.get('poster_path')),
                    'backdrop_path' : base_image_url + str(genre.get('backdrop_path')),
                    'overview' : genre['overview'],
                    'popularity' : genre['popularity'],

            }
            genre_list.append(genre_details)
        #print(genre_list)
    
    p = Paginator(genre_list,8)

    page = request.GET.get('page')

    movie_page = p.get_page(page)

    #print(genre_list)


    s = Paginator(genre_list_serie,8)

    page = request.GET.get('page')

    series_page = s.get_page(page)

    d = Paginator(lan_list_m,8)

    page = request.GET.get('page')

    lan_page_m = d.get_page(page)

    c = Paginator(lan_list_s,8)

    page = request.GET.get('page')

    lan_page_s = c.get_page(page)

    context = {
        'genres' : genre_list,
        'genre_series' : genre_list_serie,
        'genre_name' : genre_name,
        'language_m' : lan_list_m,
        'lan_s' : lan_list_s,
        'movie_page' : movie_page,
        'series_page' : series_page,
        'section': section,
        'lan_page_m' : lan_page_m,
        'lan_page_s':lan_page_s,
        'trend_movie' : trend_movie,
        'trend_serie' :  trend_serie,
    }

    if section == 'movie-genre':
        return render(request,'websiteapp/discover.html',context)
    elif section == 'series-genre':
        return render(request,'websiteapp/discover.html',context)
    elif section == 'movie-lan':
        return render(request,'websiteapp/discover.html',context)
    elif section == 'series-lan':
        return render(request,'websiteapp/discover.html',context)
    
     
    return render(request,'websiteapp/discover.html',context)
class custom (PasswordResetCompleteView):

    success_url = '/register/login/'

def login (request):

    if request.method == 'POST':
        username = request.POST['name']
        password = request.POST['password']

        user = auth.authenticate(username=username,password=password)

        if user is not None:

            auth.login(request,user)
            return redirect("/")
        else:
            messages.error(request,'Invalid Credentials')
            return redirect("login")
    else:
        return render(request,'register/login.html')

def logout (request):

    auth.logout(request)
    return reverse('websiteapp:index')

def search(request):

    

    searched = request.GET.get('searched', '')

    dbsearch = moviedetailpage.objects.filter(title__icontains=searched)

    base_image_url = 'https://image.tmdb.org/t/p/w500'

    search_list = []

    serie_list = []
    

    if searched:

        total = 10

        for page in range(1,total+1):

            urls = [
                f'https://api.themoviedb.org/3/search/movie?api_key={key}&query={searched}&page={page}',]
                #f'https://api.themoviedb.org/3/search/tv?api_key={key}&query={searched}',]
            url2 = [f'https://api.themoviedb.org/3/search/tv?api_key={key}&query={searched}&page={page}',]
            for url in url2:
                response = requests.get(url)
                serie = response.json()
            for url in urls:
                response = requests.get(url)
                data = response.json()


                if 'results' in data:
                    results = data['results']

                    
                # Process the combined results
                for result in results:
                    poster = result['poster_path']

                    backdrop_path = result['backdrop_path']

                    complete_backdrop = base_image_url + str(backdrop_path)

                    complete_poster = base_image_url + str(poster)
                    #complete_backdrop = base_image_url + str(backdrop_path) if backdrop_path else ""

                    
                    search_details = {
                            'id' : result['id'], 
                            'title' : result['title'],
                            'vote_average': result['vote_average'],
                            'release_date': result['release_date'],
                            'poster_path': complete_poster,
                            'backdrop_path' : complete_backdrop,
                            'overview' : result['overview'],
                            'popularity' : result['popularity'],
                        }
                    

                    search_list.append(search_details)
                
                

                
                if 'results' in serie:
                    seriesresults = serie['results']

                    for res in seriesresults:
                        poster = res['poster_path']

                        backdrop_path = res['backdrop_path']

                        complete_backdrop = base_image_url + str(backdrop_path)

                        complete_poster = base_image_url + str(poster)

                        serie_details = {
                            'id' : res['id'], 
                            'title' : res['name'],
                            'vote_average': res['vote_average'],
                            'release_date': res['first_air_date'],
                            'poster_path': complete_poster,
                            'backdrop_path' : complete_backdrop,
                            'overview' : res['overview'],
                            'popularity' : res['popularity'],
                        }
                        serie_list.append(serie_details)
                    #print(serie_list)
            p1 = Paginator(search_list,8)
            page1 = request.GET.get('page1')
            movie_page = p1.get_page(page1)

            p2 = Paginator(serie_list, 8)
            page2 = request.GET.get('page2')
            series_page = p2.get_page(page2)
            
        print(f"Page1: {p1,movie_page}")
        print(f"Page2: {p2,series_page}")

        context = {'searched':searched,'dbsearch':dbsearch,'results':search_list,'seriesresults':serie_list,'movie_page':movie_page,'series_page':series_page,}

        if not search_list:
            context['no_results'] = True
        #print(f"Total search results: {len(search_list)}")
        #print(f"Search results: {search_list}")

        return render (request,'websiteapp/search.html',context)
    else:
        searched = ''
        dbsearch = ''
        return render (request,'websiteapp/search.html',{'searched':searched,'dbsearch':dbsearch})
    
class Round(Func):
    function = 'ROUND'
    template='%(function)s(%(expressions)s, 2)'

class MovieDetailView(DetailView):

    
    
    def get(self, request, movieid , id):
            
            try:
                ratemovie = get_object_or_404(moviedetailpage, title=movieid)
                averagerate = userrating.objects.filter(ratingpost=ratemovie).aggregate(avg_rating=Round(Avg('rating')))['avg_rating']
                myrate = userrating.objects.filter(ratingpost=ratemovie)
                if averagerate is None:
                    averagerate = 0
                movierating = moviedetailpage.objects.get(title=movieid)
                detail = moviedetailpage.objects.all()
                det = get_object_or_404(moviedetailpage, title=movieid)
                sut = get_object_or_404(moviedetailpage, title=movieid)
                series1 = topseries.objects.all()[:4]
                comment = postcomment.objects.all()
                for c in comment:
                    print(c)
                postrating = userrating.objects.filter(ratingpost=ratemovie)
                for r in postrating:
                    print(r)
                ani = get_object_or_404(moviedetailpage, title=movieid)
                context = {'detail': detail,
                            'det': det, 'sut': sut,
                        'comment': comment, 
                        'series1': series1, 
                        'ani': ani,
                        'movierating':movierating,
                        'averagerate':averagerate,
                        'ratemovie':ratemovie,
                        'postrating':postrating,
                        'myrate':myrate,}
                form = commentsform()
                rating = ratingform(request.POST)
                context['form'] = form
                fav = get_object_or_404(moviedetailpage, title=movieid)
                is_favourite = False
                if fav.favourite.filter(id=request.user.id).exists():
                    is_favourite = True
                context['is_favourite'] = is_favourite
                like = get_object_or_404(moviedetailpage,title=movieid)
                totallike=like.like.count()
                is_like = False
                if like.like.filter(id=request.user.id).exists():
                    is_like = True
                context['totallike'] = totallike
                context['is_like'] = is_like
                context['postrating'] = postrating
                if request.user.is_authenticated:

                    if rating.is_bound and rating.is_valid():
                            userexists = userrating.objects.filter(Q(user=request.user) & Q(ratingpost__title=movieid))
                            if userexists.exists():
                                messages.error(request, 'You Have Already Rated This Movie')
                            else:
                                movierating = get_object_or_404(moviedetailpage, title=movieid)
                                rate = rating.save(commit=False)
                                rate.ratingpost = movierating
                                rate.user = request.user
                                rate.save()
                                messages.success(request, 'Rated Successfully')

                            return redirect(reverse('websiteapp:movie-details', kwargs={'movieid': movieid,'id':id}))

                if request.user.is_authenticated:
                    if form.is_valid():
                        post = get_object_or_404(moviedetailpage, title=movieid)
                        comment = form.save(commit=False)
                        comment.Post = post
                        comment.user = request.user
                        comment.save()
                        messages.success(request, 'Posted successfully')

                else:
                    messages.error(request,'Please Log-in To Comment/Rate To This Movie')
                messages.get_messages(request)
            except Exception  :
                 

                context = self.tmdb(request,movieid,id)
                return context

            
            return render(request, 'websiteapp/movie-details.html', context)

    
    def post(self, request, movieid,id,):
        
        form = commentsform(request.POST)
        rating = ratingform(request.POST)
        ratemovie = get_object_or_404(moviedetailpage, title=movieid)
        averagerate = userrating.objects.filter(ratingpost=ratemovie).aggregate(avg_rating=Round(Avg('rating')))['avg_rating']
        if request.user.is_authenticated:

            if rating.is_bound and rating.is_valid():
                    userexists = userrating.objects.filter(Q(user=request.user) & Q(ratingpost__title=movieid))
                    if userexists.exists():
                        messages.error(request, 'You Have Already Rated This Movie')
                    else:
                        movierating = get_object_or_404(moviedetailpage, title=movieid)
                        rate = rating.save(commit=False)
                        rate.ratingpost = movierating
                        rate.user = request.user
                        rate.save()
                        messages.success(request, 'Rated Successfully')

                    return redirect(reverse('websiteapp:movie-details', kwargs={'movieid': movieid,'id':id}))


        if request.user.is_authenticated:
                post = get_object_or_404(moviedetailpage, title=movieid)

                # Process comment form
                if form.is_valid():
                    comment = form.save(commit=False)
                    comment.Post = post
                    comment.user = request.user
                    comment.save()
                    messages.success(request, 'Posted successfully')
                    return redirect(reverse('websiteapp:movie-details', kwargs={'movieid': movieid,'id':id}))
                else:
                    # Handle comment form validation errors
                    error_message = form.errors.as_text()
                    messages.error(request, f'Comment Form Error: {error_message}')

                

        else:
                messages.error(request, 'Please Log-in To Comment/Rate To The Movie')
                return redirect(reverse('websiteapp:movie-details', kwargs={'movieid': movieid,'id':id}))
        
        fav = get_object_or_404(moviedetailpage,title=movieid)
        is_favourite = False
        if fav.favourite.filter(id=request.user.id).exists():
            is_favourite = True
            
        detail = moviedetailpage.objects.all()
        det = get_object_or_404(moviedetailpage, title=movieid)
        sut = get_object_or_404(moviedetailpage, title=movieid)
        series1 = topseries.objects.all()[:4]
        comment = postcomment.objects.all()
        for c in comment:
            print(c)
        postrating = userrating.objects.filter(ratingpost=ratemovie)
        ani = get_object_or_404(moviedetailpage, title=movieid)
        comment1 = postcomment.objects.select_related('user').all()
        username = request.user.username
        context = {'detail': detail, 
                   'det': det,
                     'sut': sut,
                     'comment': comment,
                     'comment1': comment1,
                     'postrating':postrating,
                    'series1': series1, 
                    'ani': ani,
                    'username':username,
                    'is_favourite':is_favourite,
                       'averagerate':averagerate,
                    'ratemovie':ratemovie,
                   'rate':rate,}
        
        context['postrating']= postrating
        fav = get_object_or_404(moviedetailpage, title=movieid)
        is_favourite = False
        if fav.favourite.filter(id=request.user.id).exists():
            is_favourite = True
        context['is_favourite'] = is_favourite
        messages.get_messages(request)
        return render (request, 'websiteapp/movie-details.html', context)
    
    def tmdb(self,request,movieid,id):
        
        tmdb_api_key = "34d518706297f7ced3a25969c4a2e1c6"
        api_urls = [
            f'https://api.themoviedb.org/3/movie/popular?api_key={key}',
            #f'https://api.themoviedb.org/3/tv/top_rated?api_key={tmdb_api_key}',
        ]
        urls = [
            f'https://api.themoviedb.org/3/movie/{id}?api_key={key}',]
        series_urls =    [f'https://api.themoviedb.org/3/tv/{id}?api_key={key}',]
        
        search_list = []
        base_image_url = 'https://image.tmdb.org/t/p/w500' 
        genre_url = f"https://api.themoviedb.org/3/genre/movie/list?api_key={key}"
        genre_response = requests.get(genre_url)
        genre_data = genre_response.json()
        genres = {genre['id']: genre['name'] for genre in genre_data['genres']}
        #https://api.themoviedb.org/3/movie/popular?api_key=87605116445c191d48efb6e99e895de5

        series_api = f'https://api.themoviedb.org/3/tv/top_rated?api_key={tmdb_api_key}'
        response = requests.get(series_api)
        series_data = response.json()
        series = series_data['results']

        movie_list = []
        series_list =[]
        search_list2 = []
        recomand_list_m = []
        recomand_list_s = []
        
        base_image_url = 'https://image.tmdb.org/t/p/w500' 
        recommend_urls = [f'https://api.themoviedb.org/3/movie/{id}/recommendations?api_key={key}']
        recommend_serie = [f'https://api.themoviedb.org/3/tv/{id}/recommendations?api_key={key}']

        sea = None
        for url in urls:
            response = requests.get(url)
            data = response.json()
        for url in series_urls:
            response = requests.get(url)
            serie_data = response.json()

            genre_names = []
            for genre_id in data.get('genres', []):
                genre = next((genre for genre in genre_data['genres'] if genre['id'] == genre_id), None)
                if genre:
                    genre_names.append(genre['name'])
            
    
            
        
            if 'id' in data :
                
                    result = data
               
                    search_details = []
                
                    poster = result['poster_path']

                    backdrop_path = result['backdrop_path']

                    complete_backdrop = base_image_url + str(backdrop_path)

                    complete_poster = base_image_url + str(poster)
    

                    #title_m = result['title']

                    #name_s = res['name']

                    
                    #complete_backdrop = base_image_url + str(backdrop_path) if backdrop_path else ""

                    if result['title']  == movieid and result['id'] == id:

                        
                            sea = result

                            movi_details_url = f"https://api.themoviedb.org/3/movie/{sea['id']}?api_key={tmdb_api_key}&append_to_response=videos"
                            movi_details_response = requests.get(movi_details_url)
                            movi_details_data = movi_details_response.json()

                            if 'videos' in movi_details_data:
                                videos = movi_details_data['videos']['results']
                                trailers = [video for video in videos if video['type'] == 'Trailer']

                                if trailers:
                                    trailerkey = trailers[0]['key']
                                    trailerurl = f"https://www.youtube.com/embed/{trailerkey}"
                                    sea['trailer_url'] = trailerurl
                                else:
                                    sea['trailer_url'] = None
                            else:
                                sea['trailer_url'] = None

                            print("Selected Movie:", sea['title'])
                            print("Trailer URL:", sea['trailer_url'])
                            genres = [genre['name'] for genre in data.get('genres', [])]
                           
                            print(recommend_urls)

                            for url in recommend_urls:  
                                recommend_response = requests.get(url)
                                recommend = recommend_response.json()
                                recommand_data = recommend['results']
                                for rec in recommand_data:
                                        complete_backdrop = base_image_url + str(rec.get('backdrop_path'))
                                        complete_poster = base_image_url + str(rec.get('poster_path'))

                                        
                                                
                                        if 'title' in rec:
                                            recomand_details = {
                                            'id': rec['id'], 
                                            'title': rec['title'],
                                            'vote_average': rec['vote_average'],
                                            'release_date': rec['release_date'],
                                            'poster_path': complete_poster,
                                            'backdrop_path': complete_backdrop,
                                            'overview': rec['overview'],
                                            'popularity': rec['popularity'],
                                            'genres' : genres,
                                            }
                                            recomand_list_m.append(recomand_details) 

                            break
                    
                    

                    if 'title' in result:

                        #print(sea,movieid)
                        search_details = {
                                'runtime' : result['runtime'],
                                'tagline' : result['tagline'],
                                'budget' : result['budget'],
                                'homepage' : result['homepage'],
                                'title' : result['title'],
                                'vote_average': result['vote_average'],
                                'release_date': result['release_date'],
                                'poster_path': complete_poster,
                                'backdrop_path' : complete_backdrop,
                                'overview' : result['overview'],
                                'popularity' : result['popularity'],
                                'genre_names' : genre_names,
                                'status': result['status'],
                                'original_title' : result['original_title'],
                                'revenue' : result['revenue'],
                                
                            }
                        search_list.append(search_details)
                        
            if 'id' in serie_data :
                
                    res = serie_data
               
                    search_details = []
                
                    poster = res['poster_path']

                    backdrop_path = res['backdrop_path']

                    complete_backdrop = base_image_url + str(backdrop_path)

                    complete_poster = base_image_url + str(poster)

                    
                    #title_m = result['title']

                    #name_s = res['name']

                    
                    #complete_backdrop = base_image_url + str(backdrop_path) if backdrop_path else ""

                    if res['name']  == movieid and res['id'] == id:

                        
                            sea = res
                            serie_details_url = f"https://api.themoviedb.org/3/tv/{sea['id']}?api_key={tmdb_api_key}&append_to_response=videos"
                            serie_details_response = requests.get(serie_details_url)
                            serie_details_data = serie_details_response.json()

                            if 'videos' in serie_details_data:
                                videos = serie_details_data['videos']['results']
                                trailers = [video for video in videos if video['type'] == 'Trailer']

                                if trailers:
                                    trailer_key = trailers[0]['key']
                                    trailer_url = f"https://www.youtube.com/embed/{trailer_key}"
                                    sea['trailer_url'] = trailer_url
                                else:
                                    sea['trailer_url'] = None
                            else:
                                sea['trailer_url'] = None

                            print("Selected Movie:", sea['name'])
                            print("Trailer URL:", sea['trailer_url'])
                            genres = [genre['name'] for genre in serie_data.get('genres', [])]

                            for url in recommend_serie:  
                                recommend_responses = requests.get(url)
                                recommend_ser = recommend_responses.json()
                                recommand = recommend_ser.get('results')
                                
                               
                                for rec in recommand:
                                        complete_backdrop = base_image_url + str(rec.get('backdrop_path'))
                                        complete_poster = base_image_url + str(rec.get('poster_path'))
                                                
                                        if 'name' in rec:
                                            recomand_details = {
                                            'id': rec['id'], 
                                            'title': rec['name'],
                                            'vote_average': rec['vote_average'],
                                            'release_date': rec['first_air_date'],
                                            'poster_path': complete_poster,
                                            'backdrop_path': complete_backdrop,
                                            'overview': rec['overview'],
                                            'popularity': rec['popularity'],
                                            }
                                            recomand_list_s.append(recomand_details) 

                             
                            break
                            
                            
                    if 'name' in res:

                        search_details = {
                                        'runtime' : res['runtime'],
                                        'tagline' : res['tagline'],
                                        'budget' : res['budget'],
                                        'homepage' : res['homepage'],
                                        'title' : res['name'],
                                        'vote_average': res['vote_average'],
                                        'release_date': res['first_air_date'],
                                        'poster_path': complete_poster,
                                        'backdrop_path' : complete_backdrop,
                                        'overview' : res['overview'],
                                        'popularity' : res['popularity'],
                                        'episode_run_time' : res['episode_run_time'],
                                        'number_of_episodes' : res['number_of_episodes'],
                                        'number_of_seasons' : res['number_of_seasons'],
                                        'last_air_date' : res['last_air_date'],
                                        'original_name' : res['original_name'],
                                        'origin_country' : res['origin_country'],
                                        'genres' : genres,
                                    }
                        search_list.append(search_details)
                        
        
        if request.user.is_authenticated:
            user_like = MovieLike.objects.filter(user=request.user, movie_name=movieid, movie_id=id).exists()
            user_fav = MovieFavorite.objects.filter(user=request.user, movie_name=movieid, movie_id=id).exists()
            totallike = MovieLike.objects.filter(movie_name=movieid, movie_id=id).count()
            allcomments = MovieComment.objects.filter(movie_name=movieid, movie_id=id)
            post_rate = MovieRating.objects.filter(user=request.user, movie_name=movieid, movie_id=id)
        else:
            user_like = MovieLike.objects.filter(movie_name=movieid, movie_id=id, user=None).exists()
            user_fav = MovieFavorite.objects.filter(movie_name=movieid, movie_id=id, user=None).exists()
            totallike = MovieLike.objects.filter(movie_name=movieid, movie_id=id).count()
            allcomments = MovieComment.objects.filter(movie_name=movieid, movie_id=id)
            post_rate = None
        #rate = MovieRating.objects.filter

        averagerate = MovieRating.objects.filter(movie_name=movieid, movie_id=id).aggregate(avg_rating=Round(Avg('rating')))['avg_rating']
        if averagerate is None:
            averagerate = 0
        context = { 'movie_details': movie_list, 'averagerate':averagerate,
                    'series_details':series_list,
                       'sea': sea,'genres':genres,
                       'search_details':search_list,'ferm':rateform(),
                       'recomand_list_m':recomand_list_m,'post_rate':post_rate,
                       'recomand_list_s':recomand_list_s,'allcomments':allcomments,
                       'id':id,'user_like':user_like,'user_fav':user_fav,'totallike':totallike,
                       'form':commentform(),}
        
            

        return render (request,'websiteapp/movie-details.html',context)
    
@login_required
def post_comment(request, movieid, id):
    if request.method == 'POST':
        form = commentform(request.POST)
        if form.is_valid():
            comment_text = form.cleaned_data['text']
            comment = MovieComment.objects.create(user=request.user, movie_name=movieid, movie_id=id, text=comment_text)
            comment.save()
            messages.success(request, 'Comment Posted successfully')
    return redirect(reverse('websiteapp:movie-details', kwargs={'movieid': movieid, 'id': id}))
@login_required
def post_rating(request, movieid, id):
    if request.method == 'POST':
        form = rateform(request.POST)
        print(form)
        if form.is_valid():
            rating_rate = form.cleaned_data['rating']
            
          
            rated = MovieRating.objects.filter(user=request.user, movie_name=movieid, movie_id=id)
            if rated.exists():
                messages.error(request, 'You Have Already Rated This Movie')

            else:
               
                MovieRating.objects.create(user=request.user, movie_name=movieid, movie_id=id, rating=int(rating_rate))
                
                messages.success(request, 'Rated Successfully')
                print(f'rate:', rating_rate)
        #print(f'rate:', rating_rate)
    return redirect(reverse('websiteapp:movie-details', kwargs={'movieid': movieid, 'id': id}))
@login_required
def myprofile(request,id):

    user = get_object_or_404(User,id=id)

    favouritelist = MovieFavorite.objects.filter(user=user)

    fav_list = []

    base_image = 'https://image.tmdb.org/t/p/w500'

    for id in favouritelist:
         
        movie_id = id.movie_id
        name = id.movie_name

        url = f'https://api.themoviedb.org/3/movie/{movie_id}?api_key={key}'

        response = requests.get(url)
        movie = response.json()
        

        if 'id' in movie:
            details = {
                    'id' : movie['id'],
                    'title': movie['title'],
                    'vote_average': movie['vote_average'],
                    'release_date': movie.get('release_date'),
                    'poster_path': base_image + str(movie.get('poster_path')),
                    'backdrop_path' : base_image + str(movie.get('backdrop_path')),
                    'overview' : movie['overview'],
                    'popularity' : movie['popularity'],
            }
            fav_list.append(details)

    myrate = MovieRating.objects.filter(user=user)

    comment = MovieComment.objects.filter(user=user)

    context = {
        'user':user,
        'favouritelist':favouritelist,
        'myrate':myrate,
        'comment':comment,
        'fav_list':fav_list,
    }

    return render (request, 'websiteapp/myprofile.html', context)

class createprofile(CreateView):

    model = profile

    form_class = profileform

    template_name = 'websiteapp/createprofile.html'

    def form_valid(self, form):
            form.instance.user = self.request.user
            return super().form_valid(form)

@login_required
def ratingdelete(request,deleteid):


        rating = get_object_or_404(userrating,pk=deleteid)


        if rating.user == request.user:

            rating.delete()
            messages.success(request,'Your Existing Rating Has Been Deleted')
            return redirect(request.META.get('HTTP_REFERER'))
        else:

            messages.error(request,'This Is Not Your Rating ')
        return redirect(request.META.get('HTTP_REFERER'))

@login_required

def ratedelete(request,movieid,id,did):


        rating = get_object_or_404(MovieRating,pk=did)


        if rating.user == request.user:

            rating.delete()
            messages.success(request,'Your Existing Rating Has Been Deleted')
        else:

            messages.error(request,'This Is Not Your Rating ')
        return redirect(reverse('websiteapp:movie-details', kwargs={'movieid': movieid,'id':id}))


def commentdelete(request,delid,id):

    
    if request.user.is_authenticated:

         
            movie = get_object_or_404(postcomment,pk=delid)

            if movie.user == request.user:

                movie.delete()
                messages.success(request,"Deleted successfully")
                messages.get_messages(request)
                return redirect(request.META.get('HTTP_REFERER'))
            elif request.user.is_superuser:
                movie.delete()
                messages.success(request,"Deleted successfully")
                messages.get_messages(request)
                return redirect(request.META.get('HTTP_REFERER'))

            else:
                messages.warning(request,"This is Not Your Comment To Delete")
                messages.get_messages(request)
                return redirect(request.META.get('HTTP_REFERER'))
    else:
        return redirect('register')

@login_required   
def comment_delete(request,id,movieid,did):
     
    comment = get_object_or_404(MovieComment, pk=did)

    if comment.user == request.user or request.user.is_superuser:
        comment.delete()
        messages.success(request, "Comment deleted successfully.")
    else:
        messages.warning(request, "You do not have permission to delete this comment.")

   
    return redirect(reverse('websiteapp:movie-details', kwargs={'movieid': movieid,'id':id}))


def favlist(request):

    user = request.user

    favouritelist = MovieFavorite.objects.filter(user=user)

    fav_list = []

    base_image = 'https://image.tmdb.org/t/p/w500'

    for id in favouritelist:
         
        movie_id = id.movie_id
        name = id.movie_name

        url = f'https://api.themoviedb.org/3/movie/{movie_id}?api_key={key}'

        response = requests.get(url)
        movie = response.json()
        

        if 'id' in movie:
            details = {
                    'id' : movie['id'],
                    'title': movie['title'],
                    'vote_average': movie['vote_average'],
                    'release_date': movie.get('release_date'),
                    'poster_path': base_image + str(movie.get('poster_path')),
                    'backdrop_path' : base_image + str(movie.get('backdrop_path')),
                    'overview' : movie['overview'],
                    'popularity' : movie['popularity'],
            }
            fav_list.append(details)
    context = {
        'favouritelist':favouritelist,
        'fav_list':fav_list,

    }

    return render(request,'websiteapp/favouritelist.html',context)


@login_required
def addfavourite(request,movieid,id):

    fav = get_object_or_404(moviedetailpage,title=movieid)

    if fav.favourite.filter(id=request.user.id).exists():

        fav.favourite.remove(request.user)
    else:

        fav.favourite.add(request.user)
    return redirect(reverse('websiteapp:movie-details', kwargs={'movieid': movieid,'id':id}))


@login_required
def addfavourite_tmdb(request,movieid,id):
     
    user_fav, created = MovieFavorite.objects.get_or_create(user=request.user, movie_name=movieid, movie_id=id)
    
    if not created:
        user_fav.delete()
    else:
        user_fav.save()
    url = reverse('websiteapp:movie-details', kwargs={'movieid': movieid,'id':id})
    context = {'user_fav': user_fav}
    return HttpResponseRedirect(url,context)


@login_required
def addlike(request,movieid,id):

    user_like, created = MovieLike.objects.get_or_create(user=request.user, movie_name=movieid, movie_id=id)
    
    if not created:
        user_like.delete()

    totallike = MovieLike.objects.filter(movie_name=movieid,movie_id=id).count()
    url = reverse('websiteapp:movie-details', kwargs={'movieid': movieid,'id':id})
    context = {'user_like': user_like,'totallike':totallike}
    return HttpResponseRedirect(url,context)

def toprating(request,serid):

    seri = topseries.objects.all()

    suti = get_object_or_404(topseries,video=serid)

    context = {'seri':seri,'suti':suti}
     
    return render (request,'websiteapp/favouritelist.html',context,)


def display_collection_movies(request, collection_id):
    base_image = 'https://image.tmdb.org/t/p/w500'
    collection_url = f'https://api.themoviedb.org/3/collection/{collection_id}?api_key={key}'
    collection_response = requests.get(collection_url)
    
    if collection_response.status_code == 200:
        collection_data = collection_response.json()

        # Extract the collection name and poster path
        collection_name = collection_data['name']
        collection_poster_path = base_image + str(collection_data.get('poster_path'))
        collection_backdrop_path = base_image + str(collection_data.get('backdrop_path'))

        movie_list = []
        if 'parts' in collection_data:
            for movie_data in collection_data['parts']:
                movie_id = movie_data['id']
                movie_url = f'https://api.themoviedb.org/3/movie/{movie_id}?api_key={key}'
                movie_response = requests.get(movie_url)
                if movie_response.status_code == 200:
                    movie_data = movie_response.json()
                    movie_details = {
                        'id': movie_id,
                        'title': movie_data['title'],
                        'release_date': movie_data['release_date'],
                        'poster_path': base_image + str(movie_data.get('poster_path')),
                        'overview': movie_data['overview'],
                    }
                    movie_list.append(movie_details)
                else:
                    print(f"Failed to fetch data for movie {movie_id}. Status code: {movie_response.status_code}")
        p = Paginator(movie_list,4)
        page = request.GET.get('page')
        movies = p.get_page(page)
        context = {
            'collection_id': collection_id,
            'collection_name': collection_name,
            'collection_poster_path': collection_poster_path,
            'movie_list': movie_list,
            'collection_backdrop_path' : collection_backdrop_path,'movies':movies
        }
        return render(request, 'websiteapp/collection_movies.html', context)

def allshows(request,section,id):

    searched = request.GET.get('searched', '')

    total = 2

    time = 'day'

    base_image = 'https://image.tmdb.org/t/p/original'
    movie_list = []
    serie_list = []
    collection_list = []
    col_list = []
    search_list = []
    trend_m = []
    trend_s = []
    collection = [86311,10,1241,9485,131292,556,573436,531241]#,,125574,8650,939352,33514,119,131635]

    if searched:
        
        ur = f'https://api.themoviedb.org/3/search/collection?api_key={key}&query={searched}'
        respon = requests.get(ur)
        response_data = respon.json()
        collect_data = response_data['results']

        for d in collect_data:
            search_details = {
                    'id': d['id'], 
                    'title': d['name'],
                    #'vote_average': d['vote_average'],
                    #'release_date': d['release_date'],
                    'poster_path': base_image + str(d.get('poster_path')),
                    'backdrop_path': base_image + str(d.get('backdrop_path')),
                    'overview': d['overview'],
                    #'popularity': d['popularity'],
                }
            search_list.append(search_details)

    trend_url = f'https://api.themoviedb.org/3/trending/movie/{time}?api_key={key}'

    trend_u = f'https://api.themoviedb.org/3/trending/tv/{time}?api_key={key}'


    trend = requests.get(trend_u)

    trend_data = trend.json()

    trend_series = trend_data['results']

    trend_response = requests.get(trend_url)

    trend_Data = trend_response.json()

    trend_movies = trend_Data['results']

    for m in trend_movies:
        details = {
                    'id' : m['id'],
                    'title': m['title'],
                    'vote_average': m['vote_average'],
                    'release_date': m.get('release_date'),
                    'poster_path': base_image + str(m.get('poster_path')),
                    'backdrop_path' : base_image + str(m.get('backdrop_path')),
                    'overview' : m['overview'],
                    'popularity' : m['popularity'],
        }
        trend_m.append(details)

    tm = Paginator(trend_m,8)

    page = request.GET.get('page')

    trend_movie = tm.get_page(page)   

    for s in trend_series:
        
            detail = {
                    'id' : s['id'],
                    'title': s['name'],
                    'vote_average': s['vote_average'],
                    'release_date': s.get('first_air_date'),
                    'poster_path': base_image + str(s.get('poster_path')),
                    'backdrop_path' : base_image + str(s.get('backdrop_path')),
                    'popularity' : s['popularity'],
            }
            trend_s.append(detail)
    ts = Paginator(trend_s,8)

    page = request.GET.get('page')

    trend_serie = ts.get_page(page)              



    for i in collection:

        collection_url = f'https://api.themoviedb.org/3/collection/{i}?api_key={key}'
        collection_response = requests.get(collection_url)
        collection_data = collection_response.json()

        
        #print(collection_data)

        collection_name = collection_data['name']
        collection_id = collection_data['id']
        collection_overview = collection_data['overview']
        collection_poster_path = base_image + str(collection_data.get('poster_path'))
        #print(collection_name,collection_poster_path)
            
        
                
        col_details = {
                    'id' : collection_id,
                    'name' : collection_name,
                    'backdrop_path' : collection_poster_path,
                    'overview' : collection_overview,
                }
        col_list.append(col_details)

        

    for tits in range(1,total+1):

        url = f'https://api.themoviedb.org/3/movie/top_rated?api_key={key}&page={tits}'
        ser = f'https://api.themoviedb.org/3/tv/popular?api_key={key}&page={tits}'

        resp = requests.get(ser)

        data = resp.json()

        serie = data['results']

           
        for re in serie:
                
                details = {
                    'id': re['id'], 
                    'title': re['name'],
                    'vote_average': re['vote_average'],
                    'release_date': re['first_air_date'],
                    'poster_path': base_image + str(re.get('poster_path')),
                    'backdrop_path': base_image + str(re.get('backdrop_path')),
                    'overview': re['overview'],
                    'popularity': re['popularity'],
                }
                serie_list.append(details)
        #print(serie_list)

        response = requests.get(url)
        res = response.json()
        result = res['results']
        #print(result)

        
        if 'results' in res:     
            for res in result:
                
                details = {
                    'id': res['id'], 
                    'title': res['title'],
                    'vote_average': res['vote_average'],
                    'release_date': res['release_date'],
                    'poster_path': base_image + str(res.get('poster_path')),
                    'backdrop_path': base_image + str(res.get('backdrop_path')),
                    'overview': res['overview'],
                    'popularity': res['popularity'],
                }
                movie_list.append(details)
        #print(f'result',movie_list)

    detail = newmovies.objects.all().order_by('moviename')

        #futail = topmovies.objects.all()

    #series = topseries.objects.all().order_by('?')

    anime = topanimes.objects.all()
    p = Paginator(movie_list , 8)

    page = request.GET.get('page')

    movies = p.get_page(page)

    s = Paginator(serie_list,8)

    sage = request.GET.get('sage')

    serie = s.get_page(sage)

    c = Paginator(col_list,8)

    page = request.GET.get('page')

    coll = c.get_page(page)

    d = Paginator(collection_list,4)

    page =  request.GET.get('page')

    col = d.get_page(page)
    

    context = {'detail':detail,'serie':serie,'section':section,'movie_data':collection_list,'searched':searched,
               'anime':anime,'movies':movies,'coll':coll,'col':col,'search_list':search_list,
               'trend_movie':trend_movie,'trend_serie':trend_serie}

        
    if section == 'movie' and id == 1:

            return render(request,'websiteapp/allshows.html',context)
    elif section == 'upcoming' and id == 2:
            return render(request,'websiteapp/allshows.html',context)
    elif section == 'series' and id == 3:
            return render(request,'websiteapp/allshows.html',context)
    elif section == 'collection' and id == 4:
            return render(request,'websiteapp/allshows.html',context)
    elif section == 'search' and id == 5:
            return render(request,'websiteapp/allshows.html',context)
    elif section == 'movie-trend' and id == 6:
        return render(request,'websiteapp/allshows.html',context)
    elif section == 'series-trend' and id == 7:
        return render(request,'websiteapp/allshows.html',context)
    
    else:
            context = {'movies':movies,'detail':detail,'serie':serie,'section':section,'anime':anime}

            

    return render(request,'websiteapp/allshows.html',context)


class addcomment(CreateView):

        model = postcomment

        form_class = commentsform

        template_name = 'websiteapp/movie-details.html'

        success_url = reverse_lazy('/')
