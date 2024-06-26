from django.shortcuts import render
from rest_framework import viewsets,permissions
from .models import Customers
from .serializers import CustomersSerializer


class CustomerViewSet(viewsets.ModelViewSet):
    # permission_classes = [AllowAny]
    permission_classes = [permissions.IsAuthenticated]
    queryset = Customers.objects.all()
    serializer_class = CustomersSerializer

