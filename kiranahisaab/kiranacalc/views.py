from django.shortcuts import render
from django.shortcuts import get_object_or_404, redirect
from django.http import HttpResponse
from .models import calc

# Create your views here.
def kirana(request):
    return render(request, 'base.html')

def contact(request):
    return render(request, 'contact.html')

def all(request):
    # Fix any records with missing slugs
    records_without_slug = calc.objects.filter(slug='')
    for record in records_without_slug:
        record.save()  # This will trigger slug generation
    
    # Get all records
    data = calc.objects.all().order_by('-created_at')
    
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

def detail(request, slug):
    item = get_object_or_404(calc, slug=slug)
    return render(request, "detail.html", {"item": item})


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

def delete_receipt(request, slug):
    if request.method == 'POST':
        item = get_object_or_404(calc, slug=slug)
        item.delete()
    return redirect('all')
