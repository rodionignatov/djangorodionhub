from django.core.management import BaseCommand
from django.contrib.auth.models import User
from typing import Sequence
from django.db import transaction
from mysite.shopapp.models import Oreder, Product
class Command(BaseCommand):
    @transaction.atomic
    def handle(self, *args, **options):
        self.stdout.write("Create order with products")
        user = User.objects.get(username="admin")
        products: Sequence[Product] = Product.objects.only("id").all()
        order = Oreder.objects.get_or_create(
            delivery_address="ul Voronova d 18",
            promovode="promo4",
            user=user,

        )
        for product in products:
            order.product.add(product)

        self.stdout.write(f"Created order {order}")
