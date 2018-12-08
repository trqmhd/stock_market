from django.shortcuts import render
from user_info.forms import UserForm, UserProfileInfoForm
from django.urls import reverse
# from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.utils.http import is_safe_url
from django.shortcuts import redirect

# Create your views here.
def index(request):
    #print(request.session.get("first_name", "Unknown")) #set
    return render(request, 'user_info/index.html')


@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))


@login_required
def special(request):
    return HttpResponse("You are Logged In 👍 ")


def register(request):
    registered = False

    if request.method == "POST":
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileInfoForm(data=request.POST)

        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()

            profile = profile_form.save(commit=False)
            profile.user = user

            if 'profile_pic' in request.FILES:
                profile.profile_pic = request.FILES['profile_pic']

            profile.save()

            registered = True

        else:
            print(user_form.errors, profile_form.errors)

    else:
        user_form = UserForm()
        profile_form = UserProfileInfoForm()

    return render(request, 'user_info/registration.html',
                  {'user_form': user_form,
                   'profile_form': profile_form,
                   'registered': registered})


def user_login(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)
        # next_ = request.GET.get('next')
        # next_post = request.POST.get('next')
        # redirect_path = next_ or next_post or None
        if user:
            if user.is_active:
                login(request, user)
                    # if is_safe_url(redirect_path, request.get_host()):
                    #     return (redirect_path)
                    # # else:
                    # #     return redirect("/")

                return HttpResponseRedirect(reverse('index'))

            else:
                return HttpResponse("Not registered")

        else:
            print("Someone tried to login and failed")
            print("Username: {} and Password {}".format(username, password))
            return HttpResponse("Invalid login details supplied")

    else:
        return render(request, 'user_info/login.html', {})
