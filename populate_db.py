import os
import django

# Setup Django Environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ecommerce.settings')
django.setup()

from store.models import Category, Product, Review

def populate():
    print("Initializing Database Seeding...")

    # Define Categories
    categories_data = [
        {"name": "Electronics", "description": "Cutting edge smart gadgets and appliances."},
        {"name": "Audio", "description": "High-fidelity, noise-canceling auditory hardware."},
        {"name": "Lighting", "description": "Luminous smart ambient lamps and desk systems."},
        {"name": "Gear", "description": "Minimalist designer luggage and everyday carry equipment."}
    ]

    categories = {}
    for cat_info in categories_data:
        cat, created = Category.objects.get_or_create(
            name=cat_info["name"],
            defaults={"description": cat_info["description"]}
        )
        categories[cat_info["name"]] = cat
        if created:
            print(f"Created category: {cat.name}")

    # Define Products
    products_data = [
        # Electronics
        {
            "category": categories["Electronics"],
            "name": "Aura Watch Pro",
            "description": "An elegant wellness smartwatch featuring AMOLED retina always-on display, 14-day battery life, and biometric tracking sensors encased in aerospace-grade titanium.",
            "price": 299.99,
            "image_url": "https://images.unsplash.com/photo-1546868871-7041f2a55e12?q=80&w=800&auto=format&fit=crop",
            "stock": 15
        },
        {
            "category": categories["Electronics"],
            "name": "AuraPad Ultimate",
            "description": "Ultra-thin 11-inch liquid retina tablet powered by dynamic processor. Ideal for creators, engineers, and digital nomads seeking pure performance.",
            "price": 799.00,
            "image_url": "https://images.unsplash.com/photo-1544244015-0df4b3ffc6b0?q=80&w=800&auto=format&fit=crop",
            "stock": 8
        },
        # Audio
        {
            "category": categories["Audio"],
            "name": "SoundAura Studio Headphones",
            "description": "Over-ear active noise-canceling headphones tuned to perfection. Immerse yourself in deep bass and crisp spatial audio with custom 40mm transducers.",
            "price": 349.50,
            "image_url": "https://images.unsplash.com/photo-1505740420928-5e560c06d30e?q=80&w=800&auto=format&fit=crop",
            "stock": 25
        },
        {
            "category": categories["Audio"],
            "name": "AuraPulse Mini Speaker",
            "description": "IP67 waterproof outdoor bluetooth speaker delivering booming 360-degree acoustics. Small in hand, gargantuan in volume.",
            "price": 89.99,
            "image_url": "https://images.unsplash.com/photo-1608043152269-423dbba4e7e1?q=80&w=800&auto=format&fit=crop",
            "stock": 4
        },
        # Lighting
        {
            "category": categories["Lighting"],
            "name": "AuraGlow Smart Desk Lamp",
            "description": "Minimalist architectural lamp featuring modular swing arm, ambient color spectrum, wireless phone charging deck, and smart voice commands.",
            "price": 120.00,
            "image_url": "https://images.unsplash.com/photo-1507473885765-e6ed057f782c?q=80&w=800&auto=format&fit=crop",
            "stock": 30
        },
        # Gear
        {
            "category": categories["Gear"],
            "name": "AuraPack Minimalist Carryall",
            "description": "Water-resistant commuter backpack with secure layout compartments for 16-inch laptops, documents, and essential chargers.",
            "price": 149.00,
            "image_url": "https://images.unsplash.com/photo-1553062407-98eeb64c6a62?q=80&w=800&auto=format&fit=crop",
            "stock": 12
        }
    ]

    for prod_info in products_data:
        prod, created = Product.objects.get_or_create(
            name=prod_info["name"],
            defaults={
                "category": prod_info["category"],
                "description": prod_info["description"],
                "price": prod_info["price"],
                "image_url": prod_info["image_url"],
                "stock": prod_info["stock"]
            }
        )
        if created:
            print(f"Created product: {prod.name}")
            
            # Add seed reviews for newly created products
            Review.objects.create(
                product=prod,
                name="Aleksey T.",
                email="aleksey@example.com",
                rating=5,
                comment="Absolutely stunning build quality. Exceeded expectations and matches my workstation setup perfectly!"
            )
            Review.objects.create(
                product=prod,
                name="Miranda K.",
                email="miranda@example.com",
                rating=4,
                comment="Very high performance and gorgeous look. Shipping took an extra day but product is top-tier."
            )
        else:
            # If product exists, just update stock for testing
            prod.stock = prod_info["stock"]
            prod.save()

    print("Database seeding completed successfully!")

if __name__ == '__main__':
    populate()
