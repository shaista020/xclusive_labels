from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.core.mail import send_mail
from .serializers import *
from contact_form.models import *
from django.conf import settings
from django.shortcuts import render,redirect
from rest_framework import viewsets
from django.contrib.auth.decorators import login_required
from rest_framework.decorators import action
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.contrib import messages
from django.utils.timezone import now
import pytz
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404, render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import get_user_model



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
from django.db.models import Sum
from django.db.models import Sum
from decimal import Decimal

def referrals_view(request):
    # Fetch referrals made by the logged-in user
    referrals = User.objects.filter(referred_by=request.user)

    # Calculate total commission from referrals and the user's own balance
    referral_commission = referrals.aggregate(Sum('available_for_withdraw'))['available_for_withdraw__sum'] or Decimal('0.00')
    user_own_commission = request.user.available_for_withdraw

    # Combine both to get the total commission
    total_commission = referral_commission + user_own_commission

    # Generate the referral link
    referral_link = request.build_absolute_uri(f'/auth/signup/?referral_code={request.user.referral_code}')

    context = {
        'referrals': referrals,
        'referral_commission': referral_commission,  # Commission from referrals
        'user_own_commission': user_own_commission,  # The logged-in user's own earnings
        'total_commission': total_commission,       # Combined total commission
        'referral_link': referral_link,
    }

    return render(request, "User/Referrals.html", context)


class NotificationViewSet(viewsets.ModelViewSet):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
       
        if self.request.user.is_staff:  
            return self.queryset  
        else:
            return self.queryset.filter(user=self.request.user)  
    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def get_notifications(self, request):
      
        notifications = self.get_queryset()
        unread_count = notifications.filter(is_read=False).count()
        serialized_notifications = NotificationSerializer(notifications, many=True)
        return Response({
            'username': request.user.username,  
            'unread_count': unread_count,
            'notifications': serialized_notifications.data
        })

    @action(detail=False, methods=['patch'], permission_classes=[IsAuthenticated])
    def mark_as_read(self, request):
        unread_notifications = self.queryset.filter(user=request.user, is_read=False)
        
        if unread_notifications.exists():
            unread_notifications.update(is_read=True)
            return Response({"status": "All notifications marked as read."})
        else:
            return Response({"status": "No unread notifications to mark."}, status=400)

    @action(detail=False, methods=['delete'], permission_classes=[IsAuthenticated])
    def delete_notifications(self, request):
        """Delete all read notifications."""
        deleted_notifications = self.queryset.filter(user=request.user, is_read=True)
        
        if deleted_notifications.exists():
            deleted_notifications.delete()
            return Response({"status": "All read notifications deleted."})
        else:
            return Response({"status": "No read notifications to delete."}, status=400)


class newLabelView(APIView):
    """
    Handles CRUD operations for Labels.
    Admins can see all labels; regular users can only see their own labels.
    """

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
        """
        Create a new label. Associates the label with the logged-in user.
        """
        data = request.data
        data['user'] = request.user.id 
        serializer = LabelSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk):
        """
        Update a label. Only admins or label owners can update.
        """
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
        """
        Delete a label. Only admins or label owners can delete.
        """
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
    return render(request, 'User/user.html')


@login_required(login_url="/auth/signin/")
def orders(request):
    # Filter orders based on the logged-in user
    user_orders = Order.objects.filter(created_by=request.user)
    return render(request, 'User/order.html', {"orders": user_orders})

@login_required(login_url="/auth/signin/")
def view_receipt(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    return render(request, 'User/receipt.html', {"order": order})
import uuid  
def create_order(request):
    packages = Order.objects.all()
    new_labels = NewLabel.objects.all()
    
    if request.method == "POST":
        batch_no = request.POST.get('batch_number')
        name = request.POST.get('name')
        order_type = request.POST.get('type')
        weight = request.POST.get('weight')
        cost = request.POST.get('cost')
        new_label_id = request.POST.get('new_label_id')

        if request.user.is_authenticated:
            user = request.user

            # Fetch the NewLabel instance
            new_label_instance = get_object_or_404(NewLabel, id=new_label_id)

            # Automatically generate tracking number
            tracking_no = str(uuid.uuid4()).replace("-", "").upper()[:12]  # Generate unique 12-character tracking number

            # Create the Order
            new_order = Order(
                new_label=new_label_instance,
                tracking_number=tracking_no,  # Automatically assigned
                batch_number=batch_no,
                name=name,
                type=order_type,
                weight=weight,
                cost=cost,
                created_by=user
            )
            new_order.save()

            # Redirect to the orders list
            return redirect('/orders')
    
    return render(request, "User/create_order.html", {'new_label': new_labels})

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

@login_required(login_url="/auth/signin/")
def package(request):
    packages = Package.objects.all()
    for package in packages:
        package.original_price = package.weight * package.length * package.width * package.height
    
    print("user-pkjs:" ,packages)
    return render(request,'User/savedPackages.html', {'packages':packages})


@login_required 
def create_package(request):
    if request.method == "POST":
        try:
           
            name = request.POST.get('name', '').strip()
            weight = float(request.POST.get('weight', 0))
            length = float(request.POST.get('length', 0))
            width = float(request.POST.get('width', 0))
            height = float(request.POST.get('height', 0))

            if weight <= 0 or length <= 0 or width <= 0 or height <= 0:
                raise ValueError("All dimensions and weight must be positive numbers.")

            new_package = Package(
                user=request.user,
                name=name,
                weight=weight,
                length=length,
                width=width,
                height=height,
            )
            new_package.save()

            return redirect('/packages_admin')

        except ValueError as e:
           
            return render(request, "User/savedPackages.html", {
                "error": str(e),
                "packages": Package.objects.filter(user=request.user),  
            })

    packages = Package.objects.filter(user=request.user)  
    return render(request, "User/savedPackages.html", {
        "packages": packages,
    })


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
    """
    Endpoint to mark a ticket as closed.
    """
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
        id = request.POST['id']
        title = request.POST['title']
        date = request.POST['date']
        message = request.POST['message']
        try:
            ticket = Ticket.objects.get(id=id)
            ticket.title = title
            ticket.created_at = date
            ticket.message = message
            ticket.save()

            return JsonResponse({"status": "success", "message": "Your message has been sent successfully!"})

        except Ticket.DoesNotExist:
            return JsonResponse({"status": "error", "message": "Ticket not found."}, status=400)

@login_required(login_url="/auth/signin/")
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