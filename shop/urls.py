from django.contrib import admin
from django.urls import path, include
from shop import views

urlpatterns = [
    path('', views.IndexView.as_view(), name="index"),
    path('add_auction/', views.AuctionAdd.as_view(), name="add_auction"),
    path('list_auction/', views.AuctionList.as_view(), name="list_auction"),
    path('auction_details/<int:pk>/', views.AuctionDetails.as_view(), name="auction_details"),
    path('add_bid/<int:pk>/', views.AddBid.as_view(), name="add_bid"),
    path('add_message/', views.MessageAddView.as_view(), name='add_message'),
    path('list_message/', views.MessageListView.as_view(), name='list_message'),
    path('list_user_auctions/', views.UserAuctionList.as_view(), name='list_user_auctions'),
    path('list_user_bids/', views.UserBidList.as_view(), name='list_user_bids'),
    path('exchange_view/', views.ExchangeView.as_view(), name='exchange_view'),
    path('exchange_list_view', views.ExchangeListView.as_view(), name='exchange_list_view'),
    path('exchange_details/<int:pk>/', views.ExchangeDetailView.as_view(), name="exchange_details"),
    path('accept_exchange/<int:pk>/<int:pk2>', views.AcceptExchange.as_view(), name="accept_exchange"),
    path('decline_exchange/<int:pk>/', views.DeclineExchange.as_view(), name="decline_exchange"),
    path('counter_exchange/<int:pk>/', views.CounterofferExchange.as_view(), name="counter_exchange"),
    path('sell_choice/', views.SellChoice.as_view(), name='sell_choice'),
    path('buy_now/', views.BuyNow.as_view(), name="buy_now"),
    path('buy_now_list/', views.BuyNowListView.as_view(), name="buy_now_list"),
    path('buy_now_details/<int:pk>/', views.BuyNowDetailView.as_view(), name="buy_now_details"),
    path('buy/<int:pk>/', views.Buy.as_view(), name="buy"),
    path('auction_delete/<int:pk>/', views.AuctionDelete.as_view(), name="auction_delete"),
]

