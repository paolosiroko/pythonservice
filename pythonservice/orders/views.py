from django.shortcuts import render
from rest_framework import viewsets
from .models import Orders
from .serializers import OrderSerializer
import africastalking
from django.conf import settings
from rest_framework.response import Response

# user_name = settings.AFRICASTKNG_USERNAME
# api_key = settings.AFRICASTKNG_API_KEY

africastalking.initialize(username=user_name,api_key=api_key)


class OrderViewSet(viewsets.ModelViewSet):
    queryset =Orders.objects.all()
    serializer_class = OrderSerializer

    def perform_create(self, serializer):
        # Save the order
        instance = serializer.save()

        # Prepare the SMS message
        customer_phone_number = instance.customer.phone_number

        order_message = f"Thank you for your order! Your order for {instance.item} has been successfully placed."

        # Access the SMS service
        sms = africastalking.SMS

        try:
            response = sms.send(message=order_message, recipients=[customer_phone_number])

            if response['SMSMessageData']['Recipients'][0]['status'] == 'Success':
                return Response(serializer.data)
            else:
                return Response({"error": "Failed to send SMS"}, status=500)
        except Exception as e:
            print("An error occurred while sending SMS:", e)
            return Response({"error": "Failed to send SMS"}, status=500)