from django.shortcuts import render, get_object_or_404
from django.contrib.auth.models import User
from wallet.models import Wallet
from wallet.models import WalletTransaction

# Create your views here.

def wallet(request, user_id):
    user = get_object_or_404(User, id=user_id)
    
    
    wallet, created = Wallet.objects.get_or_create(user=user, defaults={'balance': 0.00})

    
    filter_type = request.GET.get('filter', 'all').lower()
    
    
    if filter_type == 'debited':
        wallet_details = WalletTransaction.objects.filter(wallet=wallet, transaction_type='Debited').order_by('-created_at')
    elif filter_type == 'refund':
        wallet_details = WalletTransaction.objects.filter(wallet=wallet, transaction_type='Refund').order_by('-created_at')
    elif filter_type == 'cancellation':
        wallet_details = WalletTransaction.objects.filter(wallet=wallet, transaction_type='Cancellation').order_by('-created_at')
    else:  
        wallet_details = WalletTransaction.objects.filter(wallet=wallet).order_by('-created_at')



    
    context = {
        'wallet': wallet,
        'wallet_details': wallet_details,
        'selected_filter': filter_type
    }

    return render(request, 'user/wallet.html', context)