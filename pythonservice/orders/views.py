# from django.shortcuts import render
# from rest_framework import viewsets,permissions
# from rest_framework.permissions import AllowAny
# from .models import Orders
# from .serializers import OrderSerializer
# import africastalking
# from django.conf import settings
# from rest_framework.response import Response

# user_name = settings.AFRICASTKNG_USERNAME
# api_key = settings.AFRICASTKNG_API_KEY

# africastalking.initialize(username=user_name,api_key=api_key)


# class OrderViewSet(viewsets.ModelViewSet):
#     # permission_classes = [AllowAny]
#     permission_classes = [permissions.IsAuthenticated]
#     queryset =Orders.objects.all()
#     serializer_class = OrderSerializer

#     def perform_create(self, serializer):
#         # Save the order
#         instance = serializer.save()

#         # Prepare the SMS message
#         customer_phone_number = instance.customer.phone_number

#         order_message = f"Thank you for your order! Your order for {instance.item} has been successfully placed."

#         sender = 14489

#         # Access the SMS service
#         sms = africastalking.SMS

#         try:
#             response = sms.send(message=order_message, recipients=[customer_phone_number])

#             if response['SMSMessageData']['Recipients'][0]['status'] == 'Success':
#                 return Response(serializer.data)
#             else:
#                 return Response({"error": "Failed to send SMS"}, status=500)
#         except Exception as e:
#             print("An error occurred while sending SMS:", e)
#             return Response({"error": "Failed to send SMS"}, status=500)


from django.shortcuts import render
from rest_framework import viewsets, permissions
from rest_framework.permissions import AllowAny
from .models import Orders
from .serializers import OrderSerializer
import africastalking
from django.conf import settings
from rest_framework.response import Response

user_name = settings.AFRICASTKNG_USERNAME
api_key = settings.AFRICASTKNG_API_KEY

africastalking.initialize(username=user_name, api_key=api_key)

class send_sms():
    def __init__(self):
        self.sms = africastalking.SMS

    def send(self, message, recipients, sender):
        try:
            response = self.sms.send(message, recipients, sender)
            print(response)
        except Exception as e:
            print(f"Houston, we have a problem: {e}")

class OrderViewSet(viewsets.ModelViewSet):
    # permission_classes = [AllowAny]
    permission_classes = [permissions.IsAuthenticated]
    queryset = Orders.objects.all()
    serializer_class = OrderSerializer

    def perform_create(self, serializer):
        # Save the order
        instance = serializer.save()

        # Prepare the SMS message
        customer_phone_number = instance.customer.phone_number
        order_message = f"Thank you for your order! Your order for {instance.item} has been successfully placed."
        sender = 14489  # Replace with your sender ID or shortcode

        # Create an instance of the send_sms class
        sms_sender = send_sms()

        # Send the SMS notification
        response = sms_sender.send(order_message, [customer_phone_number], sender)

        if response is not None and 'SMSMessageData' in response and 'Recipients' in response['SMSMessageData']:
           if response['SMSMessageData']['Recipients'][0]['status'] == 'Success':
               return Response(serializer.data)
           else:
                return Response({"error": "Failed to send SMS"}, status=500)
        else:
            return Response({"error": "Failed to send SMS"}, status=500)