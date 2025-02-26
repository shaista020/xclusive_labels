from django.shortcuts import render,get_object_or_404, redirect
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import *
from contact_form.models import Ticket
from django.http import JsonResponse
from .serializers import *
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import AdminUser
from .serializers import AdminUserSerializer
from django.contrib.auth.decorators import login_required
from datetime import date
from contact_form.models import *
from decimal import Decimal
from contact_form.send_mail import send_ticket_update_email  
from contact_form.notification import notification_create  
 


class CronsView(APIView):
    def get(self, request, pk=None):
        if pk:
            type_instance = get_object_or_404(Cron, pk=pk)
            serializer = CronSerializer(type_instance)
            return Response(serializer.data)
        else:
            types = Cron.objects.all()
            serializer = CronSerializer(types, many=True)
            return Response(serializer.data)

    def post(self, request):
        serializer = CronSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    def put(self, request, pk):
        cron = get_object_or_404(Cron, pk=pk)
        serializer = CronSerializer(cron, data=request.data, partial=True)  
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        cron = get_object_or_404(Cron, pk=pk)
        cron.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class TypeView(APIView):
    def get(self, request, pk=None):
        if pk:
          
            type_instance = get_object_or_404(Type, pk=pk)
            serializer = TypeSerializer(type_instance)
            return Response(serializer.data)
        else:
         
            types = Type.objects.all()
            serializer = TypeSerializer(types, many=True)
            return Response(serializer.data)

    def post(self, request):
        serializer = TypeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk):
        type_instance = get_object_or_404(Type, pk=pk)
        serializer = TypeSerializer(type_instance, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        type_instance = get_object_or_404(Type, pk=pk)
        type_instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class PaymentView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, pk=None):
        if pk:
            payment = get_object_or_404(Payment, pk=pk)
            serializer = PaymentSerializer(payment)
            return Response(serializer.data)
        else:
            payments = Payment.objects.all()
            serializer = PaymentSerializer(payments, many=True)
            return Response(serializer.data)

    def post(self, request):
        serializer = PaymentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk):
        payment = get_object_or_404(Payment, pk=pk)
        action = request.data.get('action') 
        if action == "accept":
            payment.status = "Accepted"  
            payment.save()
            return Response({"message": "Payment accepted."}, status=status.HTTP_200_OK)

        elif action == "reject":
            payment.status = "Rejected"  
            payment.save()
            return Response({"message": "Payment rejected."}, status=status.HTTP_200_OK)

        else:
            return Response({"error": "Invalid action. Use 'accept' or 'reject'."}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        payment = get_object_or_404(Payment, pk=pk)
        payment.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class RefundView(APIView):

    def get(self, request):
       refund= Refund.objects.all()
       serializer = RefundSerializer(refund, many=True)
       return Response(serializer.data)


    def post(self, request):
        serializer = RefundSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class payment_config_View(APIView):

    def get(self, request):
       paymentConfig= PaymentConfig.objects.all()
       serializer = PaymentConfigSerializer(paymentConfig, many=True)
       return Response(serializer.data)


    def post(self, request):
        serializer = PaymentConfigSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class email_config_View(APIView):

    def get(self, request):
       email_config= EmailConfig.objects.all()
       serializer = EmailConfigSerializer(email_config, many=True)
       return Response(serializer.data)


    def post(self, request):
        serializer = EmailConfigSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


 
class Userview(APIView):
   
    def get(self, request, pk=None):
       
        if pk:
            user = get_object_or_404(AdminUser, pk=pk)  
            serializer = AdminUserSerializer(user)
            return Response(serializer.data)
        else:
            users = AdminUser.objects.all() 
            serializer = AdminUserSerializer(users, many=True)
            return Response(serializer.data)

    def post(self, request):
      
        serializer = AdminUserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save() 
            
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk=None):
       
        user = get_object_or_404(AdminUser, pk=pk)  
        serializer = AdminUserSerializer(user, data=request.data, partial=False) 
        if serializer.is_valid():
            serializer.save() 
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk=None):
       
        user = get_object_or_404(AdminUser, pk=pk) 
        user.delete() 
        return Response(status=status.HTTP_204_NO_CONTENT)  

class Weightview(APIView):
    def get(self, request, pk=None):
        if pk:
           
            weight_instance = get_object_or_404(Weight, pk=pk)
            serializer = WeightSerializer(weight_instance)
            return Response(serializer.data)
        else:
          
            weights = Weight.objects.all()
            serializer = WeightSerializer(weights, many=True)
            return Response(serializer.data)

    def post(self, request):
        serializer = WeightSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk):
        weight_instance = get_object_or_404(Weight, pk=pk)
        serializer = WeightSerializer(weight_instance, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        weight_instance = get_object_or_404(Weight, pk=pk)
        weight_instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

 


   
@login_required(login_url="/auth/signin/")
def dashboard(request):
    total_users = CustomUser.objects.all().count()
    today_date = date.today() 
    today_registered = CustomUser.objects.filter(date_joined__date =today_date).count()
    open_tickets_count = Ticket.objects.filter(status="Open").count()
    return render(request, 'Admin/Admin.html',{"total_users": total_users, "today_registered": today_registered,  'open_tickets': open_tickets_count,})

 
@login_required(login_url="/auth/signin/")
def batch(request):
    batches = Batch.objects.all()   
    return render(request, 'Admin/Abatches.html', {'batches': batches})

@login_required(login_url="/auth/signin/")
def cron(request):
    return render(request,'Admin/ACrons.html')

@login_required(login_url="/auth/signin/")
def pay(request):
    return render(request,'Admin/APayments.html')

@login_required(login_url="/auth/signin/")
def refund(request):
    return render(request,'Admin/ARefunds.html')

@login_required(login_url="/auth/signin/")
def ticket(request):
    tickets= Ticket.objects.all()
    return render(request,'Admin/ATickets.html',{"tickets":tickets})

@login_required(login_url="/auth/signin/")
def view_ticket(request, id):
    tickets= Ticket.objects.get(id=id)
    return render(request,'Admin/view_tickets.html',{"tickets":tickets})

 
from django.utils import timezone
   
  
def submit_view_tickets(request):
    if request.method == 'POST':
        user = request.user  
        try:
            ticket_id = request.POST['id']
            new_message = request.POST['description']
            status = request.POST['status']

            ticket = get_object_or_404(Ticket, id=ticket_id)
 
            sender_label = "[admin]" if user.is_superuser else "[User]"
            timestamp = timezone.now().strftime('%Y-%m-%d %H:%M')
 
            messages_to_add = []
 
            if ticket.status != status: 
                status_message = f"[{timestamp}] {sender_label} {user.username}: changed the ticket status to '{status}'."
                messages_to_add.append(status_message)
 
            if new_message.strip():
                formatted_message = f"[{timestamp}] {sender_label} {user.username}: {new_message}"
                messages_to_add.append(formatted_message)
 
                Message.objects.create(ticket=ticket, sender=user.username, text=new_message)
 
            if messages_to_add:
                ticket.message += "\n" + "\n".join(messages_to_add) if ticket.message else "\n".join(messages_to_add)
 
            ticket.status = status
            ticket.save()
 
            if status.lower() == "closed":
                notification_message = f"Your ticket '{ticket.title}' has been closed by {user.username}."
            elif status.lower() == "in progress":
                notification_message = f"Your ticket '{ticket.title}' is now in progress. {user.username} is working on it."
            elif status.lower() == "open":
                notification_message = f"Your ticket '{ticket.title}' has been reopened by {user.username}."
            else:
                notification_message = f"Your ticket '{ticket.title}' has been updated by {user.username} with a new reply."

            
            notification_create(
                ticket.user,  
                message=notification_message,
                color="Black"
            )

            
            send_ticket_update_email(ticket.user.email, ticket.user.username, ticket.title, new_message, status, user.username)

            return JsonResponse({"status": "success", "message": "Reply and status update sent successfully!"})

        except Exception as e:
            return JsonResponse({"status": "error", "message": f"Error: {str(e)}"}, status=400)


@login_required(login_url="/auth/signin/")
def setting(request):
    return render(request,'Admin/ASettings.html')

@login_required(login_url="/auth/signin/")
def type(request):
    types = Type.objects.all()
    return render(request,'Admin/ATypes.html', {'types': types})



@login_required(login_url="/auth/signin/")
def user(request):
    
    users = CustomUser.objects.all()
    
    return render(request, 'Admin/AUsers.html', {'users': users})

@login_required(login_url="/auth/signin/")
def get_user_details(request):
    if request.method == "GET":
        user_id = request.GET.get("user_id")
        try:
            user = CustomUser.objects.get(id=user_id)
            user_data = {
                "full_name": user.username,  
                "email": user.email,
                "verified_status": user.verified_status,   
                "current_balance": user.current_balance,
                "total_spent": user.total_spent,
                "date_joined": user.date_joined.strftime("%Y-%m-%d"),
            }
            return JsonResponse({"success": True, "user": user_data})
        except CustomUser.DoesNotExist:
            return JsonResponse({"success": False, "error": "User not found"})
    return JsonResponse({"success": False, "error": "Invalid request"})

@login_required(login_url="/auth/signin/")
def weight(request):
    weights = Weight.objects.all()
    return render(request, 'Admin/AWeights.html', {'weights': weights})
@login_required(login_url="/auth/signin/")
def newlable(request):
    return render(request,'Admin/newLable.html')

@login_required(login_url="/auth/signin/")
def addFunds(request):
    return render(request,'Admin/addFunds.html')

# @login_required(login_url="/auth/signin/")
def home(request):
    return render(request,'home.html')

@login_required(login_url="/auth/signin/")
def signin(request):
    return render(request,'signin.html')
@login_required(login_url="/auth/signin/")
def packages_admin(request):
    packages = Package.objects.filter(user=request.user)
    return render(request,'Admin/Packages.html', {'packages':packages})

def update_discount(request):
    if request.method == "POST":
        package_id = request.POST.get('package_id')
        discount = request.POST.get('discount')

        try:
            package = get_object_or_404(Package, id=package_id, user=request.user)

            package.discount = Decimal(discount)
            length = Decimal(str(package.length))
            width = Decimal(str(package.width))
            height = Decimal(str(package.height))

            base_price = length * width * height
            discount_amount = base_price * (package.discount / Decimal(100))
            package.total_cost = base_price - discount_amount

            package.save()
            return redirect('/packages_admin')

        except ValueError:
            return redirect('/packages_admin')

    return redirect('/packages_admin')

 
 
def edit_package(request, package_id):
    
    package = get_object_or_404(Package, pk=package_id)
 
    if request.method == "POST":
        weight = Decimal(request.POST.get('weight', 0))
        length = Decimal(request.POST.get('length', 0))
        width = Decimal(request.POST.get('width', 0))
        height = Decimal(request.POST.get('height', 0))
        dynamic_pricing_enabled = request.POST.get('dynamic_pricing_enabled', 'off') == 'on'
        discount_percentage = Decimal(request.POST.get('discount', 20))  
        original_price = Decimal(request.POST.get('original_price', 0))   
        if dynamic_pricing_enabled:
           
            original_price = weight * Decimal(2)  
            discounted_price = original_price * (Decimal(1) - (discount_percentage / Decimal(100)))
            discount_amount = original_price - discounted_price
            total_cost = discounted_price
        else:
            
            discounted_price = original_price * (Decimal(1) - (discount_percentage / Decimal(100)))
            discount_amount = original_price - discounted_price
            total_cost = discounted_price
 
        package.weight = weight
        package.length = length
        package.width = width
        package.height = height
        package.discount = discount_percentage
        package.dynamic_pricing_enabled = dynamic_pricing_enabled
        package.original_price = original_price
        package.discounted_price = discounted_price
        package.discount_amount = discount_amount
        package.total_cost = total_cost
        package.save()
 
        return redirect('package_detail', package_id=package.id)
 
    return render(request, 'Admin/edit_package.html', {
        'package': package
    })


@login_required
def update_global_discount(request):
    if request.method == "POST":
        discount = Decimal(request.POST.get('discount')) 
        packages = Package.objects.filter(user=request.user)

        for package in packages:
            package.discount = discount
            
            volume = Decimal(package.length) * Decimal(package.width) * Decimal(package.height)
            
            package.total_cost = volume - (volume * discount / Decimal(100))
            
            package.save()
        
        return redirect('/packages_admin')

    return render(request, 'Admin/packages.html')
