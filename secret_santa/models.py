from django.db import models
from django.contrib.auth.models import User


class Group(models.Model):
    name = models.CharField(max_length=255, unique=True)  # Ensuring group name is unique
    admin = models.ForeignKey(User, on_delete=models.CASCADE, related_name='admin_groups')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Group'
        verbose_name_plural = 'Groups'


class Member(models.Model):
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE, related_name='memberships')
    name = models.CharField(max_length=255)
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name='members')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Member'
        verbose_name_plural = 'Members'


class SecretSantaAssignment(models.Model):
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    giver = models.ForeignKey(User, related_name='giver_assignments', on_delete=models.CASCADE)
    receiver = models.ForeignKey(User, related_name='receiver_assignments', on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Secret Santa Assignment'
        verbose_name_plural = 'Secret Santa Assignments'


class GroupJoinRequest(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    status = models.CharField(max_length=10, choices=(('PENDING', 'Pending'), ('ACCEPTED', 'Accepted'), ('REJECTED', 'Rejected')), default='PENDING')
    timestamp = models.DateTimeField(auto_now_add=True)  # Automatically set the timestamp when a record is created

    def __str__(self):
        return f"{self.user.username} wants to join {self.group.name}"

