from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .models import UserWallet, DepositRequest
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.utils.translation import activate


# የተስተካከለው ብጁ ፎርም (የሁሉንም መስኮች መመሪያ በግልጽ ያጠፋል)
class CustomUserCreationForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if 'username' in self.fields:
            self.fields['username'].help_text = ''
        if 'password' in self.fields:
            self.fields['password'].help_text = ''
        if 'password1' in self.fields:
            self.fields['password1'].help_text = ''
        if 'password2' in self.fields:
            self.fields['password2'].help_text = ''


# 1. የተጠቃሚ ምዝገባ (Register View)
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


# 2. ዋናው የተጠቃሚ ገጽ (Dashboard)
@login_required
def dashboard(request):
    wallet, created = UserWallet.objects.get_or_create(user=request.user)
    context = {
        'wallet': wallet
    }
    return render(request, 'dashboard.html', context)


# 3. 1000 ብር አስገብቶ ስክሪንሾት መላኪያ ገጽ
@login_required
def submit_deposit(request):
    if request.method == 'POST':
        amount = request.POST.get('amount')
        screenshot = request.FILES.get('screenshot')

        if amount and screenshot:
            DepositRequest.objects.create(
                user=request.user,
                amount=amount,
                cbe_screenshot=screenshot
            )
            messages.success(request, "የክፍያ ማረጋገጫዎ በትክክል ደርሶናል! በአድሚን ሲረጋገጥ ብሩ ይገባልሃል።")
            return redirect('dashboard')
        else:
            messages.error(request, "እባክዎ መረጃዎችን በትክክል ይሙሉ!")

    return render(request, 'deposit.html')


# 4. የዕለታዊ ኦርደር ሎጂክ (በቀን 100 ብር መደመሪያ)
@login_required
def complete_order(request):
    if request.method == 'POST':
        wallet = UserWallet.objects.get(user=request.user)

        # በቀን 1 ጊዜ ብቻ እንዲሠራ መገደብ
        if wallet.daily_orders_done < 1:
            wallet.balance += 100
            wallet.daily_orders_done += 1
            wallet.save()
            return JsonResponse({'status': 'success', 'message': 'እንኳን ደስ አለዎት! 100 ብር ወደ አካውንትዎ ተጨምሯል።'})
        else:
            return JsonResponse({'status': 'error', 'message': 'የዛሬውን ኦርደር ጨርሰዋል! እባክዎ ነገ ይመለሱ。'})

    return JsonResponse({'status': 'error', 'message': 'የተሳሳተ ጥያቄ!'})


# 5. ሆም ፔጅ ቪው
def home_view(request):
    return render(request, 'home.html')


def set_language_view(request):
    if request.method == 'POST':
        language = request.POST.get('language')
        next_url = request.POST.get('next', '/')
        if language:
            activate(language)
            request.session['django_language'] = language
        return HttpResponseRedirect(next_url)
    return HttpResponseRedirect('/')


# 6. ቀጥታ የይለፍ ቃል መቀየሪያ (ከተረጋገጫ ጋር)
def direct_password_reset(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        new_password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        # የይለፍ ቃሎቹ መመሳሰላቸውን ማረጋገጥ
        if new_password != confirm_password:
            messages.error(request, 'የይለፍ ቃሎቹ አይመሳሰሉም፤ እባክዎን ደግመው ይሞክሩ።')
            return render(request, 'registration/direct_reset.html')

        try:
            user = User.objects.get(username=username)
            user.set_password(new_password)
            user.save()
            messages.success(request, 'የይለፍ ቃልዎ በተሳካ ሁኔታ ተቀይሯል! አሁን በአዲሱ ፓስወርድ መግባት ይችላሉ።')
            return redirect('login')
        except User.DoesNotExist:
            messages.error(request, 'ይህ ዩዘር ስም አልተገኘም፤ እባክዎን በትክክል ያስገቡ።')

    return render(request, 'registration/direct_reset.html')