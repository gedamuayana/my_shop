from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.utils.translation import activate
from decimal import Decimal, InvalidOperation
from .models import UserWallet, DepositRequest, WithdrawRequest


# 1. የተስተካከለው ብጁ ፎርም
class CustomUserCreationForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].help_text = ''


# 2. የተጠቃሚ ምዝገባ
def register_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'አካውንትዎ በሰላም ተፈጥሯል! አሁን መግባት ይችላሉ።')
            return redirect('login')
    else:
        form = CustomUserCreationForm()
    return render(request, 'register.html', {'form': form})


# 3. ዳሽቦርድ
@login_required
def dashboard(request):
    wallet, created = UserWallet.objects.get_or_create(user=request.user)
    return render(request, 'dashboard.html', {'wallet': wallet})


# 4. ተቀማጭ መላኪያ
@login_required
def submit_deposit(request):
    if request.method == 'POST':
        amount = request.POST.get('amount')
        screenshot = request.FILES.get('screenshot')
        if amount and screenshot:
            DepositRequest.objects.create(user=request.user, amount=amount, cbe_screenshot=screenshot)
            messages.success(request, "የክፍያ ማረጋገጫዎ ደርሶናል!")
            return redirect('dashboard')
        messages.error(request, "እባክዎ መረጃዎችን በትክክል ይሙሉ!")
    return render(request, 'deposit.html')


# 5. የዕለታዊ ኦርደር ሎጂክ
@login_required
def complete_order(request):
    if request.method == 'POST':
        try:
            wallet = UserWallet.objects.get(user=request.user)
            if wallet.daily_orders_done < 1:
                wallet.balance += 100
                wallet.daily_orders_done += 1
                wallet.save()
                return JsonResponse({'status': 'success', 'message': 'እንኳን ደስ አለዎት! 100 ብር ተጨምሯል።'})
            return JsonResponse({'status': 'error', 'message': 'የዛሬውን ኦርደር ጨርሰዋል!'})
        except UserWallet.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Wallet አልተገኘም!'})
    return JsonResponse({'status': 'error', 'message': 'የተሳሳተ ጥያቄ!'})


# 6. ገንዘብ ማውጫ (Withdraw)
@login_required
def withdraw_view(request):
    wallet = UserWallet.objects.get(user=request.user)
    if request.method == 'POST':
        amount_str = request.POST.get('amount')
        bank_name = request.POST.get('bank_name')
        bank_account = request.POST.get('bank_account')

        if not amount_str or not bank_name or not bank_account:
            messages.error(request, "ሁሉም መረጃዎች መሞላት አለባቸው!")
            return render(request, 'withdraw.html', {'wallet': wallet})

        try:
            amount_dec = Decimal(amount_str)
            if amount_dec <= 0:
                messages.error(request, "ትክክለኛ መጠን ያስገቡ!")
            elif wallet.balance >= amount_dec:
                WithdrawRequest.objects.create(user=request.user, amount=amount_dec, bank_name=bank_name,
                                               bank_account=bank_account)
                wallet.balance -= amount_dec
                wallet.save()
                messages.success(request, "ጥያቄዎ በተሳካ ሁኔታ ተልኳል!")
                return redirect('dashboard')
            else:
                messages.error(request, "በቂ ሂሳብ የለዎትም!")
        except (InvalidOperation, ValueError, TypeError):
            messages.error(request, "ቁጥር ብቻ ያስገቡ!")
    return render(request, 'withdraw.html', {'wallet': wallet})


# 7. ሌሎች ረዳት ተግባራት
def home_view(request):
    return render(request, 'home.html')


def set_language_view(request):
    if request.method == 'POST':
        lang = request.POST.get('language')
        if lang:
            activate(lang)
            request.session['django_language'] = lang
    return HttpResponseRedirect(request.POST.get('next', '/'))


def direct_password_reset(request):
    if request.method == 'POST':
        try:
            user = User.objects.get(username=request.POST.get('username'))
            password = request.POST.get('password')
            confirm = request.POST.get('confirm_password')
            if password and password == confirm:
                user.set_password(password)
                user.save()
                messages.success(request, 'ፓስወርድ ተቀይሯል!')
                return redirect('login')
            messages.error(request, 'ፓስወርድ አይመሳሰልም!')
        except User.DoesNotExist:
            messages.error(request, 'ዩዘር ስም አልተገኘም!')
    return render(request, 'registration/direct_reset.html')