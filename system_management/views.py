import json
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import  authenticate,login, logout
from django.contrib.auth.hashers import make_password
from django.utils.crypto import get_random_string
from .models import User
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from system_management.models import Profile, Province, UserType
from system_management.constants import CREATOR

def home_page(request):
   context = {
        'title': 'Welcome to Sino\'s Blog',
        'content': 'Share your thoughts, create new posts, and comment on others!',
    }
   return render(request, 'index.html', context)

def login_view(request):
    if request.user.is_authenticated:
        return redirect('BLOG/blog')
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        # Authenticate the user
        user = authenticate(request, username=email, password=password)

        # Check if the user exists and is valid
        if user is not None:
            login(request, user)  # Log the user in
            return JsonResponse({'success': True})  # Send success JSON response
        else:
            return JsonResponse({'success': False, 'message': 'Invalid email or password'})  # Send error JSON response
    
    # If not a POST request, redirect to login page
    return render(request, 'login.html')

def logout_view(request):
    logout(request)
    print('User logged out')
    return redirect('login')

def register_view(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        # Password mismatch error
        if password != confirm_password:
            return JsonResponse({"error": "Passwords do not match."}, status=400)

        # Email already registered error
        if User.objects.filter(email=email).exists():
            return JsonResponse({"error": "Email is already registered."}, status=400)
        user_type = UserType.objects.get(name= CREATOR)
        user_type_id = user_type.id
        # Creating the user
        User.objects.create_user(
            first_name=first_name,
            last_name=last_name,
            email=email,
            password=password,
            user_type_id = user_type_id
        )

        # Return success message as JSON
        return JsonResponse({"success": "Registration successful! Please login."}, status=200)

    # If the request is not POST, return JSON error (or handle it differently)
    if request.method == 'GET':
         return render(request, 'register.html')
     


@login_required
def profile_view(request):
    user = request.user
    provinces = Province.objects.all()  # Fetch all provinces

    try:
        profile = user.profile
    except Profile.DoesNotExist:
        profile = None  # Handle the case where the profile does not exist

    context = {
        'profile': profile,  # Pass the user's profile data
        'provinces': provinces,  # Pass all provinces for the dropdown
        'user': user
    }
    return render(request, 'profile.html', context)


@login_required

def add_user(request):
    try:
        # Extracting fields from request data
        user_type_id = request.POST.get('user_type_id')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        id_number = request.POST.get('id_number')
        phone_number = request.POST.get('phone_number')
        email = request.POST.get('email')
        
        # Check if email is already registered
        if User.objects.filter(email=email).exists():
            return JsonResponse({'success': False, 'error': 'Email already registered'}, status=400)
       
        # Generate a random password
        password = get_random_string(length=8)
        print('password',password)
        
        # Check if the user_type exists
        try:
            user_type = UserType.objects.get(id=user_type_id)
        except UserType.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Invalid user type'}, status=400)

        # Create user
        user = User.objects.create(
            email=email,
            first_name=first_name,
            last_name=last_name,
            password=make_password(password),
            user_type_id = user_type_id
        )
        
        # Assign user type if applicable
        
        user.save()
        print('user',user)
        # Create or update the user's profile with additional info
        Profile.objects.create(
            user=user,
            phone_number=phone_number,
            id_number=id_number
        )

        # Return success response
        return JsonResponse({
            'success': True,
            'message':'user added sucessfully',
            'user': {
                'id': user.id,
                'email': user.email,
                'phone_number': phone_number,
                'role': user_type.name,
                'password': password 
            }
        }, status=201)
    
    except json.JSONDecodeError:
        return JsonResponse({'success': False, 'error': 'Invalid data format'}, status=400)
    
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=500)



@login_required
def view_users(request):
    users = User.objects.all()  # Fetch all provinces

    context = {
        'users': users
    }
    return render(request, 'users.html', context)

@login_required
def delete_user(request, user_id):
    """
        Admin view to delete a user from the system.

        This view is accessible to logged-in administrators.
        It retrieves the user by their 'user_id',
        deletes the user from the system,
        and redirects to the 'manage_users' page.

        Parameters:
        - request (HttpRequest): The HTTP request object.
        - user_id (int): The ID of the user to be deleted.

        Returns:
        - HttpResponseRedirect: Redirects to the 'manage_users' page after deleting the user.

        Raises:
        - Http404: If the specified user does not exist.
    """

    user = get_object_or_404(User, id=user_id)
    user.delete()

    return redirect('view_users')

def update_profile(request):
    if request.method == 'POST':
        user_id = request.user.id
        
        # Retrieve form data
        phone_number = request.POST.get('phone_number')
        suburb = request.POST.get('suburb')
        street_address = request.POST.get('street_address')
        city = request.POST.get('city')
        postal_code = request.POST.get('postal_code')
        province = request.POST.get('province')  
        id_type = request.POST.get('id_type')  

        # Handle ID or Passport based on selection
        id_number = request.POST.get('id_number') if id_type == 'id' else None
        passport_number = request.POST.get('passport_number') if id_type == 'passport' else None
        
        # Update or create profile
        profile, _ = Profile.objects.update_or_create(
            user_id=user_id,
            defaults={
                'phone_number': phone_number,
                'suburb': suburb,
                'street_address': street_address,
                'city': city,
                'postal_code': postal_code,
                'province': province,
                'id_number': id_number,
                'passport_number': passport_number
            }
        )
        return redirect('profile')

    return redirect('profile')

@login_required
def change_user_status(request, user_id):
    try:

        if request.user.id == user_id:
            return JsonResponse({'success': False, 'error': 'You cannot deactivate yourself!'}, status=400)

        user = User.objects.get(id=user_id)
        user.is_active = not user.is_active
        user.save()
        
        status = 'activated' if user.is_active else 'deactivated'
        return JsonResponse({'success': True, 'status': status})
    except User.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'User does not exist'}, status=404)
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=500)


@login_required
def update_user(request, user_id):
    try:
        data = json.loads(request.body)
        user = User.objects.get(id=user_id)
        
        # Update user details
        user.first_name = data.get('first_name', user.first_name)
        user.last_name = data.get('last_name', user.last_name)
        user.email = data.get('email', user.email)
        user.save()

        # Update profile (assuming you have a Profile model)
        profile = user.profile
        profile.phone_number = data.get('phone_number', profile.phone_number)
        profile.save()

        return JsonResponse({'success': True, 'message': 'User updated successfully'})
    except User.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'User does not exist'}, status=404)
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=500)
