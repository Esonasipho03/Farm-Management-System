import json
from django.urls import reverse
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.conf import settings
from django.contrib.auth.decorators import login_required

from app.forms import UserProfileForm
from app.models import Auction, Bid


# Helper function to build breadcrumbs
def build_breadcrumbs(crumbs):
    """
    crumbs: List of tuples in the form (url_name, display_name)
    """
    breadcrumbs = [{'url': reverse(url_name), 'name': display_name} for url_name, display_name in crumbs]
    return breadcrumbs


# Homepage view
def homepage(request):
    breadcrumbs = build_breadcrumbs([('homepage', 'Home')])
    return render(request, 'index.html', {'breadcrumbs': breadcrumbs})


# Auction list



def auctions_list(request):
    # Fetch all the auctions from the management app's Auction model
    auctions = Auction.objects.all()
    # Pass the auctions to the template
    return render(request, 'user/auctions_list.html', {'auctions': auctions})



def auctions_detail(request, pk):
    auction = get_object_or_404(Auction, pk=pk)
    return render(request, 'user/auctions_detail.html', {'auction': auction})


def place_bid(request, auction_id):
    if request.method == 'POST':
        auction = Auction.objects.get(id=auction_id)
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        bid_amount = request.POST.get('bidAmount')

        # Create a new Bid
        Bid.objects.create(auction=auction, name=name, phone=phone, bid_amount=bid_amount)

        # Update the current bid on the auction
        auction.current_bid = bid_amount
        auction.save()

        return JsonResponse({'message': 'Bid placed successfully!'})
    return JsonResponse({'error': 'Invalid request'}, status=400)

def thankyou_view(request):
    name = request.GET.get('name')
    phone = request.GET.get('phone')
    bid_amount = request.GET.get('bidAmount')
    auction_id = request.GET.get('auctionId')
    return render(request, 'user/thankyou.html', {
        'name': name,
        'phone': phone,
        'bid_amount': bid_amount,
        'auction_id': auction_id,
    })
def delete_bid(request, bid_id):
    if request.method == 'POST':
        try:
            bid = Bid.objects.get(id=bid_id)
            bid.delete()
            return JsonResponse({'message': 'Bid deleted successfully!'})
        except Bid.DoesNotExist:
            return JsonResponse({'error': 'Bid not found'}, status=404)
    return JsonResponse({'error': 'Invalid request'}, status=400)


# Delete bid view
def delete_bid(request, bid_id):
    if request.method == 'POST':
        try:
            bid = Bid.objects.get(id=bid_id)
            bid.delete()
            return JsonResponse({'message': 'Bid deleted successfully!'})
        except Bid.DoesNotExist:
            return JsonResponse({'error': 'Bid not found'}, status=404)
    return JsonResponse({'error': 'Invalid request'}, status=400)


# User bids view (login required)
@login_required
def user_bids(request):
    user_bids = Bid.objects.filter(user=request.user)  # Assuming the Bid model has a foreign key to the user
    breadcrumbs = build_breadcrumbs([('homepage', 'Home'), ('user_bids', 'My Bids')])
    return render(request, 'user/user_bids.html', {'user_bids': user_bids, 'breadcrumbs': breadcrumbs})


def account2_view(request):
    user = request.user
    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('account2')  # Redirect to account page after successful update
    else:
        form = UserProfileForm(instance=user)
    
    context = {
        'form': form,
        'user': user,
    }
    return render(request, 'user/account2.html', context)