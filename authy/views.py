from django.shortcuts import render, redirect, get_object_or_404
from authy.forms import SignupForm, ChangePasswordForm, EditProfileForm
from django.contrib.auth.models import User

from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash

from authy.models import Profile
from post.models import Post, Follow, Stream
from .models import books, BookReview
from django.db import transaction
from django.template import loader
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.views.generic import TemplateView, ListView
from django.db.models import Q # new

from django.core.paginator import Paginator

from django.urls import resolve

# Create your views here. 
def UserProfile(request, username):
	user = get_object_or_404(User, username=username)
	profile = Profile.objects.get(user=user)
	url_name = resolve(request.path).url_name
	
	if url_name == 'profile':
		posts = Post.objects.filter(user=user).order_by('-posted')

	else:
		posts = profile.favorites.all()


			#Profile info box 
	posts_count = Post.objects.filter(user=user).count()
	following_count = Follow.objects.filter(follower=user).count()
	followers_count = Follow.objects.filter(following=user).count()

	#follow status
	follow_status = Follow.objects.filter(following=user, follower=request.user).exists()

	#Pagination
	paginator = Paginator(posts, 6)
	page_number = request.GET.get('page')
	post_paginator = paginator.get_page(page_number)

	template = loader.get_template('profile.html')

	context = {
		'posts': post_paginator,
		'profile':profile,
		'following_count':following_count,
		'followers_count':followers_count,
		'posts_count':posts_count,
		'url_name':url_name,
		'follow_status': follow_status,

	}

	return HttpResponse(template.render(context, request))

def Signup(request):
	if request.method == 'POST':
		form = SignupForm(request.POST)
		if form.is_valid():
			username = form.cleaned_data.get('username')
			email = form.cleaned_data.get('email')
			password = form.cleaned_data.get('password')
			User.objects.create_user(username=username, email=email, password=password)
			return redirect('login')
	else:
		form = SignupForm()
	
	context = {
		'form':form,
	}

	return render(request, 'signup.html', context)

@login_required
def book(request):

    book_obj = books.objects.all()
    return render(request, 'book.html',{'book_obj' : book_obj})

@login_required
def Book_Details(request, books_id):
	bookDetails = books.objects.filter(id__icontains= books_id)
	reviews = BookReview.objects.filter(books = books_id)
	context = {'bookDetails': bookDetails, 
					'reviews' : reviews,
					'books_id' :books_id, 
					}

	return render(request, 'Book_details.html',context)

@login_required
def rating_process(request):

	if request.method == "POST":
		books_id = request.POST.get("books_id")
		book = books.objects.get(id = books_id)
		stars = request.POST.get("stars")
		content = request.POST.get("content")

		new_review = BookReview(books = book, stars = stars, content = content)
		new_review.save()

	return redirect('Book details',books_id)


@login_required
def PasswordChange(request):
	user = request.user
	if request.method == 'POST':
		form = ChangePasswordForm(request.POST)
		if form.is_valid():
			new_password = form.cleaned_data.get('new_password')
			user.set_password(new_password)
			user.save()
			update_session_auth_hash(request, user)
			return redirect('change_password_done')
	else:
		form = ChangePasswordForm(instance=user)

	context = {
		'form':form,
	}

	return render(request, 'change_password.html', context)

def PasswordChangeDone(request):
	return render(request, 'change_password_done.html')

def contactus(request):

	return render(request, 'contactus.html')

def report(request):

	return render(request,'report.html')


@login_required
def EditProfile(request):
	user = request.user.id
	profile = Profile.objects.get(user__id=user)

	if request.method == 'POST':
		form = EditProfileForm(request.POST, request.FILES)
		if form.is_valid():
			profile.picture = form.cleaned_data.get('picture')
			profile.first_name = form.cleaned_data.get('first_name')
			profile.last_name = form.cleaned_data.get('last_name')
			profile.location = form.cleaned_data.get('location')
			profile.url = form.cleaned_data.get('url')
			profile.profile_info = form.cleaned_data.get('profile_info')
			profile.save()
			return redirect('index')
	else:
		form = EditProfileForm()

	context = {
		'form':form,
	}

	return render(request, 'edit_profile.html', context)


@login_required
def follow(request, username, option):
	user = request.user
	following = get_object_or_404(User, username=username)

	try:
		f, created = Follow.objects.get_or_create(follower=user, following=following)

		if int(option) == 0:
			f.delete()
			Stream.objects.filter(following=following, user=user).all().delete()
		else:
			 posts = Post.objects.all().filter(user=following)[:10]

			 with transaction.atomic():
			 	for post in posts:
			 		stream = Stream(post=post, user=request.user, date=post.posted, following=following)
			 		stream.save()

		return HttpResponseRedirect(reverse('profile', args=[username]))
	except User.DoesNotExist:
		return HttpResponseRedirect(reverse('profile', args=[username]))

class HomePageView(TemplateView):
    template_name = 'book.html'

class SearchResultsView(ListView):
    model = books
    template_name = 'book.html'

    def get_queryset(self): # new
        query = self.request.GET.get('q1')
        object_list = books.objects.filter(
            Q(Title__icontains=query)
        )
        return object_list
	

def searchBook1(request):
	if request.method =="GET":
		Category = request.GET['Category']
		book = books.objects.filter(Category__icontains=Category)
		return render(request,'book1.html', {'data': book})	

def userlist(request):
	
	u = User.objects.all()
	return render(request,'book1.html',{'u': u})

def UserSearch1(request):
	query = request.GET.get("q2")
	context = {}
	
	if query:
		u = User.objects.filter(Q(username__icontains=query))

		#Pagination
		paginator = Paginator(u, 6)
		page_number = request.GET.get('page')
		users_paginator = paginator.get_page(page_number)

		context = {
				'u': users_paginator,
			}
	
	template = loader.get_template('index.html')
	
	return HttpResponse(template.render(context, request))

