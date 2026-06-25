import uuid
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from .models import Category, Product, Order, OrderItem, Review

def store_view(request):
    products = Product.objects.filter(is_active=True)
    categories = Category.objects.all()

    # Search filter
    query = request.GET.get('q')
    if query:
        products = products.filter(name__icontains=query) | products.filter(description__icontains=query)

    # Category filter
    category_slug = request.GET.get('category')
    selected_category = None
    if category_slug:
        selected_category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=selected_category)

    # Sorting
    sort_by = request.GET.get('sort_by')
    if sort_by == 'price_asc':
        products = products.order_by('price')
    elif sort_by == 'price_desc':
        products = products.order_by('-price')
    elif sort_by == 'newest':
        products = products.order_by('-created_at')
    else:
        products = products.order_by('-created_at')

    context = {
        'products': products,
        'categories': categories,
        'selected_category': selected_category,
        'query': query,
        'sort_by': sort_by,
    }
    return render(request, 'store/store.html', context)


def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug, is_active=True)
    reviews = product.reviews.all().order_by('-created_at')
    related_products = Product.objects.filter(category=product.category, is_active=True).exclude(id=product.id)[:4]

    context = {
        'product': product,
        'reviews': reviews,
        'related_products': related_products,
    }
    return render(request, 'store/detail.html', context)


@require_POST
def add_review(request, slug):
    product = get_object_or_404(Product, slug=slug, is_active=True)
    name = request.POST.get('name')
    email = request.POST.get('email')
    rating = request.POST.get('rating')
    comment = request.POST.get('comment')

    if not name or not email or not rating or not comment:
        messages.error(request, "All review fields are required.")
        return redirect('store:product_detail', slug=product.slug)

    try:
        rating = int(rating)
        if rating < 1 or rating > 5:
            raise ValueError
    except ValueError:
        messages.error(request, "Invalid rating value.")
        return redirect('store:product_detail', slug=product.slug)

    Review.objects.create(
        product=product,
        name=name,
        email=email,
        rating=rating,
        comment=comment
    )
    messages.success(request, "Thank you! Your review has been submitted.")
    return redirect('store:product_detail', slug=product.slug)


def cart_view(request):
    cart = request.session.get('cart', {})
    cart_items = []
    subtotal = 0

    for product_id, quantity in cart.items():
        try:
            product = Product.objects.get(id=product_id, is_active=True)
            total = product.price * quantity
            subtotal += total
            cart_items.append({
                'product': product,
                'quantity': quantity,
                'total': total,
            })
        except Product.DoesNotExist:
            pass

    shipping_cost = 0 if subtotal > 100 or subtotal == 0 else 10
    grand_total = subtotal + shipping_cost

    context = {
        'cart_items': cart_items,
        'subtotal': subtotal,
        'shipping_cost': shipping_cost,
        'grand_total': grand_total,
    }
    return render(request, 'store/cart.html', context)


def cart_add(request, product_id):
    product = get_object_or_404(Product, id=product_id, is_active=True)
    quantity = int(request.GET.get('quantity', 1))

    if quantity <= 0:
        messages.error(request, "Quantity must be greater than zero.")
        return redirect('store:store_view')

    cart = request.session.get('cart', {})
    current_qty = cart.get(str(product_id), 0)
    new_qty = current_qty + quantity

    # Stock validation
    if new_qty > product.stock:
        messages.warning(request, f"Sorry, only {product.stock} items of {product.name} are available.")
        cart[str(product_id)] = product.stock
    else:
        cart[str(product_id)] = new_qty
        messages.success(request, f"Added {product.name} to your cart.")

    request.session['cart'] = cart
    return redirect(request.META.get('HTTP_REFERER', 'store:cart_view'))


@require_POST
def cart_update(request):
    product_id = request.POST.get('product_id')
    quantity = request.POST.get('quantity')
    
    if not product_id or not quantity:
        return JsonResponse({'error': 'Missing parameters'}, status=400)

    try:
        product_id = int(product_id)
        quantity = int(quantity)
        product = Product.objects.get(id=product_id, is_active=True)
    except (ValueError, Product.DoesNotExist):
        return JsonResponse({'error': 'Invalid product or quantity'}, status=400)

    cart = request.session.get('cart', {})
    
    if quantity <= 0:
        if str(product_id) in cart:
            del cart[str(product_id)]
    else:
        if quantity > product.stock:
            quantity = product.stock
            messages.warning(request, f"Capped quantity at maximum available stock ({product.stock} items).")
        cart[str(product_id)] = quantity

    request.session['cart'] = cart

    # Recalculate totals
    subtotal = 0
    item_total = 0
    total_count = sum(cart.values())

    for pid, qty in cart.items():
        try:
            p = Product.objects.get(id=pid, is_active=True)
            subtotal += p.price * qty
            if int(pid) == product_id:
                item_total = p.price * qty
        except Product.DoesNotExist:
            pass

    shipping_cost = 0 if subtotal > 100 or subtotal == 0 else 10
    grand_total = subtotal + shipping_cost

    return JsonResponse({
        'success': True,
        'item_total': float(item_total),
        'subtotal': float(subtotal),
        'shipping_cost': float(shipping_cost),
        'grand_total': float(grand_total),
        'cart_count': total_count,
        'capped': quantity == product.stock and quantity > 0
    })


def cart_remove(request, product_id):
    cart = request.session.get('cart', {})
    
    if str(product_id) in cart:
        del cart[str(product_id)]
        request.session['cart'] = cart
        messages.success(request, "Item removed from cart.")
        
    return redirect('store:cart_view')


def checkout_view(request):
    cart = request.session.get('cart', {})
    if not cart:
        messages.warning(request, "Your cart is empty.")
        return redirect('store:store_view')

    cart_items = []
    subtotal = 0
    for product_id, quantity in cart.items():
        try:
            product = Product.objects.get(id=product_id, is_active=True)
            total = product.price * quantity
            subtotal += total
            cart_items.append({
                'product': product,
                'quantity': quantity,
                'total': total,
            })
        except Product.DoesNotExist:
            pass

    shipping_cost = 0 if subtotal > 100 or subtotal == 0 else 10
    grand_total = subtotal + shipping_cost

    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        address = request.POST.get('address')
        city = request.POST.get('city')
        zipcode = request.POST.get('zipcode')

        if not name or not email or not address or not city or not zipcode:
            messages.error(request, "Please fill in all shipping details.")
        else:
            sufficient_stock = True
            for item in cart_items:
                if item['quantity'] > item['product'].stock:
                    messages.error(request, f"Sorry, the quantity for {item['product'].name} exceeds the current stock ({item['product'].stock} left).")
                    sufficient_stock = False
            
            if sufficient_stock:
                order = Order.objects.create(
                    user=request.user if request.user.is_authenticated else None,
                    shipping_name=name,
                    shipping_email=email,
                    shipping_address=address,
                    shipping_city=city,
                    shipping_zipcode=zipcode,
                    total_price=grand_total,
                    transaction_id=str(uuid.uuid4()).split('-')[0].upper(),
                    status='Pending'
                )

                for item in cart_items:
                    OrderItem.objects.create(
                        order=order,
                        product=item['product'],
                        price=item['product'].price,
                        quantity=item['quantity']
                    )
                    item['product'].stock -= item['quantity']
                    item['product'].save()

                request.session['cart'] = {}
                messages.success(request, "Order placed successfully!")
                return redirect('store:order_success', order_id=order.id)

    context = {
        'cart_items': cart_items,
        'subtotal': subtotal,
        'shipping_cost': shipping_cost,
        'grand_total': grand_total,
    }
    return render(request, 'store/checkout.html', context)


def order_success(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    context = {
        'order': order,
    }
    return render(request, 'store/success.html', context)
