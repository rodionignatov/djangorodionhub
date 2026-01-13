from django.test import TestCase
from Testing.mysite.shopapp.utils import add_two_numbers
from django.urls import reverse
from string import ascii_letters
from random import choices
from models import Product
from django.contrib.auth.models import User
from django.conf import settings

class AddTwoNumbersTestCase(TestCase):
    def test_add_two_numbers(self):
        result = add_two_numbers(2, 3)

        self.assertEquals(result, 5)


class ProductCreateViewTestCase(TestCase):
    def setUp(self) -> None:
        self.product_name = "".join(choices(ascii_letters, k = 10))
        Product.object.filter(name=self.product_name).delete()
    def test_create_product(self):
        response = self.client.post(
            reverse("shopapp:product_create"),
            {
                "name": self.product_name,
                "price": "123.45",
                "description": "Good table",
                "discount": "12",
            }
        )
        self.assertRedirects(response, reverse("shopapp:product_list"))
        self.assertTrue(
            Product.objects.filter(name=self.product_name).exists()
        )

class ProductDetailsViewTestCase(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.product = Product.objects.create(name="Best Product")
    @classmethod
    def tearDownClass(cls):
        cls.product.delete()

    def test_get_product(self):
        response = self.client.get(
            reverse("shopapp:product_details", kwargs={"pk": self.product.pk})
        )
        self.assertEquals(response.status_code, 200)

    def test_get_product_and_chek_content(self):
        response = self.client.get(
            reverse("shopapp:product_details", kwargs={"pk": self.product.pk})
        )
        self.assertContains(response, self.product.name)

class ProductsListViewTestVace(TestCase):
    filteres = [
        'products-fixture.json',

    ]

    def test_products(self):
        response = self.client.get(reverse("shopapp:product_list"))
        self.assertQuerySetEqual(
            qs=Product.object.filter(archived=False).all(),
            values=(p.pk for p in response.context["products"]),
            transform=lambda p: p.pk,
        )
        self.assertTemplateUsed(response, 'shopapp/products-list.html')

class OrdersViewTestCase(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.user = User.objects.create_user(username="mambet_test", password="88ah")
    @classmethod
    def tearDownClass(cls):
        cls.user.delete()
    def setUp(self) -> None:
        self.client.force_login(self.user)
    def test_orders_view(self):
        response = self.client.get(reverse("shopapp:orders_list"))
        self.assertContains(response, "Orders")
    def test_orders_view_not_auntheticated(self):
        self.client.logout()
        response = self.client.get(reverse("shopapp:orders_list"))
        self.assertEquals(response.status_code, 302)
        self.assertIn(str(settings.LOGIN_URL), response.url)

class ProductsExportViewTestCase(TestCase):
    fixtures = [
        'products-fixture.json',
    ]
    def tets_get_products_view(self):
        response = self.client.get(
            reverse("shopapp:products-export"),
        )
        self.assertEqual(response.status_code, 200)
        products = Product.objects.order_by("pk").all()
        expected_data = [
            {
                "pk": product.pk,
                "name": product.name,
                "price": str(product.price),
                "archived": product.archived,

            }
            for product in products
        ]
        products_data = response.json()
        self.assertEqual(
            products_data["products"],
            expected_data,

        )



















