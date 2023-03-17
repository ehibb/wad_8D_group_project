from django.urls import path
from card import views

app_name = 'card'

urlpatterns = [
    path('', views.index, name='index'),
    path('about/', views.about, name='about'),
    path('category/<slug:category_name_slug>/', views.show_category, name='show_category'),
    path('add_category/', views.add_category, name='add_category'),
    path('category/<slug:category_name_slug>/add_cardset/', views.add_cardset, name='add_cardset'),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('restricted/', views.restricted, name='restricted'),
    path('logout/', views.user_logout, name='logout'),
    path('settings/', views.settings, name='settings'),
    path('account/', views.account, name='account'),
    path('my_cards/', views.my_cards, name='my_cards'),
    path('my_cards/comment/', views.comment, name='comment'),
    path('test/', views.test, name='test'),
    path('card_set/<slug:flash_card_set_slug>/', views.show_flash_card_set, name='card_set'),
    path('card_set/<slug:flash_card_set_slug>/add_card/', views.add_card, name='add_card'),
    path('search/', views.search, name='search'),
    path('edit/', views.edit, name='edit'),
]
