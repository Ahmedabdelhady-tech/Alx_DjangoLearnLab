from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Notification

class NotificationListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        notifications = Notification.objects.filter(recipient=request.user).order_by('-created_at')
        unread = notifications.filter(is_read=False)
        data = {
            "unread_count": unread.count(),
            "notifications": [
                {
                    "actor": n.actor.username,
                    "verb": n.verb,
                    "target": str(n.target),
                    "created_at": n.created_at,
                    "is_read": n.is_read,
                }
                for n in notifications
            ],
        }
        return Response(data)
