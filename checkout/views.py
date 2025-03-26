from rest_framework.generics import CreateAPIView

from checkout.models import Checkout
from checkout.serializers import CheckoutSerializer


class CheckoutAPIView(CreateAPIView):
    queryset = Checkout.objects.all()
    serializer_class = CheckoutSerializer
