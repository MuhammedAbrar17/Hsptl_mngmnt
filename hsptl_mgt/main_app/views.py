from django.shortcuts import render,redirect,get_object_or_404
from django.views import View
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect

from django.contrib.auth import update_session_auth_hash

from django.contrib.auth import get_user_model
from .forms import CustomUserCreationForm

from .models import Doctor

# Create your views here.


def index(request):
    if request.user.is_authenticated:
        return redirect('home')
    return render(request, 'login.html') 


def log_in(request):

    if request.method == "POST":
        username = request.POST.get("username")
        pass1 = request.POST.get("pass1")

        user = authenticate(username=username, password=pass1)

        if user is not None:
            login(request, user)
            return redirect('home')

        else:
            messages.error(request, "invalid username or password")
            return redirect("log_in")

    if request.user.is_authenticated:
        return redirect('home')
    
    return render(request, 'login.html')


@login_required(login_url='log_in')
def home(request):
    return render(request,'home.html')



#create user 

User = get_user_model()

# @login_required
def create_user(request):
    # if request.user.role != 'Admin':
    #     messages.error(request, 'Only admins can create users.')
    #     return redirect('admin_dashboard')  # Replace with your appropriate redirect

    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password1'])  # Assuming password1 field in form
            user.save()
            messages.success(request, 'User created successfully!')
            return redirect(user_list)  # Replace with your user list view
    else:
        form = CustomUserCreationForm()

    return render(request,'admin/create_user.html', {'form': form})

    
def signout(request):
    logout(request)
    return HttpResponseRedirect("/")  


#list user

def user_list(request):
    users = User.objects.all()


    return render(request, 'admin/user_list.html', {'users': users})


def edit_user(request, id):
    user = get_object_or_404(User, id=id)
    
    if request.method == 'POST':
        # Get the form data
        username = request.POST.get('username')
        role = request.POST.get('role')
        current_password = request.POST.get('current_password')
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')
        
        # Check if the user entered the correct current password
        if current_password:
            if not user.check_password(current_password):
                messages.error(request, 'Current password is incorrect.')
                return redirect('edit_user', id=id)
            elif new_password != confirm_password:
                messages.error(request, 'New passwords do not match.')
                return redirect('edit_user', id=id)
            else:
                # Update the user's password
                user.set_password(new_password)
        
        # Update the user's username and role
        user.username = username
        user.role = role
        
        # Save the user instance
        user.save()
        
        # Re-authenticate the user after password change
        update_session_auth_hash(request, user)
        
        messages.success(request, 'User details updated successfully.')
        return redirect(user_list)
    
    return render(request, 'admin/edit_user.html', {'user': user})



#delet user

@login_required
def delete_user(request, user_id):
    # Get the user to be deleted or return a 404 if not found
    user_to_delete = get_object_or_404(User, id=user_id)

    # Prevent admin from deleting themselves
    if request.user == user_to_delete:
        messages.error(request, "You cannot delete your own account.")
        return redirect(user_list)

    # Delete the user and show a success message
    user_to_delete.delete()
    messages.success(request, f"User '{user_to_delete.username}' has been deleted successfully.")
    return redirect(user_list)



# admin

def admin_dashboard(request):
    return render(request,"admin/admin_dashboard.html")


# doctor





# Function to add a new doctor
def add_doctor(request):
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        specialty = request.POST['specialty']
        availability = request.POST['availability']
        
        Doctor.objects.create(
            first_name=first_name,
            last_name=last_name,
            specialty=specialty,
            availability=availability
        )
        
        messages.success(request, 'Doctor profile added successfully.')
        return redirect(admin_dashboard)
    return render(request, 'admin/add_doctor.html')


# Function to list all doctors
def doctor_list(request):
    doctors = Doctor.objects.all()  # Fetch all doctor records
    return render(request, 'admin/doctor_list.html', {'doctors': doctors})

# Function to edit doctor details
def edit_doctor(request, doctor_id):
    doctor = get_object_or_404(Doctor, id=doctor_id)
    if request.method == 'POST':
        doctor.first_name = request.POST['first_name']
        doctor.last_name = request.POST['last_name']
        doctor.specialty = request.POST['specialty']
        doctor.availability = request.POST['availability']
        doctor.save()
        messages.success(request, 'Doctor details updated successfully.')
        return redirect(doctor_list)
    return render(request, 'admin/edit_doctor.html', {'doctor': doctor})

# # Function to delete doctor profile
def delete_doctor(request, doctor_id):
    doctor = get_object_or_404(Doctor, id=doctor_id)
    if request.method == 'POST':
        doctor.delete()
        messages.success(request, 'Doctor profile deleted successfully.')
        return redirect(doctor_list)
    return redirect(doctor_list)

# Function to retrieve doctor details
# def doctor_detail(request, doctor_id):
#     doctor = get_object_or_404(Doctor, id=doctor_id)
#     return render(request, 'doctor_detail.html', {'doctor': doctor})
