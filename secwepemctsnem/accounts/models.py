from django.db import models
from django.contrib.auth.models import User
from invitation.models import *
     
class UserProfile(models.Model):
    user = models.ForeignKey(User, unique=True)
    url = models.URLField()
    home_address = models.TextField()
    phone_number = models.CharField(max_length=20)
#    public_profile_field = models.BooleanField(default=True)
    def __unicode__(self):
        return "%s's profile" % self.user
    @models.permalink
    def get_absolute_url(self):
        return ('profiles_profile_detail', [self.user.username] )
    def get_invitation_stats(self):
        try:
            return InvitationStats.objects.get(user=self.user)
        except:
            return InvitationStats.objects.none()

