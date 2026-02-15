from django.shortcuts import render
from django.shortcuts import get_object_or_404, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.models import User
from django.contrib import messages
from .models import calc

# Authentication Views
def login_view(request):
    if request.user.is_authenticated:
        return redirect('kirana')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth_login(request, user)
            messages.success(request, f'Welcome back, {user.username}!')
            return redirect('kirana')
        else:
            messages.error(request, 'Invalid username or password.')
    
    return render(request, 'login.html')

def register_view(request):
    if request.user.is_authenticated:
        return redirect('kirana')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')
        
        errors = []
        
        if not username or not password or not password2:
            errors.append('All fields are required.')
        
        if password != password2:
            errors.append('Passwords do not match.')
        
        if len(password) < 6:
            errors.append('Password must be at least 6 characters long.')
        
        if User.objects.filter(username=username).exists():
            errors.append('Username already exists.')
        
        if email and User.objects.filter(email=email).exists():
            errors.append('Email already registered.')
        
        if not errors:
            user = User.objects.create_user(username=username, email=email, password=password)
            auth_login(request, user)
            messages.success(request, f'Account created successfully! Welcome, {username}!')
            return redirect('kirana')
        else:
            for error in errors:
                messages.error(request, error)
    
    return render(request, 'register.html')

def logout_view(request):
    auth_logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect('login')

# Main Views
@login_required(login_url='login')
def kirana(request):
    return render(request, 'base.html')

def contact(request):
    return render(request, 'contact.html')

@login_required(login_url='login')
def all(request):
    # Fix any records with missing slugs for current user
    records_without_slug = calc.objects.filter(user=request.user, slug='')
    for record in records_without_slug:
        record.save()  # This will trigger slug generation
    
    # Get all records for current user only
    data = calc.objects.filter(user=request.user).order_by('-created_at')
    
    # Search functionality
    search_query = request.GET.get('search', '')
    if search_query:
        data = data.filter(name__icontains=search_query)
    
    # Date filter functionality
    from_date = request.GET.get('from_date', '')
    to_date = request.GET.get('to_date', '')
    
    if from_date:
        data = data.filter(created_at__date__gte=from_date)
    if to_date:
        data = data.filter(created_at__date__lte=to_date)
    
    context = {
        'data': data,
        'search_query': search_query,
        'from_date': from_date,
        'to_date': to_date,
    }
    
    return render(request, 'all.html', context)

@login_required(login_url='login')
def detail(request, slug):
    item = get_object_or_404(calc, slug=slug, user=request.user)
    return render(request, "detail.html", {"item": item})


@login_required(login_url='login')
def add_data(request):
    receipt_data = None
    errors = []
    form_data = {
        "name": "",
    }

    if request.method == "POST":
        name = request.POST.get("name")
        product_names = request.POST.getlist("product_name[]")
        product_prices = request.POST.getlist("product_price[]")

        form_data["name"] = name or ""

        if not name:
            errors.append("Please enter a customer name.")

        if not product_names or not product_prices:
            errors.append("Please add at least one product.")
        elif len(product_names) != len(product_prices):
            errors.append("Product names and prices count mismatch.")

        product_list = []
        price_list = []
        
        for i in range(len(product_names)):
            product_name = product_names[i].strip() if i < len(product_names) else ""
            price_str = product_prices[i].strip() if i < len(product_prices) else ""
            
            if not product_name:
                errors.append(f"Product name cannot be empty (Item #{i+1})")
                continue
            
            if not price_str:
                errors.append(f"Price cannot be empty for {product_name}")
                continue
            
            try:
                price = int(price_str)
                if price < 0:
                    errors.append(f"Price cannot be negative for {product_name}")
                    continue
                product_list.append(f"{product_name} : ₹{price}")
                price_list.append(price)
            except ValueError:
                errors.append(f"Invalid price for {product_name}: {price_str}")

        if not price_list and not errors:
            errors.append("Please enter at least one valid product.")

        if not errors:
            total = sum(price_list)

            calc.objects.create(
                user=request.user,
                name=name,
                amount=total,
                items=", ".join(product_list)
            )

            receipt_data = {
                "name": name,
                "items": product_list,
                "total": total
            }

    return render(
        request,
        "base.html",
        {
            "receipt": receipt_data,
            "errors": errors,
            "form_data": form_data,
        },
    )

@login_required(login_url='login')
def delete_receipt(request, slug):
    if request.method == 'POST':
        item = get_object_or_404(calc, slug=slug, user=request.user)
        item.delete()
    return redirect('all')
# Admin Panel Views (Hidden Admin Login)
def admin_login(request):
    """Hidden admin login page - only for superusers"""
    if request.user.is_authenticated and request.user.is_superuser:
        return redirect('admin_dashboard')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)
        if user is not None:
            if user.is_superuser:
                auth_login(request, user)
                messages.success(request, f'Admin login successful!')
                return redirect('admin_dashboard')
            else:
                messages.error(request, 'Access denied. Only admin can access this page.')
        else:
            messages.error(request, 'Invalid credentials.')
    
    return render(request, 'admin_login.html')

def admin_dashboard(request):
    """Admin dashboard - shows all users and their data"""
    if not request.user.is_authenticated or not request.user.is_superuser:
        messages.error(request, 'Unauthorized access. Admin login required.')
        return redirect('admin_login')
    
    # Get all users
    users = User.objects.all()
    
    # Get summary statistics
    total_users = users.count()
    total_receipts = calc.objects.count()
    total_amount = sum(obj.amount for obj in calc.objects.all())
    
    # Pagination and search
    search_query = request.GET.get('search', '')
    if search_query:
        users = users.filter(username__icontains=search_query) | users.filter(email__icontains=search_query)
    
    context = {
        'users': users,
        'total_users': total_users,
        'total_receipts': total_receipts,
        'total_amount': total_amount,
        'search_query': search_query,
    }
    
    return render(request, 'admin_dashboard.html', context)

def admin_user_detail(request, user_id):
    """Admin view - shows all receipts and details for a specific user"""
    if not request.user.is_authenticated or not request.user.is_superuser:
        messages.error(request, 'Unauthorized access.')
        return redirect('admin_login')
    
    user = get_object_or_404(User, pk=user_id)
    receipts = calc.objects.filter(user=user).order_by('-created_at')
    
    # Calculate statistics for this user
    total_receipts = receipts.count()
    total_amount = sum(obj.amount for obj in receipts)
    avg_amount = int(total_amount / total_receipts) if total_receipts > 0 else 0
    
    context = {
        'user': user,
        'receipts': receipts,
        'total_receipts': total_receipts,
        'total_amount': total_amount,
        'avg_amount': avg_amount,
    }
    
    return render(request, 'admin_user_detail.html', context)

def admin_logout(request):
    """Admin logout"""
    auth_logout(request)
    messages.success(request, 'Admin logout successful.')
    return redirect('admin_login')