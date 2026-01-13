"""
В этом модуле лежат различные наборы представлений.

Разные view интернет-магазинов: по товарам, заказам и т. д.
"""

from http.client import HTTPResponse
from itertools import product
from timeit import default_timer

from django.contrib.messages import success
from django.urls import reverse_lazy
from django.views.generic import TemplateView, ListView, DetailView, CreateView, UpdateView, DeleteView
from .forms import ProductForm
from .models import Product, Oreder, ProductImage
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.viewsets import ModelViewSet
from django.contrib.auth.models import Group
from django.http import HttpResponse, HttpRequest, HttpResponseRedirect
from django.shortcuts import render, redirect, reverse, get_object_or_404, reverse
from django.template.context_processors import request
from .models import Product
from .forms import ProductForm, OrderForm
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin, UserPassesTestMixin
from .forms import GroupForm
from django_filters.rest_framework import DjangoFilterBackend
from .serializers import ProductSerializer
from drf_spectacular.utils import extend_schema, OpenApiResponse


@extend_schema(description="Product view CRUD")
class ProductViewSet(ModelViewSet):
    """
    Набор представлений для действий над Product
    Полный CRUD для сущностей товара
    """

    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [
        SearchFilter,
#        DjangoFilterBackend,
#        OrderingFilter,

    ]
    search_fields = ["name", "description"]
    filterset_fields = [
        "name",
        "description",
#        "price",
#        "discount",
#        "archived",

    ]
    ordering_fields = [
        "name",
        "price",
        "discount",
    ]
    @extend_schema(
        summary="Get one product by ID",
        description="Retrieves **product**, returns 404 if not found",
        responses={
            200: ProductSerializer,
            404: OpenApiResponse(description="Empty response, product by id not found"),

        },

    )
    def retrieve(self, *args, **kwargs):
        return super().retrieve(*args, **kwargs)

def create_order(request: HttpRequest)-> HttpResponse:
    if request.method == "POST":
        form = OrderForm(request.POST)
        if form.is_valid():
            form.save()
            url = reverse("shopapp:orders_list")
            return redirect(url)
    else:
        form = OrderForm()
    context = {
        "form": form,
    }
    url = reverse("shopapp:orders_list")
    return render(request, "shopapp/orders.html", context=context)


def create_product(request: HttpRequest) -> HttpResponse:
    if request.method == "POST":
        form = ProductForm(request.POST)
        if form.is_valid():
            #name = form.cleaned_data["name"]
            #price = form.cleaned_data["price"]
            #Product.objects.create(**form.cleaned_data)
            form.save()
            url = reverse("shopapp:products_list")
            return redirect(url)
    else:
        form =  ProductForm()
    context = {
        "form": form,
    }
    url = reverse("shopapp:products_list")
    return render(request, "shopapp/create-product.html", context=context)



class ShopIndexView(View):
    def get(self, request: HttpRequest) -> HttpResponse:
        products = [
            ('Laptop', 1488),
            ('Desktop', 1999),
            ('Iphone', 3000),
        ]
        context = {
            'time_running': default_timer(),
            'products': products,
            'items': 5,
        }
        return render(request, 'shopapp/shop-index.html', context=context)





class GroupsListView(View):
    def get(self, request: HttpRequest) -> HttpResponse:
        context = {
            "form": GroupForm(),
            "groups": Group.objects.prefetch_related('permissions').all(),
        }
        return render(request, 'shopapp/groups-list.html', context=context)

    def post(self, request: HttpRequest):
        form = GroupForm(request.POST)
        if form.is_valid():
            form.save()

        return redirect(request.path)



class ProductDetailsView(DetailView):
    template_name = "shopapp/product-details.html"
    queryset = Product.objects.prefetch_related("images")
    model = Product
    context_object_name = "product"





class ProductsListView(ListView):
    template_name = 'shopapp/products-list.html'
    model = Product
    context_object_name = "products"
    queryset = Product.objects.filter(archived=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["products"] = Product.objects.all()
        return context



class ProductCreateView(CreateView, UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_superuser

    model = Product
    fields = "name", "price", "description", "discount", "preview"
    success_url = reverse_lazy("shopapp:products-list")

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)




class ProductUpdateView(UpdateView):
    model = Product
    #fields = "name", "price", "description", "discount", "preview"
    template_name_suffix = "_update_form"
    form_class = ProductForm

    def get_success_url(self):
        return reverse(
            "shopapp:product_details",
            kwargs={"pk": self.object.pk},
        )
    def form_valid(self, form):
        response = super().form_valid(form)
        for image in form.files.getlist("images"):
            ProductImage.objects.create(
                product=self.object,
                image=image,
            )
        return response


class ProductDeleteView(DeleteView):
    model = Product
    success_url = reverse_lazy("shopapp:products_list")

    def form_valid(self, form):
        success_url = self.get_success_url()
        self.object.archived = True
        self.object.save()
        return HttpResponseRedirect(success_url)



class OrdersListView(ListView, LoginRequiredMixin):
    template_name = 'shopapp/orders_list.html'
    queryset = (
        Oreder.objects
        .select_related("user")
        .prefetch_related("products")
        .all()
    )


class OrderDetailView(DetailView, PermissionRequiredMixin):
    permission_required = "shopapp.view_order"
    template_name = 'shopapp/order_detail.html'
    queryset = (
        Oreder.objects.select_related("user").prefetch_related("products")
    )



