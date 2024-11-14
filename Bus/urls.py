from django.urls import path
from . import views
urlpatterns = [
    path('',views.index,name="home"),
    path('search/',views.search,name="findbus"),
    path('signup/',views.signup,name="signup"),
    path('login/',views.login_user,name="login"),
    path('logout/',views.logout_user,name="logout"),
    path('busseat/',views.busseat,name="busseat"),
    path('reservation/',views.reservation,name="reservation"),
    path('bookings/pdf/',views.generate_pdf, name='generate_pdf'),
    path('busopbus/',views.busopbus, name='busopbus'),
    path('busopbooking/',views.busopbooking, name='busopbooking'),
    path('busopnavbar/',views.busopnavbar, name='busopnavbar'),

  


]