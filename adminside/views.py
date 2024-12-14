from django.shortcuts import render,get_object_or_404, redirect
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import *
from contact_form.models import Ticket

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

class signupView(APIView):
    
    def get(self, request):
        signup = AdminUser.objects.all()
        serializer = AdminUserSerializer(signup, many=True)
        return Response(serializer.data)

    def post(self, request):
       
        serializer = AdminUserSerializer(data=request.data)

        if serializer.is_valid():
         
            user = serializer.save()

            user.is_superuser = False
            user.is_staff = False

            user.save()

            return Response({"message": "Signup successful!", "redirect_url": "/signin/"}, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class signinView(APIView):
    def post(self, request, *args, **kwargs):
        email = request.data.get('email')
        password = request.data.get('password')

        try:
           
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            user = None

        if user:
            authenticated_user = authenticate(username=user.username, password=password)
        else:
            authenticated_user = None

        print(authenticated_user)

        if authenticated_user:
            if authenticated_user.is_superuser:
                return Response({"redirect_url": "/1/"}, status=status.HTTP_200_OK)
            else:
                return Response({"redirect_url": "/user_dashboard/"}, status=status.HTTP_200_OK)
        else:
            return Response(
                {"error": "Invalid email or password"}, 
                status=status.HTTP_401_UNAUTHORIZED
            )

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


class Ticketview(APIView):

    def get(self, request):
       ticket= Ticket.objects.all()
       serializer = TicketSerializer(ticket, many=True)
       return Response(serializer.data)


    def post(self, request):
        serializer = TicketSerializer(data=request.data)
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

class Notificationview(APIView):

    def get(self, request, pk=None):
        if pk is not None:

            try:
                notification = Notification.objects.get(pk=pk)
                serializer = NotificationSerializer(notification)
                return Response(serializer.data, status=status.HTTP_200_OK)
            except Notification.DoesNotExist:
                return Response({"error": "Notification not found"}, status=status.HTTP_404_NOT_FOUND)
        else:

            notifications = Notification.objects.all()
            serializer = NotificationSerializer(notifications, many=True)
            return Response(serializer.data)

    def post(self, request):
        serializer = NotificationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk=None):
        if pk is None:
            return Response({"error": "pk is required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            notification = Notification.objects.get(pk=pk)
        except Notification.DoesNotExist:
            return Response({"error": "Notification not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = NotificationSeenSerializer(notification, data={'is_seen': True}, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    


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
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .models import CustomUser

@login_required(login_url="/auth/signin/")
def get_user_details(request):
    if request.method == "GET":
        user_id = request.GET.get("user_id")
        try:
            user = CustomUser.objects.get(id=user_id)
            user_data = {
                "full_name": user.username,  
                "email": user.email,
                "verified_status": "Yes" if user.verified_status else "No",
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

@login_required(login_url="/auth/signin/")
def home(request):
    return render(request,'home.html')

@login_required(login_url="/auth/signin/")
def signin(request):
    return render(request,'signin.html')

