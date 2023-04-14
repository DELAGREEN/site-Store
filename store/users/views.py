from django.shortcuts import render, HttpResponseRedirect
from django.contrib import auth, messages
from django.urls import reverse
from users.forms import UserLoginForm, UserRegistratoinForm, UserProfileForm
from products.models import Basket
from django.contrib.auth.decorators import login_required

def login(request):
    if request.method == 'POST':
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = auth.authenticate(username=username, password=password)
            if user:
                auth.login(request, user)
                return HttpResponseRedirect(reverse('index'))
    else:
        form = UserLoginForm()
    context = {'form': UserLoginForm()}
    return render(request, 'users/login.html', context)


def registration(request):
    if request.method == 'POST':
        form = UserRegistratoinForm(data=request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Поздравляем! Вы успешно зарегестрированны!')
            return HttpResponseRedirect(reverse('users:login'))
    else:
        form = UserRegistratoinForm()
        
    context = {'form': form}
    return render(request, 'users/registration.html', context)


@login_required
def profile(request):
    if request.method == 'POST':
        form = UserProfileForm(instance=request.user, data=request.POST, files=request.FILES)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('users:profile'))
        else:
            print(form.errors)
    else:
        form = UserProfileForm(instance=request.user)

# region important
###    baskets = Basket.objects.filter(user=request.user)


###    total_sum = sum(basket.sum() for basket in baskets)
###    total_quantity = sum(basket.quantity for basket in baskets)

###  total_sum = 0
###  total_quantity = 0
###  for basket in baskets:
###      total_sum = total_sum + basket.sum()
###      total_quantity = total_quantity + basket.quantity

# endregion

    context = {'title': 'Store - Профиль', 
               'form': form,
               'baskets': Basket.objects.filter(user=request.user),

               
               # region important
               #'total_sum' : total_sum,
               #'total_quantity' : total_quantity
               # endregion


               }
    return render(request, 'users/profile.html', context)



def logout(request):
    auth.logout(request)
    return HttpResponseRedirect(reverse('index'))