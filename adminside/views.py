from django.shortcuts import render,get_object_or_404, redirect
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import *
from contact_form.models import Ticket
from django.http import JsonResponse
from .serializers import *
from rest_framework import status
from django.contrib.auth import authenticate
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


class BatchView(APIView):
    def get(self, request, pk=None):
        if pk:
            batch = get_object_or_404(Batch, pk=pk)
            serializer = BatchSerializer(batch)
            return Response(serializer.data)
        else:
            batches = Batch.objects.all()
            serializer = BatchSerializer(batches, many=True)
            return Response(serializer.data)

    def post(self, request):
        serializer = BatchSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk):
        batch = get_object_or_404(Batch, pk=pk)
        serializer = BatchSerializer(batch, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        batch = get_object_or_404(Batch, pk=pk)
        batch.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


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


class label_api_config_view(APIView):

    def get(self, request):
       label_api_config= LabelAPIConfig.objects.all()
       serializer = LabelAPIConfigSerializer(label_api_config, many=True)
       return Response(serializer.data)


    def post(self, request):
        serializer = LabelAPIConfigSerializer(data=request.data)
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

 


class LabelView(APIView):
    def get(self, request):
        labels = newLabel.objects.all()
        serializer = newLableSerializer(labels, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = newLableSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
@login_required(login_url="/auth/signin/")
def dashboard(request):
    total_users = CustomUser.objects.all().count()
    today_date = date.today() 
    today_registered = CustomUser.objects.filter(date_joined__date =today_date).count()
    open_tickets_count = Ticket.objects.filter(status="Open").count()
    return render(request, 'Admin/Admin.html',{"total_users": total_users, "today_registered": today_registered,  'open_tickets': open_tickets_count,})

@login_required(login_url="/auth/signin/")
def batch(request):
    return render(request, 'Admin/Abatches.html')

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

def submit_view_tickets(request):
    if request.method == 'POST':
        id = request.POST['id']
        title = request.POST['title']
        date = request.POST['date']
        message = request.POST['message']
        status = request.POST["status"]

        try:
            ticket= Ticket.objects.get(id=id)
            ticket.title = title
            ticket.created_at = date
            ticket.message = message
            ticket.status  = status
            ticket.save() 
            return redirect('/tickets/')

        except:
            msg = 'error'
            return render(request,'Admin/view_tickets.html',{"msg":msg})

    

@login_required(login_url="/auth/signin/")
def setting(request):
    return render(request,'Admin/ASettings.html')

@login_required(login_url="/auth/signin/")
def type(request):
    types = Type.objects.all()
    return render(request,'Admin/ATypes.html', {'types': types})



@login_required(login_url="/auth/signin/")
def user(request):
    # Fetch all users
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
                "verified_status": user.verified_status,  # No extra check needed here
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

@login_required
def edit_package(request, package_id):
    package = get_object_or_404(Package, id=package_id, user=request.user)

    if request.method == "POST":
        try:
            package.name = request.POST.get('name').strip()
            package.weight = Decimal(str(request.POST.get('weight')))
            package.length = Decimal(str(request.POST.get('length')))
            package.width = Decimal(str(request.POST.get('width')))
            package.height = Decimal(str(request.POST.get('height')))
            package.discount = Decimal(str(request.POST.get('discount')))
            volume = package.length * package.width * package.height
            package.dynamic_pricing_enabled = 'dynamic_pricing_enabled' in request.POST

            if package.dynamic_pricing_enabled:
                discount_amount = (volume * package.discount) / Decimal(100)
                package.total_cost = volume - discount_amount  
            else:
                package.total_cost = volume

            package.save()
            return redirect('/packages_admin')

        except Exception as e:
            print(f"Error: {e}")  
            return render(request, 'Admin/edit_package.html', {'package': package, 'error': "Invalid input."})

    return render(request, 'Admin/edit_package.html', {'package': package})


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
