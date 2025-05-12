# views.py
from django.shortcuts import render, redirect, get_object_or_404
from .models import Auction, AuctionItem
from django.db.models import Q
from .forms import AuctionForm, AuctionItemForm
from django.shortcuts import render, redirect


def auction_list(request):
    auctions = Auction.objects.all()
    breadcrumbs = [
        {'name': 'Home', 'url': '/'},
        {'name': 'Auction', 'url': ''}
    ]
    return render(request, 'auction_list.html', {'auctions': auctions, 'breadcrumbs': breadcrumbs})


def create_auction(request):
    if request.method == 'POST':
        form = AuctionForm(request.POST, request.FILES)  # Add request.FILES if dealing with files
        if form.is_valid():
            form.save()
            return redirect('auct_list')
    else:
        form = AuctionForm()

    breadcrumbs = [
        {'name': 'Home', 'url': '/'},
        {'name': 'Auctions', 'url': '/auctions/'},
        {'name': 'Create New Auction', 'url': ''},
    ]
    
    return render(request, 'auction_form.html', {'form': form, 'breadcrumbs': breadcrumbs})

def update_auction(request, pk):
    auction = get_object_or_404(Auction, pk=pk)
    if request.method == 'POST':
        form = AuctionForm(request.POST, request.FILES, instance=auction)
        if form.is_valid():
            form.save()
            return redirect('auct_list')
    else:
        form = AuctionForm(instance=auction)

    breadcrumbs = [
        {'name': 'Home', 'url': '/'},
        {'name': 'Auctions', 'url': '/auctions/'},
        {'name': f'Update Auction: {auction.title}', 'url': ''},
    ]
    
    return render(request, 'auction_form.html', {'form': form, 'breadcrumbs': breadcrumbs})


def auction_detail(request, pk):
    auction = get_object_or_404(Auction, pk=pk)
    breadcrumbs = [
        {'name': 'Home', 'url': '/'},
        {'name': 'Auction', 'url': '/auctions/'},
        {'name': auction.title, 'url': ''}  # Assuming 'title' is a field in your Auction model
    ]
    return render(request, 'auction_detail.html', {'auction': auction, 'breadcrumbs': breadcrumbs})


def create_auction_item(request, auction_pk, item_pk=None):
    auction = get_object_or_404(Auction, pk=auction_pk)
    if item_pk:
        # Editing an existing auction item
        item = get_object_or_404(AuctionItem, pk=item_pk, auction=auction)
    else:
        # Creating a new auction item
        item = None

    if request.method == 'POST':
        form = AuctionItemForm(request.POST, request.FILES, instance=item)
        if form.is_valid():
            item = form.save(commit=False)
            item.auction = auction
            item.save()
            return redirect('auct_detail', pk=auction_pk)
    else:
        form = AuctionItemForm(instance=item)

    breadcrumbs = [
        {'name': 'Home', 'url': '/'},
        {'name': 'Auctions', 'url': '/auctions/'},
        {'name': auction.title, 'url': f'/auctions/{auction.pk}/'},
        {'name': 'Edit Item' if item else 'Add New Item', 'url': ''}
    ]
    
    return render(request, 'auction_item_form.html', {'form': form, 'auction': auction, 'breadcrumbs': breadcrumbs})

def delete_auction(request, pk):
    auction = get_object_or_404(Auction, pk=pk)
    
    if request.method == 'POST':
        auction.delete()  # This will also delete related auction items because of the ForeignKey with CASCADE
        return redirect('auct_list')  # Redirect to the auction list after deletion
    
    return render(request, 'auction_confirm_delete.html', {'auction': auction})

def delete_auction_item(request, auction_pk, item_pk):
    
    auction = get_object_or_404(Auction, pk=auction_pk)
    auction_item = get_object_or_404(AuctionItem, pk=item_pk)
    
    if request.method == 'POST':
        auction_item.delete()  # Delete the auction item
        return redirect('auct_detail', pk=auction_pk)  # Redirect back to the auction detail page
    
    return render(request, 'auction_item_confirm_delete.html', {'auction_item': auction_item, 'auction': auction})







   




