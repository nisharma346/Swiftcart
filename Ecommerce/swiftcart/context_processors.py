from .models import Announcement

def announcement(request):
    return {
        'announcement': Announcement.objects.filter(is_active=True).first()
    }
