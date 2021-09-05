import datetime
from datetime import date

from django.contrib.auth.models import User
from django.test import Client
import pytest
from django.urls import reverse

from shop.models import Auction, Bid, Message, Exchange


@pytest.mark.django_db
def test_client():
    Client()


@pytest.mark.django_db
def test_index_view_get():
    c = Client()
    url = reverse('index')
    response = c.get(url)
    assert response.status_code == 200


@pytest.mark.django_db
def test_list_auction_logged_in(auctions, user):
    c = Client()
    c.force_login(user)
    url = reverse('list_auction')
    response = c.get(url)
    auction = response.context['auction_list']
    assert response.status_code == 200
    assert auction.count() == len(auctions)


@pytest.mark.django_db
def test_list_auction_not_logged():
    c = Client()
    url = reverse('list_auction')
    response = c.get(url)
    assert response.status_code == 302
    assert response.url.startswith(reverse('login'))


@pytest.mark.django_db
def test_auction_add_get_logged_in(user):
    c = Client()
    c.force_login(user)
    url = reverse('add_auction')
    response = c.get(url)
    assert response.status_code == 200


@pytest.mark.django_db
def test_auction_add_get_not_logged():
    c = Client()
    url = reverse('add_auction')
    response = c.get(url)
    assert response.status_code == 302
    assert response.url.startswith(reverse('login'))


@pytest.mark.django_db
def test_auction_add_post(user, category):
    c = Client()
    tomorrow = datetime.date.today() + datetime.timedelta(days=5)
    c.force_login(user)
    url = reverse('add_auction')
    response = c.post(url, {"name": 'test', "description": 'test', "price": 100, "end_date": tomorrow, "owner": user,
                            "category": 1})
    assert response.status_code == 302
    assert Auction.objects.count() == 1


@pytest.mark.django_db
def test_add_bid_get_not_logged_in(auctions):
    c = Client()
    url = reverse('add_bid', args=(auctions[0].pk,))
    response = c.get(url)
    assert response.status_code == 302
    assert response.url.startswith(reverse('login'))


@pytest.mark.django_db
def test_add_bid_get_logged_in(two_users, auctions):
    c = Client()
    c.force_login(two_users[1])
    url = reverse('add_bid', args=(auctions[0].pk,))
    response = c.get(url)
    assert response.status_code == 200


@pytest.mark.django_db
def test_bid_add_post(two_users, auctions):
    c = Client()
    today = datetime.date.today()
    c.force_login(two_users[0])
    url = reverse('add_bid', args=(auctions[0].pk,))
    response = c.post(url, {"price": 200, "auction": auctions[0].id, "bidder": two_users[1], "date": today})
    assert response.status_code == 302
    assert Bid.objects.count() == 1


@pytest.mark.django_db
def test_message_add_view_get_not_logged_in():
    c = Client()
    url = reverse('add_message')
    response = c.get(url)
    assert response.status_code == 302
    assert response.url.startswith(reverse('login'))


@pytest.mark.django_db
def test_message_add_view_get_logged_in(user):
    c = Client()
    c.force_login(user)
    url = reverse('add_message')
    response = c.get(url)
    assert response.status_code == 200


@pytest.mark.django_db
def test_message_add_view_post(two_users):
    c = Client()
    today = datetime.date.today()
    c.force_login(two_users[0])
    url = reverse('add_message')
    response = c.post(url, {"from_user": two_users[0], "to_user": two_users[1], "text": "jakis text"})
    assert response.status_code == 302
    assert Message.objects.count() == 1


@pytest.mark.django_db
def test_message_list_view_not_logged():
    c = Client()
    url = reverse('list_message')
    response = c.get(url)
    assert response.status_code == 302
    assert response.url.startswith(reverse('login'))


@pytest.mark.django_db
def test_message_list_view_logged_in(two_users, messages):
    c = Client()
    c.force_login(two_users[0])
    url = reverse('list_message')
    response = c.get(url)
    msg = response.context["message_list"]
    assert response.status_code == 200
    assert msg.count() == len(messages)


@pytest.mark.django_db
def test_user_auction_list_not_logged():
    c = Client()
    url = reverse('list_user_auctions')
    response = c.get(url)
    assert response.status_code == 302
    assert response.url.startswith(reverse('login'))


@pytest.mark.django_db
def test_user_auction_list_logged_in(user, auctions):
    c = Client()
    c.force_login(user)
    url = reverse('list_user_auctions')
    response = c.get(url)
    user_auctions = response.context_data["object_list"]
    assert response.status_code == 200
    assert user_auctions.count() == len(auctions)


@pytest.mark.django_db
def test_user_bid_list_not_logged():
    c = Client()
    url = reverse('list_user_bids')
    response = c.get(url)
    assert response.status_code == 302
    assert response.url.startswith(reverse('login'))


@pytest.mark.django_db
def test_user_bid_list_logged_in(user, bids):
    c = Client()
    c.force_login(user)
    url = reverse('list_user_bids')
    response = c.get(url)
    user_bids = response.context_data["object_list"]
    assert response.status_code == 200
    assert user_bids.count() == len(bids)


@pytest.mark.django_db
def test_exchange_view_get_not_logged():
    c = Client()
    url = reverse('exchange_view')
    response = c.get(url)
    assert response.status_code == 302
    assert response.url.startswith(reverse('login'))


@pytest.mark.django_db
def test_exchange_view_logged_in(user):
    c = Client()
    c.force_login(user)
    url = reverse('exchange_view')
    response = c.get(url)
    assert response.status_code == 200


@pytest.mark.django_db
def test_exchange_view_post(two_users, auctions):
    c = Client()
    c.force_login(two_users[0])
    url = reverse('exchange_view')
    response = c.post(url, {"proposal": auctions[1].id, "proposal_user": two_users[0], "exchange": auctions[2].id,
                            "counter_offer": 10000})
    assert Exchange.objects.count() == 1
    assert response.status_code == 302


@pytest.mark.django_db
def test_exchange_list_not_logged():
    c = Client()
    url = reverse('exchange_list_view')
    response = c.get(url)
    assert response.status_code == 302
    assert response.url.startswith(reverse('login'))


@pytest.mark.django_db
def test_exchange_list_logged_in(user, exchanges):
    c = Client()
    c.force_login(user)
    url = reverse('exchange_list_view')
    response = c.get(url)
    exchange_test = response.context_data["object_list"]
    assert response.status_code == 200
    assert exchange_test.count() == len(exchanges)


@pytest.mark.django_db
def test_exchange_detail_view_not_logged_in(exchanges):
    c = Client()
    url = reverse('exchange_details', args=(exchanges[0].pk,))
    response = c.get(url)
    assert response.status_code == 302
    assert response.url.startswith(reverse('login'))


@pytest.mark.django_db
def test_exchange_detail_view_logged_in(exchanges, user):
    c = Client()
    c.force_login(user)
    url = reverse('exchange_details', args=(exchanges[0].pk,))
    response = c.get(url)
    assert response.status_code == 200


@pytest.mark.django_db
def test_auction_detail_view_not_logged_in(auctions):
    c = Client()
    url = reverse('auction_details', args=(auctions[0].pk,))
    response = c.get(url)
    assert response.status_code == 302
    assert response.url.startswith(reverse('login'))


@pytest.mark.django_db
def test_auction_detail_view_logged_in(auctions, user):
    c = Client()
    c.force_login(user)
    url = reverse('auction_details', args=(auctions[0].pk,))
    response = c.get(url)
    assert response.status_code == 200


@pytest.mark.django_db
def test_accept_exchange_not_logged_in(auctions):
    c = Client()
    url = reverse('accept_exchange', args=(auctions[0].pk, auctions[1].pk))
    response = c.get(url)
    assert response.status_code == 302
    assert response.url.startswith(reverse('login'))


@pytest.mark.django_db
def test_accept_exchange_logged_in(auctions, user):
    c = Client()
    c.force_login(user)
    url = reverse('accept_exchange', args=(auctions[0].pk, auctions[1].pk))
    response = c.get(url)
    assert response.status_code == 302


@pytest.mark.django_db
def test_decline_exchange_not_logged_in(exchanges):
    c = Client()
    url = reverse('decline_exchange', args=(exchanges[0].pk,))
    response = c.get(url)
    assert response.status_code == 302
    assert response.url.startswith(reverse('login'))


@pytest.mark.django_db
def test_decline_exchange_logged_in(exchanges, user):
    c = Client()
    c.force_login(user)
    url = reverse('decline_exchange', args=(exchanges[0].pk,))
    response = c.get(url)
    assert response.status_code == 302


@pytest.mark.django_db
def test_counteroffer_exchange_not_logged_in(exchanges):
    c = Client()
    url = reverse('counter_exchange', args=(exchanges[0].pk,))
    response = c.get(url)
    assert response.status_code == 302
    assert response.url.startswith(reverse('login'))


@pytest.mark.django_db
def test_counteroffer_exchange_logged_in(exchanges, user):
    c = Client()
    c.force_login(user)
    url = reverse('counter_exchange', args=(exchanges[0].pk,))
    response = c.get(url)
    assert response.status_code == 200


@pytest.mark.django_db
def test_buy_now_list_view_not_logged():
    c = Client()
    url = reverse('buy_now_list')
    response = c.get(url)
    assert response.status_code == 302
    assert response.url.startswith(reverse('login'))


@pytest.mark.django_db
def test_buy_now_list_view_logged_in(user, auctions):
    c = Client()
    c.force_login(user)
    url = reverse('buy_now_list')
    response = c.get(url)
    buy_now_test = response.context_data["object_list"]
    assert response.status_code == 200
    assert buy_now_test.count() == len(auctions)


@pytest.mark.django_db
def test_sell_choice_not_logged_in():
    c = Client()
    url = reverse('sell_choice')
    response = c.get(url)
    assert response.status_code == 302
    assert response.url.startswith(reverse('login'))


@pytest.mark.django_db
def test_sell_choice_logged_in(user):
    c = Client()
    c.force_login(user)
    url = reverse('buy_now_list')
    response = c.get(url)
    assert response.status_code == 200


@pytest.mark.django_db
def test_buy_now_view_get_not_logged():
    c = Client()
    url = reverse('buy_now')
    response = c.get(url)
    assert response.status_code == 302
    assert response.url.startswith(reverse('login'))


@pytest.mark.django_db
def test_buy_now_get_logged(user):
    c = Client()
    c.force_login(user)
    url = reverse('buy_now')
    response = c.get(url)
    assert response.status_code == 200


@pytest.mark.django_db
def test_buy_now_post(two_users):
    c = Client()
    c.force_login(two_users[0])
    url = reverse('buy_now')
    response = c.post(url, {"name": 'test', "description": 'test', "price": 100, "owner": two_users[0],
                            "category": 1})
    assert Auction.objects.count() == 1
    assert response.status_code == 302


@pytest.mark.django_db
def test_buy_now_detail_view_not_logged_in(auctions):
    c = Client()
    url = reverse('buy_now_details', args=(auctions[0].pk,))
    response = c.get(url)
    assert response.status_code == 302
    assert response.url.startswith(reverse('login'))


@pytest.mark.django_db
def test_buy_now_detail_view_logged_in(auctions, user):
    c = Client()
    c.force_login(user)
    url = reverse('buy_now_details', args=(auctions[0].pk,))
    response = c.get(url)
    assert response.status_code == 200

@pytest.mark.django_db
def test_buy_logged_in(auctions, user):
    c = Client()
    c.force_login(user)
    url = reverse('buy', args=(auctions[0].pk,))
    response = c.get(url)
    assert response.status_code == 200


@pytest.mark.django_db
def test_buy_not_logged_in(auctions):
    c = Client()
    url = reverse('buy', args=(auctions[0].pk,))
    response = c.get(url)
    assert response.status_code == 302
    assert response.url.startswith(reverse('login'))

@pytest.mark.django_db
def test_delete_auction_not_logged_in(auctions):
    c = Client()
    url = reverse('auction_delete', args=(auctions[0].pk,))
    response = c.get(url)
    assert response.status_code == 302
    assert response.url.startswith(reverse('login'))


@pytest.mark.django_db
def test_delete_auction_logged_in(auctions, user):
    c = Client()
    c.force_login(user)
    url = reverse('buy', args=(auctions[0].pk,))
    response = c.get(url)
    assert response.status_code == 200