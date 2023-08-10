# Django core imports
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.contrib import messages

# Import models and forms related to the application
from .models import Group, Member, SecretSantaAssignment, GroupJoinRequest
from .forms import LoginForm, RegisterForm, GroupForm

# Utility imports
from .utils import secret_santa_algorithm
import random

# Import auth forms
from django.contrib.auth.forms import UserCreationForm


def login_view(request):
    """
    Handle user login.
    """
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('homepage')
        else:
            return render(request, 'login.html', {'error': 'Invalid username or password'})
    return render(request, 'login.html')


def logout_view(request):
    """
    Handle user logout.
    """
    logout(request)
    return redirect('login')


def register_view(request):
    """
    Handle user registration.
    """
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Log the user in
            login(request, user)
            return redirect('homepage')
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})


@login_required
def homepage(request):
    """
    Display the homepage with groups, assignments, and join requests.
    """
    groups = Group.objects.filter(members__user=request.user)
    assignments = SecretSantaAssignment.objects.filter(giver=request.user).select_related('receiver')

    # Get group join requests where the logged-in user is the admin
    join_requests = GroupJoinRequest.objects.filter(group__admin=request.user, status='PENDING')

    return render(request, 'homepage.html', {'groups': groups, 'assignments': assignments, 'join_requests': join_requests})

@login_required
def accept_request(request, request_id):
    """
    Accept a group join request.
    """
    join_request = get_object_or_404(GroupJoinRequest, pk=request_id)
    
    if request.user == join_request.group.admin:
        join_request.status = 'ACCEPTED'
        join_request.save()
        member = Member(user=join_request.user, name=join_request.user.username, group=join_request.group)
        member.save()
    
    return redirect('homepage')


@login_required
def reject_request(request, request_id):
    """
    Reject a group join request.
    """
    join_request = get_object_or_404(GroupJoinRequest, pk=request_id)

    if request.user == join_request.group.admin:
        join_request.status = 'REJECTED'
        join_request.save()

    return redirect('homepage')

@login_required
def create_group(request):
    """
    Handle group creation.
    """
    if request.method == 'POST':
        form = GroupForm(request.POST)
        if form.is_valid():
            group = form.save(commit=False)
            group.admin = request.user
            group.save()

            # Add the creator of the group as a member with the role of "admin"
            member = Member(user=request.user, group=group, role="admin")
            member.save()

            return redirect('homepage')
    else:
        form = GroupForm()
    return render(request, 'create_group.html', {'form': form})


@login_required
def search_groups(request):
    """
    Search for groups by name.
    """
    query = request.GET.get('query')
    if query is None:
        groups = Group.objects.none() # Return an empty queryset
    else:
        groups = Group.objects.filter(Q(name__icontains=query))
    return render(request, 'search_results.html', {'groups': groups})


@login_required
def group_detail(request, group_id):
    """
    Display group details and handle adding members.
    """
    group = get_object_or_404(Group, pk=group_id)
    members = Member.objects.filter(group=group)
    
    is_admin = request.user == group.admin # Check if the current user is the admin

    if request.method == 'POST':
        name = request.POST.get('name')
        phone_number = request.POST.get('phone_number')
        member = Member(name=name, group=group)
        member.save()
        return redirect('group_detail', group_id=group.id)

    return render(request, 'group_detail.html', {'group': group, 'members': members, 'is_admin': is_admin})


@login_required
def delete_member(request, member_id):
    """
    Delete a member from a group.
    """
    member = get_object_or_404(Member, pk=member_id)
    member.delete()
    return redirect('group_detail', group_id=member.group.id)


@login_required
def request_join_group(request, group_id):
    """
    Handle requests to join a group.
    """
    group = get_object_or_404(Group, pk=group_id)
    
    if request.method == 'POST':
        join_request, created = GroupJoinRequest.objects.get_or_create(user=request.user, group=group)
        
        if created:
            messages.success(request, "Your request to join has been sent!")
        else:
            messages.warning(request, "You have already requested to join this group.")
        
        return redirect('search_groups')  # Redirect back to search results or another appropriate page

    return redirect('homepage')


@login_required
def run_secret_santa(request, group_id):
    """
    Execute the secret santa algorithm for a group.
    """
    group = Group.objects.get(pk=group_id)

    secret_santa_algorithm(group)

    return redirect('group_detail', group_id=group_id)

