from adminside.models import *
def notification_create(user, message, color="Black"):
    
    Notification.objects.create(
        message=message,
        user=user,  
        created_by=user,   
        color=color,
        
    )
   