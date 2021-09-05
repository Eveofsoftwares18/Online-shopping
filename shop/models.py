import datetime

from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse



Categories = (
    (1, 'auction'),
    (2, 'buynow'),
    (3, 'exchange')
)




class Auction(models.Model):
    name = models.CharField(max_length=256)
    description = models.CharField(max_length=512)
    price = models.FloatField()
    end_date = models.DateField(null=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    today = datetime.date.today()
    sold = models.BooleanField(null=False, default=False)
    category = models.IntegerField(choices=Categories)


    def __str__(self):
        return f"{self.name}"

    def get_absolute_url(self):
        return reverse("auction_details", args=(self.pk,))


class Bid(models.Model):
    auction = models.ForeignKey(Auction, on_delete=models.CASCADE, null=True)
    bidder = models.ForeignKey(User, on_delete=models.CASCADE)
    price = models.FloatField()
    date = models.DateField(auto_now_add=True)


    def __str__(self):
        return f"name: {self.auction.name} bid: {self.price}"


class Message(models.Model):
    from_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent')
    to_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received')
    text = models.TextField()


class Exchange(models.Model):
    proposal = models.ForeignKey(Auction, on_delete=models.CASCADE, related_name='proposed')
    proposal_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='proposal_user')
    exchange = models.ForeignKey(Auction, on_delete=models.CASCADE, related_name='exchange')
    counter_offer = models.FloatField(null=True)

    def __str__(self):
        return f"User: {self.proposal_user} is proposing {self.proposal} for {self.exchange}. Additional payment is {self.counter_offer}"
