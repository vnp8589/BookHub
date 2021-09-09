from django.urls import path
from authy.views import UserProfile, Signup, PasswordChange, PasswordChangeDone, EditProfile, book, Book_Details,rating_process, searchBook1,userlist, UserSearch1, contactus, report
from . import views
from django.contrib.auth import views as authViews 
from authy.views import SearchResultsView, HomePageView


urlpatterns = [
   	
    path('profile/edit', EditProfile, name='edit-profile'),
   	path('signup/', Signup, name='signup'),
   	path('login/', authViews.LoginView.as_view(template_name='login.html'), name='login'),
   	path('logout/', authViews.LogoutView.as_view(), {'next_page' : 'index'}, name='logout'),
   	path('changepassword/', PasswordChange, name='change_password'),
   	path('changepassword/done', PasswordChangeDone, name='change_password_done'),
	  path('login/password-reset/', authViews.PasswordResetView.as_view(template_name='request_password_reset.html'), name='password_reset'),
    path('password-reset/done/', authViews.PasswordResetView.as_view(template_name='password_reset_done.html'), name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/', authViews.PasswordResetConfirmView.as_view(template_name='password_reset_confirm.html'), name='password_reset_confirm'),
    path('password-reset-complete/', authViews.PasswordResetCompleteView.as_view(template_name='password_reset_complete.html'), name='password_reset_complete'),  	
    path('<int:books_id>',Book_Details,name="Book details"),
    path('rating_process',rating_process, name='rating_process'),
    path('search_book/', SearchResultsView.as_view(), name='list_book'),
	  path('filterBooks/',searchBook1, name="filterBook"),
    path('upload1/', HomePageView.as_view(), name='upload_book'),
    path('userlist/',userlist,name='userlist'),
    path('new1/', UserSearch1, name='usersearch1'),
     
]