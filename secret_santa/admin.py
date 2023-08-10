from django.contrib import admin
from .models import Group, Member, GroupJoinRequest, SecretSantaAssignment
# Register your models here.
admin.site.register(Group)
admin.site.register(Member)
admin.site.register(GroupJoinRequest)
admin.site.register(SecretSantaAssignment)
