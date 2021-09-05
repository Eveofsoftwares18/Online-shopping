import datetime
from datetime import date

from django.contrib.auth.models import User
import pytest
from shop.models import Auction, Bid, Categories, Exchange, Message


@pytest.fixture
def category():
    u = Categories
    return u


@pytest.fixture
def user():
    u = User()
    u.username = 'cooklee'
    u.set_password("vet")
    u.save()
    return u


@pytest.fixture
def two_users():
    users = []
    for x in range(2):
        u = User()
        u.username = f"{x}"
        u.set_password("vet")
        u.save()
        users.append(u)
    return users


@pytest.fixture
def auctions(user, category):
    ts = []
    for x in range(10):
        t = Auction()
        t.name = 'nazwa'
        t.description = 'jakis content'
        t.owner = user
        t.price = 100
        t.end_date = date.today() + datetime.timedelta(days=1)
        t.category = 3
        t.sold = False
        t.save()
        ts.append(t)
    return ts


@pytest.fixture
def messages(two_users):
    ts = []
    for x in range(10):
        t = Message()
        t.text = 'jakis content'
        t.to_user = two_users[0]
        t.from_user = two_users[1]
        t.save()
        ts.append(t)
    return ts


@pytest.fixture
def exchanges(user, auctions):
    ts = []
    for x in range(10):
        t = Exchange()
        t.proposal = auctions[0]
        t.proposal_user = user
        t.exchange = auctions[1]
        t.counter_offer = 1
        t.save()
        ts.append(t)
    return ts


@pytest.fixture
def bids(user, auctions):
    ts = []
    for x in range(10):
        t = Bid()
        t.auction = auctions[0]
        t.bidder = user
        t.price = 20
        t.date = date.today()
        t.save()
        ts.append(t)
    return ts