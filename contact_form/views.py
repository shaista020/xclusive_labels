from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.core.mail import send_mail
from .serializers import *
from contact_form.models import *
from adminside.models import *
from django.conf import settings
from django.shortcuts import render,redirect
from rest_framework import viewsets
from django.contrib.auth.decorators import login_required,user_passes_test
from rest_framework.decorators import action
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.contrib import messages
from django.utils.timezone import now
import pytz
import uuid
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404, render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import get_user_model
import csv
import time
from django.http import HttpResponse
from django.core.files.storage import FileSystemStorage
from django.conf import settings
from django.db.models import Sum
from decimal import Decimal
from django.template.loader import get_template
from xhtml2pdf import pisa
from contact_form.send_mail import send_ticket_update_email 
from contact_form.notification import notification_create
class ContactInfoView(APIView):
    def post(self, request):
        serializer = ContactInfoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()


            name = serializer.validated_data['name']
            email = serializer.validated_data['email']
            message = serializer.validated_data['message']


            subject = f"New Contact Info from {name}"
            email_message = f"Name: {name}\nEmail: {email}\nMessage:\n{message}"
            recipient_list = [email]

            try:

                send_mail(
                    subject,
                    email_message,
                    settings.EMAIL_HOST_USER,
                    recipient_list,
                    fail_silently=False,
                )


                return Response(
                    {"message": "Contact information submitted successfully and email sent!"},
                    status=status.HTTP_201_CREATED
                )
            except Exception as e:
                return Response(
                    {"error": "Failed to send email", "details": str(e)},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



    def get(self, request):
        contacts = ContactInfo.objects.all()
        serializer = ContactInfoSerializer(contacts, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class PackageView(APIView):
    permission_classes = [IsAuthenticated]  
    
    def get(self, request):
        packages = Package.objects.all()  
        serializer = SavePackageSerializer(packages, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        data = request.data
        data['user'] = request.user.id 
        serializer = SavePackageSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

 
class TicketView(APIView):
    permission_classes = [IsAuthenticated] 
    def get(self, request, ticket_id=None):
        if ticket_id:
            try:
                if request.user.is_staff: 
                    ticket = Ticket.objects.get(id=ticket_id)  
                else:
                    ticket = Ticket.objects.get(id=ticket_id, user=request.user)  
                serializer = TicketSerializer(ticket)
                return Response(serializer.data, status=status.HTTP_200_OK)
            except Ticket.DoesNotExist:
                return Response({"error": "Ticket not found"}, status=status.HTTP_404_NOT_FOUND)
        else:
            if request.user.is_staff: 
                tickets = Ticket.objects.all()
            else:
                tickets = Ticket.objects.filter(user=request.user)  
            serializer = TicketSerializer(tickets, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        data = request.data
        data['user'] = request.user.id

        serializer = TicketSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    def put(self, request, ticket_id):
        try:
            if request.user.is_staff:  
                ticket = Ticket.objects.get(id=ticket_id)
            else:
                ticket = Ticket.objects.get(id=ticket_id, user=request.user) 
        except Ticket.DoesNotExist:
            return Response({"error": "Ticket not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = TicketSerializer(ticket, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    @action(detail=True, methods=['post'])
    def close(self, request, ticket_id=None):
        """
        Close a ticket.
        """
        try:
            if request.user.is_staff:  
                ticket = Ticket.objects.get(id=ticket_id)
            else:
                ticket = Ticket.objects.get(id=ticket_id, user=request.user) 
            ticket.status = "Closed"
            ticket.save()
            return Response({"message": "Ticket closed successfully", "status": "Closed"}, status=status.HTTP_200_OK)
        except Ticket.DoesNotExist:
            return Response({"error": "Ticket not found"}, status=status.HTTP_404_NOT_FOUND)


class OrderView(APIView):

    def get(self,request):
        orders = Order.objects.all()
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)
    def post(self,request):
        serializer = OrderSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PaymentView(APIView):
    def get(self,request):
        Payments = Payment.objects.all()
        serializer = PaymentSerializer(Payments, many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)
    def post(self,request):
        serializer = PaymentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class AddFundView(APIView):
    def get(self,request):
        funds = AddFund.objects.all()
        serializer = AddFundSerializer(funds, many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)
    def post(self,request):
        serializer = AddFundSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class AddressView(APIView):
    permission_classes = [IsAuthenticated]  
    def get(self, request, pk=None):
        if request.user.is_staff:
            addresses = Address.objects.all()  
        elif pk:
            try:
                address = Address.objects.get(pk=pk, user=request.user)
            except Address.DoesNotExist:
                return Response({"error": "Address not found or not authorized"}, status=status.HTTP_404_NOT_FOUND)
            return Response(AddressSerializer(address).data, status=status.HTTP_200_OK)
        else:
            addresses = Address.objects.filter(user=request.user)

        serializer = AddressSerializer(addresses, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        data = request.data
        data['user'] = request.user.id

        serializer = AddressSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk):
        try:
            address = Address.objects.get(pk=pk, user=request.user)
        except Address.DoesNotExist:
            return Response({"error": "Address not found or not authorized"}, status=status.HTTP_404_NOT_FOUND)

        serializer = AddressSerializer(address, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        try:
            address = Address.objects.get(pk=pk, user=request.user)
        except Address.DoesNotExist:
            return Response({"error": "Address not found or not authorized"}, status=status.HTTP_404_NOT_FOUND)

        address.delete()
        return Response({"message": "Address deleted successfully"}, status=status.HTTP_204_NO_CONTENT)

class ShipFromAddressView(APIView):
    def get(self, request):
        addresses = ShipFromAddress.objects.all()
        serializer = ShipFromAddressSerializer(addresses, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = ShipFromAddressSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ProfileView(APIView):

    def get(self, request):
        profile = Profile.objects.get(user=request.user)
        serializer = ProfileSerializer(profile)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = ProfileSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            print(serializer,"a")
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class StoreView(APIView):
    permission_classes = [IsAuthenticated]  

    def get(self, request, pk=None):
        if pk:        
            try:
                store = Store.objects.get(pk=pk, user=request.user)  
            except Store.DoesNotExist:
                return Response({"detail": "Store not found."}, status=status.HTTP_404_NOT_FOUND)

            serializer = StoreSerializer(store)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            stores = Store.objects.filter(user=request.user)  
            serializer = StoreSerializer(stores, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        data = request.data
        data['user'] = request.user.id

        serializer = StoreSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk):
        try:
            address = Store.objects.get(pk=pk, user=request.user)
        except Store.DoesNotExist:
            return Response({"error": "Address not found or not authorized"}, status=status.HTTP_404_NOT_FOUND)

        serializer = StoreSerializer(address, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        try:
            store = Store.objects.get(pk=pk, user=request.user) 
        except Store.DoesNotExist:
            return Response({"detail": "Store not found."}, status=status.HTTP_404_NOT_FOUND)

        store.delete()
        return Response({"detail": "Store deleted successfully."}, status=status.HTTP_204_NO_CONTENT)

class CouponView(APIView):
    def get(self, request):
        coupons = Coupon.objects.filter(is_active=True)
        serializer = CouponSerializer(coupons, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = CouponSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class DeleteAccountView(APIView):
    def delete(self, request):
        user = request.user
        user.delete()

def referrals_view(request):
    referrals = CustomUser.objects.filter(referred_by=request.user)
    referral_commission = referrals.aggregate(Sum('available_for_withdraw'))['available_for_withdraw__sum'] or Decimal('0.00')
    user_own_commission = request.user.available_for_withdraw
    total_commission = referral_commission + user_own_commission
    referral_link = request.build_absolute_uri(f'/auth/signup/?referral_code={request.user.referral_code}')

    context = {
        'referrals': referrals,
        'referral_commission': referral_commission,  
        'user_own_commission': user_own_commission,  
        'total_commission': total_commission,     
        'referral_link': referral_link,
    }

    return render(request, "User/Referrals.html", context)

 
 
class NotificationViewSet(viewsets.ModelViewSet):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer
    permission_classes = [IsAuthenticated]
    def perform_create(self, serializer):
        # Automatically set created_by from the authenticated user
        serializer.save(created_by=self.request.user)
    @action(detail=False, methods=["delete"], permission_classes=[IsAuthenticated])
    def delete_notifications(self, request):
     """Delete all notifications for the current user."""
     self.get_queryset().delete()
     return Response({"message": "All notifications deleted."}, status=200)
    @action(detail=False, methods=["patch"], permission_classes=[IsAuthenticated])
    def mark_as_read(self, request):
        """Mark all notifications as read for the current user."""
        notifications = self.get_queryset().filter(is_read=False)
        notifications.update(is_read=True)
        return Response({"message": "All notifications marked as read."}, status=200)

    
 
    def get_queryset(self):
        """Return notifications for the user. Admins see all notifications."""
        if self.request.user.is_staff:
            return self.queryset   
        else:
            return self.queryset.filter(Q(user=self.request.user) | Q(is_global=True))

    @action(detail=False, methods=["get"], permission_classes=[IsAuthenticated])
    def get_notifications(self, request):
        """Fetch user notifications and print debug logs."""
        
        print(f"\n🔍 DEBUG: User '{request.user.username}' requested notifications.")

        notifications = self.get_queryset().order_by("-created_at")

        if not notifications.exists():
            print("⚠️ DEBUG: No notifications found for this user.")

        data = []
        for n in notifications:
            created_by_name = n.created_by.full_name if n.created_by else "Admin"
            print(f"✅ DEBUG: Notification ID={n.id}, Message='{n.message}', Created By={created_by_name}")

            data.append({
                "id": n.id,
                "message": n.message,
                "is_read": n.is_read,
                "created_at": n.created_at.strftime("%Y-%m-%d %H:%M:%S"),
                "username": created_by_name,
            })

        print("✅ DEBUG: Finished processing notifications, returning response.\n")
        return Response(data)

 

class newLabelView(APIView):
   

    def get(self, request, pk=None):
        user = request.user 
        if pk:  
            try:
                label = NewLabel.objects.get(pk=pk)

                if user.is_staff or label.user == user:
                    serializer = LabelSerializer(label)
                    return Response(serializer.data)
                else:
                    return Response(
                        {"error": "You do not have permission to view this label"},
                        status=status.HTTP_403_FORBIDDEN
                    )

            except NewLabel.DoesNotExist:
                return Response(
                    {"error": "Label not found"},
                    status=status.HTTP_404_NOT_FOUND
                )

        else: 
            if user.is_staff: 
                labels = NewLabel.objects.all()
            else: 
                labels = NewLabel.objects.filter(user=user)

            serializer = LabelSerializer(labels, many=True)
            return Response(serializer.data)

    def post(self, request):
        
        data = request.data
        data['user'] = request.user.id 
        serializer = LabelSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk):
        try:
            label = NewLabel.objects.get(pk=pk)

            
            if not (request.user.is_staff or label.user == request.user):
                return Response(
                    {"error": "You do not have permission to update this label"},
                    status=status.HTTP_403_FORBIDDEN
                )

        except NewLabel.DoesNotExist:
            return Response({"error": "Label not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = LabelSerializer(label, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
       
        try:
            label = NewLabel.objects.get(pk=pk)
            if not (request.user.is_staff or label.user == request.user):
                return Response(
                    {"error": "You do not have permission to delete this label"},
                    status=status.HTTP_403_FORBIDDEN
                )

        except NewLabel.DoesNotExist:
            return Response({"error": "Label not found"}, status=status.HTTP_404_NOT_FOUND)

        label.delete()
        return Response({"message": "Label deleted successfully"}, status=status.HTTP_204_NO_CONTENT)

class TopStatesView(APIView):
    def get(self, request):
        data = StateShipmentData.objects.all().order_by('-shipments_percentage')  
        serializer = StateShipmentDataSerializer(data, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
class TransactionViewSet(viewsets.ModelViewSet):
    queryset = Transaction.objects.all().order_by('-created_at')  
    serializer_class = TransactionSerializer

@login_required(login_url="/auth/signin/")
def dashboard(request):
    user_notifications = Notification.objects.filter(user=request.user)
    global_notifications = Notification.objects.filter(is_global=True)
    referrals = CustomUser.objects.filter(referred_by=request.user)
    referral_commission = referrals.aggregate(Sum('available_for_withdraw'))['available_for_withdraw__sum'] or Decimal('0.00')
    user_own_commission = request.user.available_for_withdraw
    total_commission = referral_commission + user_own_commission
    return render(request, 'User/user.html', {
        "user_notifications": user_notifications,
        "global_notifications": global_notifications,
        "total_commission":total_commission,
    })

#================================order==========================
@login_required(login_url="/auth/signin/")
def orders(request):
    user_orders = Order.objects.filter(created_by=request.user)
    return render(request, 'User/order/order_list.html', {"orders": user_orders})

@login_required(login_url="/auth/signin/")
def view_receipt(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    return render(request, 'User/order/receipt.html', {"order": order})
 
 

 
@login_required
def create_order(request):
    packages = Order.objects.all()
    new_labels = NewLabel.objects.all()
    batches = Batch.objects.all()   

    if request.method == "POST":
        batch_id = request.POST.get('batch_id')  
        name = request.POST.get('name')
        order_type = request.POST.get('type')
        weight = request.POST.get('weight')
        cost = request.POST.get('cost')
        new_label_id = request.POST.get('new_label_id')
        status = request.POST.get('status')  

        if request.user.is_authenticated:
            user = request.user  
            new_label_instance = get_object_or_404(NewLabel, id=new_label_id)
            batch_instance = get_object_or_404(Batch, id=batch_id)

            tracking_no = str(uuid.uuid4()).replace("-", "").upper()[:12]

            new_order = Order(
                new_label=new_label_instance,
                tracking_number=tracking_no,
                batch_number=batch_instance,  
                name=name,
                type=order_type,
                weight=weight,
                cost=cost,
                status=status,  
                created_by=user
            )
            new_order.save()
 
            notification_create(user, f"New order created: {tracking_no}", color="Black")

            return redirect('/orders')

    return render(request, "User/order/create_order.html", {'new_label': new_labels, 'batches': batches})

@login_required(login_url="/auth/signin/")
def addFund(request):
    return render(request, 'User/addFunds.html')

@login_required(login_url="/auth/signin/")
def address(request):
    address = Address.objects.filter(user=request.user)
    return render(request,'User/fromAddresses.html', {'address':address})

@login_required(login_url="/auth/signin/")
def payment(request):
    return render(request,'User/Payments.html')

@login_required(login_url="/auth/signin/")
def referral(request):
    return render(request,'User/Referrals.html')
def package(request):
    search_query = request.GET.get('search', '')  
    packages = Package.objects.all()
    if search_query:
        packages = packages.filter(name__icontains=search_query)  
    return render(request, 'User/savedPackages.html', {'packages': packages})

def handle_uploaded_file(request):
    if request.method == 'POST' and request.FILES.get('csv_file'):
        csv_file = request.FILES['csv_file']
        fs = FileSystemStorage()
        file_path = fs.save(csv_file.name, csv_file)

        start_time = time.time()
        try:
            with open(fs.path(file_path), mode='r') as file:
                reader = csv.DictReader(file)
                bulk_create_list = []
                for row in reader:
                    weight = float(row.get('Weight', 0))
                    length = float(row.get('Length', 0))
                    width = float(row.get('Width', 0))
                    height = float(row.get('Height', 0))
                    rate = float(row.get('Rate', 0))
                    shipping_class = row.get('Shipping Class', 'Unknown')

                    bulk_create_list.append(CompetitorRate(
                        weight=weight, length=length, width=width,
                        height=height, rate=rate, shipping_class=shipping_class
                    ))
                CompetitorRate.objects.bulk_create(bulk_create_list)

            return render(request, 'Admin/upload.html', {
                'success_message': f"Successfully uploaded {len(bulk_create_list)} rows."
            })
        except Exception as e:
            return HttpResponse(f"Error processing CSV: {e}", status=500)
    return render(request, 'Admin/upload.html')
 
@login_required
def create_package(request):
    if request.method == "POST":
        user = request.user
        try:
            name = request.POST.get('name', '').strip()
            weight = Decimal(request.POST.get('weight', 0))  
            length = Decimal(request.POST.get('length', 0))  
            width = Decimal(request.POST.get('width', 0))    
            height = Decimal(request.POST.get('height', 0))  
            dynamic_pricing_enabled = request.POST.get('dynamic_pricing_enabled', 'off') == 'on'
            shipping_class = request.POST.get('shipping_class', 'Standard')
            
            discount_percentage_obj = ShippingClassDiscount.objects.filter(shipping_class=shipping_class).first()
            discount_percentage = discount_percentage_obj.discount_percentage if discount_percentage_obj else 20

            new_package = Package(
                user=request.user, name=name, weight=weight, length=length,
                width=width, height=height, dynamic_pricing_enabled=dynamic_pricing_enabled,
                discount=discount_percentage, shipping_class=shipping_class
            )

            if dynamic_pricing_enabled:
                competitor_rate = new_package.get_competitor_rate()
                
                if competitor_rate:
                    print(f"Competitor Rate Found: {competitor_rate.rate} for {competitor_rate.length}x{competitor_rate.width}x{competitor_rate.height}")
                else:
                    print("No exact competitor rate found. Using estimated base pricing.")

                new_package.calculate_discounted_price()

            new_package.save()
            notification_create(
                user, 
                message=f"New Package '{new_package.name}' has been Added In list.", 
                color="Black"
            )
            return redirect('/packages_admin')
        

        except Exception as e:
            print(f"Error in create_package: {str(e)}")
            return render(request, "Admin/Packages.html", {
                "error": str(e), "packages": Package.objects.filter(user=request.user),
            })

    return render(request, "Admin/Packages.html", {"packages": Package.objects.filter(user=request.user)})


@login_required(login_url="/auth/signin/")
def setting(request):
    return render(request,'User/settings.html')


User = get_user_model()

def update_profile(request):
    user = request.user 
    if request.method == 'POST':
        first_name = request.POST.get('first_name', user.first_name)
        email = request.POST.get('email', user.email)
        timezone_str = request.POST.get('timezone', 'UTC')  
        is_2fa_enabled = request.POST.get('is_2fa_enabled') == 'True'  

        if not first_name:
            messages.error(request, "First Name is required.")
            return redirect('/settings/')

        user.first_name = first_name
        user.email = email
        user.timezone = timezone_str
        user.is_2fa_enabled = is_2fa_enabled  

        try:
            user.save() 
            
            # ✅ Fix the notification message
            status = "enabled" if is_2fa_enabled else "disabled"
            notification_create(
                user, 
                message=f"'{first_name}' has {status} 2FA.", 
                color="Black"
            ) 
            
            messages.success(request, "Profile updated successfully.")
        except Exception as e:
            messages.error(request, f"An error occurred: {e}")

        return redirect('/settings/')  

    else:
        try:
            if user.timezone:
                user_timezone = pytz.timezone(user.timezone)  
                current_time = now().astimezone(user_timezone)  
            else:
                current_time = now()  
        except pytz.UnknownTimeZoneError:
            current_time = now()  
        
        return render(request, 'profile.html', {'user': user, 'current_time': current_time})


@login_required(login_url="/auth/signin/")
def store(request):
    store = Store.objects.filter(user=request.user)
    return render(request,'User/stores.html', {'store':store})

@login_required(login_url="/auth/signin/")
def supports(request):
    support = Ticket.objects.filter(user=request.user)
    return render(request,'User/support.html', {'support': support})

@csrf_exempt
def close_ticket(request, ticket_id):
    if request.method == "POST":
        ticket = get_object_or_404(Ticket, id=ticket_id)
        ticket.status = "Closed"
        ticket.save()

        return JsonResponse({"message": "Ticket closed successfully", "ticket_id": ticket.id})
    else:
        return JsonResponse({"error": "Invalid request method"}, status=405)

@login_required(login_url="/auth/signin/")
def view_tickets_user(request, id):
    tickets= Ticket.objects.get(id=id)
    return render(request,'User/view_tickets.html',{"tickets":tickets})


 
def submit_view_tickets_user(request):
    if request.method == 'POST':
        user = request.user 
        try:
            ticket_id = request.POST['id']
            new_message = request.POST['description']

            ticket = get_object_or_404(Ticket, id=ticket_id)
 
            if ticket.message:
                ticket.message += f"\nUser: {new_message}"
            else:
                ticket.message = f"User: {new_message}"
            ticket.save()
            notification_create(
                user, 
                message=f"Your ticket '{ticket.title}' message sent successfully!.", 
                color="Black"
            )
            send_ticket_update_email(ticket.user.email, ticket.user.username, ticket.title, new_message, ticket.status, "User")

            return JsonResponse({"status": "success", "message": "Reply sent successfully!"})

        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)}, status=400)

def newLable(request):
    package= Package.objects.all()
   
    return render(request,'User/newLable.html',{"packages":package})
 
@login_required(login_url="/auth/signin/")
def contact(request):
    return render(request,'contact.html')

@login_required
def delete_account(request):
    user = request.user
    if request.method == 'GET':
        notification_create(user, f"User '{user.username}' has deleted their account.", color="Red")

       

        user.delete()  
        messages.success(request, "Your account has been permanently deleted.")
        return redirect('/')  
    else:
        messages.error(request, "Invalid request method.")
        return redirect('/settings/')  

def load_navbar(request):
    if request.user.is_staff: 
        return render(request, "navbarAdmin.html")
    else:
        return render(request, "navbar.html")

def load_sidebar(request):
    if request.user.is_staff: 
        return render(request, "sidebarAdmin.html")
    else:
        return render(request, "sidebar.html")
def orders_admin(request):
    order = Order.objects.all()
    return render(request, 'Admin/order.html',{"orderss": order})
@login_required(login_url="/auth/signin/")
def view_receipt_admin(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    return render(request, 'Admin/receipt.html', {"order": order})



def generate_pdf(request, order_id):
    try:
        order = Order.objects.get(id=order_id)

        user_name = request.user.username if request.user.is_authenticated else "Guest"

        context = {
    'order': order,
    'user_name': user_name,  
    'company_logo': request.build_absolute_uri(settings.MEDIA_URL + 'images/logo1.png'),
    'company_name': 'Pirate Ship',
    'ship_from_address': order.new_label.ship_from.address,
    'ship_from_city': order.new_label.ship_from.city,
    'ship_from_state': order.new_label.ship_from.state,
    'ship_from_zip_code': order.new_label.ship_from.zip_code
}


        template = get_template('User/order/receipt_template.html')
        html = template.render(context)

        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="order_{order.id}_receipt.pdf"'

        pisa_status = pisa.CreatePDF(html, dest=response)

        if pisa_status.err:
            return HttpResponse('We had an error generating your PDF', status=500)

        return response

    except Exception as e:
        return HttpResponse(f'Internal Server Error: {str(e)}', status=500)

#===========================Globel notification==============================
 
 
def is_admin(user):
    return user.is_superuser

@login_required
@user_passes_test(is_admin)
def create_notification(request):
    if request.method == "POST":
        message = request.POST.get("message")
        user_id = request.POST.get("user_id") or None
        is_global = request.POST.get("is_global") == "on"
        color = request.POST.get("color", "black")  
        created_by = request.user   
        if is_global:
            Notification.objects.create(
                message=message,
                is_global=True,  
                user=None,  
                created_by=created_by,
                color=color
            )
        else:
            user = CustomUser.objects.get(id=user_id)
            Notification.objects.create(
                message=message,
                user=user,
                is_global=False,   
                created_by=created_by,
                color=color
            )

        messages.success(request, "Notification created successfully!")
        return redirect("create_notification")

    users = CustomUser.objects.all()
    return render(request, "Admin/create_notification.html", {"users": users})
