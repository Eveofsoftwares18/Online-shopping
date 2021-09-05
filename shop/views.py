from datetime import datetime, date

from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.shortcuts import render, redirect

# Create your views here.
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView, ListView, DetailView, UpdateView

from shop.forms import AuctionAddForm, BidAddForm, MessageForm, ExchangeForm, ExchangeForm2, BuyNowAddForm
from shop.models import Auction, Bid, Message, Exchange


class IndexView(View):
    def get(self, request):
        return render(request, "base.html")


class AuctionAdd(LoginRequiredMixin, View):
    def get(self, request):
        active_user = request.user.username
        form = AuctionAddForm
        return render(request, "auction_form.html", {"form": form, "active_user": active_user})

    def post(self, request):
        form = AuctionAddForm(request.POST)
        if form.is_valid():
            auction = form.save(commit=False)
            auction.owner = request.user
            auction.category = "1"
            auction.save()
            return redirect('index')
        return render(request, "auction_form.html", {"form": form})


class AuctionList(LoginRequiredMixin, ListView):
    model = Auction
    template_name = "list.html"


class AuctionDetails(LoginRequiredMixin, UpdateView):
    model = Auction
    form_class = AuctionAddForm
    template_name = 'auction_form.html'


class AddBid(LoginRequiredMixin, View):
    def get(self, request, pk):
        auction = Auction.objects.get(id=pk)
        if request.user == auction.owner:
            return redirect('index')
        if auction.end_date <= date.today():
            return redirect('index')
        form = BidAddForm
        return render(request, "auction_form.html", {"form": form, "auction": auction})

    def post(self, request, pk):
        form = BidAddForm(request.POST)
        today = date.today()
        if form.is_valid():
            bid = form.save(commit=False)
            bid.bidder = request.user
            bid.auction = Auction.objects.get(id=pk)
            if bid.bidder == bid.auction.owner:
                return HttpResponse("OWNER CANT BID")
            elif today >= bid.auction.end_date:
                return HttpResponse("AUCTION FINISHED")
            elif bid.price > bid.auction.price:
                auction = Auction.objects.get(id=pk)
                auction.price = bid.price
                auction.save()
                bid.save()
                return redirect('index')
            else:
                return HttpResponse("AUCTION PRICE TOO LOW")
        return render(request, "auction_form.html", {"form": form})


class MessageAddView(LoginRequiredMixin, View):
    def get(self, request):
        form = MessageForm
        return render(request, "message_form.html", {"form": form})

    def post(self, request):
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.from_user = request.user
            message.save()
            return redirect('index')
        return render(request, "message_form.html", {"form": form})


class MessageListView(LoginRequiredMixin, ListView):
    model = Message
    template_name = "message_list.html"

    def get_queryset(self):
        return Message.objects.filter(to_user=self.request.user)


class UserAuctionList(LoginRequiredMixin, ListView):
    model = Auction
    template_name = "user_auctions_list.html"

    def get_queryset(self):
        return Auction.objects.filter(owner=self.request.user)


class UserBidList(LoginRequiredMixin, ListView):
    model = Bid
    template_name = "user_bid_list.html"

    def get_queryset(self):
        return Bid.objects.filter(bidder=self.request.user)


class ExchangeView(LoginRequiredMixin, View):
    def get(self, request):
        form = ExchangeForm()
        form.fields["proposal"].queryset = Auction.objects.filter(owner=self.request.user, sold=False)
        form.fields["exchange"].queryset = Auction.objects.exclude(owner=self.request.user).exclude(sold=True)

        return render(request, 'exchange_form.html', {"form": form})

    def post(self, request):
        form = ExchangeForm(request.POST)
        if form.is_valid():
            exchange = form.save(commit=False)
            exchange.proposal_user = self.request.user
            exchange.counter_offer = 0
            exchange.save()
            return redirect('index')
        return render(request, "message_form.html", {"form": form})


class ExchangeListView(LoginRequiredMixin, ListView):
    model = Exchange
    template_name = "exchange_list.html"

    def get_queryset(self):
        return Exchange.objects.filter(exchange__owner=self.request.user)


class ExchangeDetailView(LoginRequiredMixin, DetailView):
    model = Exchange
    template_name = 'exchange_details.html'


class AcceptExchange(LoginRequiredMixin, View):
    def get(self, request, pk, pk2):
        auction = Auction.objects.get(pk=pk)
        auction.category = "3"
        auction.sold = True
        auction.save()
        auction = Auction.objects.get(pk=pk2)
        auction.sold = True
        auction.save()
        return redirect('exchange_list_view')


class DeclineExchange(LoginRequiredMixin, View):
    def get(self, request, pk):
        exchange = Exchange.objects.get(pk=pk)
        exchange.delete()
        return redirect('exchange_list_view')


class CounterofferExchange(LoginRequiredMixin, UpdateView):
    model = Exchange
    form_class = ExchangeForm2
    template_name = "exchange_form.html"
    success_url = reverse_lazy('exchange_list_view')


class BuyNow(LoginRequiredMixin, CreateView):
    def get(self, request):
        form = BuyNowAddForm
        return render(request, 'form.html', {"form": form})

    def post(self, request):
        form = BuyNowAddForm(request.POST)
        if form.is_valid():
            buynow = form.save(commit=False)
            buynow.owner = self.request.user
            buynow.category = "2"
            buynow.save()
            return redirect('index')
        return render(request, "form.html", {"form": form})


class BuyNowListView(LoginRequiredMixin, ListView):
    model = Auction
    fields = ["description", "owner", "name"]
    template_name = 'buy_now_list.html'


class BuyNowDetailView(LoginRequiredMixin, DetailView):
    model = Auction
    template_name = "buy_now_detail_view.html"


class Buy(LoginRequiredMixin, View):
    def get(self, request, pk):
        auction = Auction.objects.get(pk=pk)
        auction.category = "2"
        auction.sold = True
        auction.save()
        return HttpResponse('Redirecting to your bank')


class SellChoice(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, 'sell_choice.html')


class AuctionDelete(LoginRequiredMixin, View):
    def get(self, request, pk):
        auction = Auction.objects.get(pk=pk)
        auction.delete()
        return HttpResponse('Auction deleted')
