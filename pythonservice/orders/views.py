from django.shortcuts import render
from rest_framework import viewsets
from .models import Orders
from .serializers import OrderSerializer

# Create your views here.
class OrderViewSet(viewsets.ModelViewSet):
    queryset =Orders.objects.all()
    serializer_class = OrderSerializer