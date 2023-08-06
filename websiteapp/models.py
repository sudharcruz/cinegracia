from django.db import models
from django.contrib.auth.models import User,AbstractUser

from django.urls import reverse_lazy,reverse



class upcoming(models.Model):

    moviename = models.CharField(max_length=100)

    release =  models.CharField(max_length=100)

    Rating =  models.IntegerField()

    image = models.ImageField()
    
    Duration = models.IntegerField()

class newmovies(models.Model):
    
    moviename = models.CharField(max_length=100)

    release =  models.CharField(max_length=100)

    Rating =  models.DecimalField(max_digits=3,decimal_places=2)

    image = models.ImageField()
    
    Duration = models.SlugField(max_length=100)

    def __str__(self):
        return self.moviename

class moviedetailpage(models.Model):

    bgimage = models.ImageField()

    movieimage = models.ImageField()

    newrel = models.CharField(max_length=200)

    title = models.CharField(max_length=200)

    res = models.SlugField(max_length=50)

    genre = models.CharField(max_length=200)

    release = models.DateField()

    duration = models.SlugField()

    plot = models.TextField(max_length=2000)

    ott = models.CharField(max_length=50)

    seasons = models.SlugField(max_length=50,default=None ,blank=True,null=True)

    episodes = models.SlugField(max_length=50, default=None ,blank=True,null=True)

    video = models.FileField(upload_to='media/',null=True)

    favourite = models.ManyToManyField(User,related_name="favourite",blank=True)

    like = models.ManyToManyField(User,related_name="like",blank=True)

    def __str__(self):

        return self.title

class userrating(models.Model):

    ratingpost = models.ForeignKey(moviedetailpage,related_name='ratingpost',on_delete=models.CASCADE)

    user = models.ForeignKey(User,on_delete=models.CASCADE)

    rating = models.DecimalField(max_digits=3,decimal_places=1)

    time = models.DateTimeField(auto_now_add=True)

    def __str__(self) :
        return '%s - %s ' % (self.ratingpost.title,self.rating)
    
class toprated(models.Model):
    
    bgimage = models.ImageField()

    movieimage = models.ImageField()

    newrel = models.CharField(max_length=200)

    title = models.CharField(max_length=200)

    res = models.SlugField(max_length=50)

    genre = models.CharField(max_length=200)

    release = models.DateField()

    duration = models.SlugField()

    plot = models.TextField(max_length=2000)

    ott = models.CharField(max_length=50)

    def __str__(self):
        return self.title

class topmovies(models.Model):

    moviename = models.CharField(max_length=100)

    release =  models.CharField(max_length=100)

    rating =  models.DecimalField(max_digits=3,decimal_places=2)

    image = models.ImageField()
    
    duration = models.SlugField(max_length=100)

    def __str__(self):
        return self.moviename

class topseries(models.Model):
    
    seriesname = models.CharField(max_length=100)

    release =  models.CharField(max_length=100)

    rating =  models.DecimalField(max_digits=3,decimal_places=2)

    image = models.ImageField()
    
    duration = models.SlugField(max_length=100)

    video = models.FileField(upload_to='media/',null=True)

    def __str__(self):
        return self.seriesname

class comments(models.Model):

    usercomment = models.TextField(max_length=2000)

class topanimes(models.Model):

    animename = models.CharField(max_length=100)

    release =  models.CharField(max_length=100)

    rating =  models.DecimalField(max_digits=3,decimal_places=2)

    image = models.ImageField()
    
    duration = models.SlugField(max_length=100)

    def __str__(self):
        return self.animename


class postcomment(models.Model):

    Post = models.ForeignKey(moviedetailpage,related_name="comments",on_delete=models.CASCADE)

    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

    name = models.CharField(null=True,max_length=250)

    commentreply = models.ForeignKey('self',null=True,blank=True,related_name='replies',on_delete=models.CASCADE)

    date_added = models.DateTimeField(auto_now_add=True)

    usercomments = models.TextField(max_length=2000)

    def __str__(self) :
            return '%s - %s ' % (self.Post.title,self.name)
        
class profile (models.Model):

    user = models.OneToOneField(User,on_delete=models.CASCADE)

    dp = models.ImageField(blank=True,null=True,upload_to='media/')

    insta_url = models.CharField(blank=True,null=True,max_length=300)

    fb_url = models.CharField(blank=True,null=True,max_length=300)

    github_url = models.CharField(blank=True,null=True,max_length=300)

    youtube_url = models.CharField(blank=True,null=True,max_length=300)

    twitter_url = models.CharField(blank=True,null=True,max_length=300)

    bio = models.TextField(blank=True,null=True,max_length=2000)

    def __str__(self):

        return str(self.user)
    def get_absolute_url(self):

        return reverse('myprofile')

class MovieLike(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    movie_id = models.PositiveIntegerField()
    movie_name = models.CharField(max_length=200,blank=True,null=True)

    def __str__(self):
        return '%s - %s' % (self.user,self.movie_name)
class MovieComment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    movie_id = models.PositiveIntegerField()
    movie_name = models.CharField(max_length=200,blank=True,null=True)
    text = models.TextField()
    date_added = models.DateTimeField(auto_now_add=True,null=False)
    def __str__(self):
        return '%s - %s' % (self.user,self.movie_name)
class MovieFavorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    movie_id = models.PositiveIntegerField()
    movie_name = models.CharField(max_length=200,blank=True,null=True)
    movie_poster = models.ImageField(null=True,blank=True)
    def __str__(self):
        return '%s - %s' % (self.user,self.movie_name)

class MovieRating(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    movie_id = models.PositiveIntegerField()
    rating = models.DecimalField(max_digits=3,decimal_places=1)
    date_added = models.DateTimeField(auto_now_add=True,null=False)
    movie_name = models.CharField(max_length=200,blank=True,null=True)
    def __str__(self):
        return '%s - %s' % (self.user,self.movie_name)




