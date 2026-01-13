#from audioop import reverse
from http.client import responses
from trace import Trace
from django.views import View
from django.contrib.auth.decorators import login_required, permission_required, user_passes_test
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import LogoutView
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.template.context_processors import request
from django.urls import reverse_lazy, reverse
from django.views.generic import TemplateView, CreateView, UpdateView
from django.utils.translation import gettext_lazy as _, ngettext
from .models import Profile

class HelloView(View):
    wellcome_message = _("welcome hello world")
    def get(self, request: HttpRequest) -> HttpResponse:
        items_str = request.GET.get("items") or 0
        items = int(items_str)
        products_line = ngettext(
            "one product",
            "{count} products",
            items,
        )
        products_line = products_line.format(count=items)
        return HttpResponse(
            f"<h1>{self.wellcome_message}</h1>"
            f"\n<h2>{products_line}</h2>"
        )



#class AboutMeView(TemplateView):
#    template_name = "myauth/about-me.html"
#    fields = "avatar",

class AboutMeView(UpdateView):
    template_name = "myauth/about-me.html"
    model = Profile
    fields = "avatar",

    success_url = reverse_lazy("myauth:about-me")

    def get_object(self, queryset=None):
        return self.request.user.profile

class RegisterView(CreateView):
    form_class = UserCreationForm
    template_name = "myauth/register.html"
    success_url = reverse_lazy("myauth:about-me")

    def form_valid(self, form):
        response = super().form_valid(form)
        Profile.objects.create(user=self.object)

        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password1")

        user = authenticate(self.request, username=username, password=password)
        login(request=self.request, user=user)
        form.instance.created_by = self.request.user
        return super().form_valid(form)





def login_view(request: HttpRequest) -> HttpResponse:
    if request.method == "GET":
        if request.user.is_authenticated:
            return redirect('/admin/')

        return render(request, 'myauth/login.html')

    username = request.POST["username"]
    password = request.POST["password"]

    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        return redirect('/admin/')

    return render(request, "myauth/login.html", {"error": "Invalid login credentials"})




def logout_view(request: HttpRequest):
    logout(request)
    return redirect(reverse("myauth:login"))



class MyLogoutView(LogoutView):
    next_page = reverse_lazy("myauth:login")



def set_cookie_view(request: HttpRequest) -> HttpResponse:
    response = HttpResponse("Cookie set")
    response.set_cookie("fizz", "buzz", max_age=3600)
    return response



@user_passes_test(lambda u: u.is_superuser)
def get_cookie_view(request: HttpRequest) -> HttpResponse:
    value = request.COOKIES.get("fizz", "default value")
    return HttpResponse(f"Cookie value: {value!r}")


@permission_required("myauth.view_profile", raise_exception=True)
def set_session_view(requset: HttpRequest) -> HttpResponse:
    requset.session["foobar"] = "spameggs"
    return HttpResponse("Session set!")


@login_required
def get_session_view(requset: HttpRequest) -> HttpResponse:
    value = requset.session.get("foobar", "default")
    return HttpResponse(f"Session value: {value!r}")


