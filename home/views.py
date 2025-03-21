from django.shortcuts import render, redirect
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import PatientForm, BlogForm, AppointmentForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.admin.views.decorators import staff_member_required
from .models import *
from django.core.paginator import Paginator
from django.db.models import Q


def home(request):
    doctors = Doctor.objects.all()  # List of doctors
    blogs = Blog.objects.all().order_by('-created_at')  # Fetch blogs in descending order

    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')  # Redirect to avoid resubmitting form
        else:
            print(form.errors)
    else:
        form = AppointmentForm()

    return render(request, "home/index.html", {"blogs": blogs, 'doctors': doctors, 'form': form})


def blog_list(request):
    blogs = Blog.objects.all().order_by('-created_at')
    return render(request, 'home/blog_list.html', {'blogs': blogs})

def blog_detail(request, blog_id):
    blog = get_object_or_404(Blog, id=blog_id)
    return render(request, 'home/blog_detail.html', {'blog': blog})


@login_required
def profile(request):
    user = request.user
    patient = user.patient

    context = {
        'patient': patient,
        
    }
    return render(request, 'home/profile.html', context)

@login_required
def edit_profile(request):
    user = request.user
    patient = user.patient

    if request.method == 'POST':
        patient_form = PatientForm(request.POST, request.FILES, instance=patient)
        if patient_form.is_valid():
            patient_form.save()
            messages.success(request, 'Your profile has been updated successfully!')
            return redirect('profile')
    else:
        patient_form = PatientForm(instance=patient)

    context = {
        'patient_form': patient_form
    }
    return render(request, 'home/edit_profile.html', context)




#-------------------------Admin Site--------------------------------

def admin_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None and user.is_staff:  # Only allow staff users
            login(request, user)
            return redirect('admin_dashboard')
        else:
            messages.error(request, 'Invalid credentials or not authorized.')
    return render(request, 'accounts/admin_login.html')


@login_required
def admin_logout(request):
    logout(request)
    return redirect('admin_login')


@login_required
def admin_dashboard(request):
    total_patients = Patient.objects.count()
    appointments = Appointment.objects.all().order_by('-appointment_date')[:5]  # Fetch the 5 latest appointments


    context = {
        'total_patients': total_patients,
        'appointments': appointments
    }
    return render(request, 'admin/dashboard.html', context)


@login_required
def admin_user_list(request):
    all_users = User.objects.all()
    paginator = Paginator(all_users, 20)  # Paginate the products
    page_number = request.GET.get('page')
    users = paginator.get_page(page_number)

    if request.method=="GET":
        search= request.GET.get('search')
        if search:
            users= User.objects.filter(
                Q(username__icontains=search)|
                Q(first_name__icontains=search)|
                Q(last_name__icontains=search)|
                Q(email__icontains=search)|
                Q(date_joined__icontains=search)
                )
        else: 
            users= paginator.get_page(page_number)

    context = {
        'users': users,
    }
    return render(request, 'admin/user_list.html', context)


@login_required
def admin_user_detail(request, user_id):
    user = get_object_or_404(User, id=user_id)
    context = {
        'user': user,
    }
    return render(request, 'admin/user_detail.html', context)


@login_required
def add_blog(request):
    if request.method == "POST":
        form = BlogForm(request.POST, request.FILES)
        if form.is_valid():
            blog = form.save(commit=False)
            blog.author = request.user  # Assign logged-in admin as author
            blog.save()
            messages.success(request, "Blog added successfully!")
            return redirect("manage-blogs")  # Redirect back to dashboard
        else:
            messages.error(request, "Error adding blog. Please check the form.")
    else:
        form = BlogForm()
    
    return render(request, "admin/add_blog.html", {"form": form})



# View to manage blogs (Display all blogs with Update and Delete buttons)
@login_required
def manage_blogs(request):
    blogs = Blog.objects.all()
    return render(request, "admin/manage_blogs.html", {"blogs": blogs})

# View to update blog
@login_required
def update_blog(request, blog_id):
    blog = get_object_or_404(Blog, id=blog_id)
    if request.method == "POST":
        form = BlogForm(request.POST, request.FILES, instance=blog)
        if form.is_valid():
            form.save()
            messages.success(request, "Blog updated successfully.")
            return redirect("manage-blogs")
    else:
        form = BlogForm(instance=blog)
    
    return render(request, "admin/update_blog.html", {"form": form, "blog": blog})

# View to delete blog
@login_required
def delete_blog(request, blog_id):
    blog = get_object_or_404(Blog, id=blog_id)
    blog.delete()
    messages.success(request, "Blog deleted successfully.")
    return redirect("manage-blogs")