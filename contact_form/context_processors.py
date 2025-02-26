from adminside.models import Notification

def notification_context(request):
    if request.user.is_authenticated:
        if request.user.is_superuser:
           
            all_notifications = Notification.objects.all().order_by("-created_at")
        else:
          
            user_notifications = Notification.objects.filter(user=request.user, is_read=False)
            global_notifications = Notification.objects.filter(is_global=True, is_read=False)
            admin_created_notifications = Notification.objects.filter(created_by__is_superuser=True, is_read=False)
 
            all_notifications = (user_notifications | global_notifications | admin_created_notifications).order_by("-created_at")

        unread_count = all_notifications.count()  
        notifications = all_notifications  
    else:
        notifications = []
        unread_count = 0

    return {"notifications": notifications, "unread_count": unread_count}
