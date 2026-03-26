from django.urls import path
from .views import home_view, ask_view, clear_chat_view

urlpatterns = [
    path("", home_view, name="home"),
    path("ask/", ask_view, name="ask"),
    path("clear/", clear_chat_view, name="clear"),
]