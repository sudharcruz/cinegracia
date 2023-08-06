from django import forms
from django.forms import ModelForm
from.models import *

class profileupdate(forms.ModelForm):

    class Meta:

        model = profile

        fields = ('bio','dp','insta_url')


        labels={
            'bio':'BIO',
            'dp':'Profile Pic',
            'insta_url' : '',
            'fb_url':'',
            'github_url' : '',
            'youtube_url' : '',
            'twitter_url' : '',
        }


        widgets = {
            'insta_url': forms.TextInput(attrs={'placeholder': 'Your Instagram Link', 'class': 'form-control','style':'margin-right:10px;width:700px;margin-left: 300px; margin-bottom: 5px; color: gold'}),
            'fb_url': forms.TextInput(attrs={'placeholder': 'Your Facebook Link', 'class': 'form-control','style':'width:700px;margin-left: 300px; margin-bottom: 5px;' }),
            'github_url': forms.TextInput(attrs={'placeholder': 'Your Github Link', 'class': 'form-control','style':'width:700px;margin-left: 300px; margin-bottom: 5px;'}),
            'youtube_url': forms.TextInput(attrs={'placeholder': 'Your YouTube Link', 'class': 'form-control','style':'width:700px;margin-left: 300px; margin-bottom: 5px;'}),
            'twitter_url': forms.TextInput(attrs={'placeholder': 'Your Twitter Link', 'class': 'form-control', 'style':'width:700px;margin-left: 300px; margin-bottom: 5px;'}),
            'dp': forms.FileInput(attrs={'class': 'form-control', 'style': 'margin-left: 300px; margin-bottom: 5px;width:700px;'}),
        }

class profileform(forms.ModelForm):

    bio = forms.CharField(widget=forms.Textarea(attrs={'placeholder': 'Your Bio', 'class': 'form-control','style':'width:700px;margin-left: 300px; margin-bottom: 5px;'}), required=True)

    class Meta:

        model = profile

        fields = ('bio','insta_url','fb_url','github_url','youtube_url','twitter_url','dp',)

        labels={
            'bio':'',
            'dp':'Profile Pic',
            'insta_url' : '',
            'fb_url':'',
            'github_url' : '',
            'youtube_url' : '',
            'twitter_url' : '',
        }
        widgets = {
            'insta_url': forms.TextInput(attrs={'placeholder': 'Your Instagram Link', 'class': 'form-control','style':'margin-right:10px;width:700px;margin-left: 300px; margin-bottom: 5px;'}),
            'fb_url': forms.TextInput(attrs={'placeholder': 'Your Facebook Link', 'class': 'form-control','style':'width:700px;margin-left: 300px; margin-bottom: 5px;' }),
            'github_url': forms.TextInput(attrs={'placeholder': 'Your Github Link', 'class': 'form-control','style':'width:700px;margin-left: 300px; margin-bottom: 5px;'}),
            'youtube_url': forms.TextInput(attrs={'placeholder': 'Your YouTube Link', 'class': 'form-control','style':'width:700px;margin-left: 300px; margin-bottom: 5px;'}),
            'twitter_url': forms.TextInput(attrs={'placeholder': 'Your Twitter Link', 'class': 'form-control', 'style':'width:700px;margin-left: 300px; margin-bottom: 5px;'}),
            'dp': forms.FileInput(attrs={'class': 'form-control', 'style': 'margin-left: 300px; margin-bottom: 5px;width:700px;'}),
        }
class commentsform(forms.ModelForm):

    

    class Meta:
        
        model = postcomment
        fields = ('usercomments',)

        labels = {
            'usercomments':'',
        }

        widgets = {
            'usercomments' : forms.TextInput(attrs={'placeholder': 'Your Comments Here','style':'width:575px;','style':'height:80px;','style':'font-size:20px;'}),
    
        }

class commentform(forms.ModelForm):

    class Meta:

        model = MovieComment

        fields = ('text',)

        labels = {
            'text':'',
        }

        widgets = {
            'text' : forms.TextInput(attrs={'placeholder': ' Comment Here ','style':'width:575px;height:70px','style':'font-size:20px;border-radius:50px'}),
    
        }

class rateform(forms.ModelForm):

    class Meta():

        model = MovieRating

        fields = ('rating',)

        labels = {
            'rating':'',
        }

        widgets = {
            'rating' : forms.NumberInput(attrs={'placeholder':'Rate Here','style':'width:200px;','style':'border-radius:30px;','style':'height:50px;'}),
        }


class ratingform(forms.ModelForm):

    class Meta():

        model = userrating

        fields = ('rating',)

        labels = {
            'rating':'',
        }

        widgets = {
            'rating' : forms.NumberInput(attrs={'placeholder':'Rate Here','style':'width:200px;','style':'border-radius:30px;','style':'height:50px;'}),
        }