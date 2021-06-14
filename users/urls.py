from django.urls import path
from .views import LoginView, UserView, KakaoSignInView, Example
urlpatterns = [
        path('/users', UserView.as_view()),
        path('/login', LoginView.as_view()),
        path('/kakaosignin', KakaoSignInView.as_view()),
        path('/decorator-test', Example.as_view())
        ]