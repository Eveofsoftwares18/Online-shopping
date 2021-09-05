from django import forms

from shop.models import Auction, Bid, Message, Exchange


class AuctionAddForm(forms.ModelForm):
    class Meta:
        model = Auction
        fields = ['name', 'description', 'price', 'end_date']
        widgets = {
            'end_date': forms.SelectDateWidget()
        }

class BuyNowAddForm(forms.ModelForm):
    class Meta:
        model = Auction
        fields = ['name', 'description', 'price']


class BidAddForm(forms.ModelForm):
    class Meta:
        model = Bid
        fields = ["price"]


class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['to_user', 'text']


class ExchangeForm(forms.ModelForm):
    class Meta:
        model = Exchange
        fields = ['proposal', 'exchange']

class ExchangeForm2(forms.ModelForm):
    class Meta:
        model = Exchange
        fields = ['counter_offer']




