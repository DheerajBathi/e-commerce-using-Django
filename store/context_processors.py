def cart_processor(request):
    """
    Returns the total quantity of items in the cart, stored in session.
    Format of session cart: { 'product_id': quantity, ... }
    """
    cart = request.session.get('cart', {})
    total_items = sum(cart.values())
    return {'cart_count': total_items}
