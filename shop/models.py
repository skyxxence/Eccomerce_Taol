from django.db import models
from authentication.models import CustomUser


class Category(models.Model):
    name = models.CharField(max_length=255, unique=True)  # The category name (e.g., 'Electronics', 'Clothing', etc.)
    parent = models.ForeignKey('self', null=True, blank=True, related_name='subcategories', on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    # Optional: for better display in admin
    class Meta:
        verbose_name_plural = "Categories"

class SubCategory(models.Model):
    name = models.CharField(max_length=255, unique=True)  # The category name (e.g., 'Electronics', 'Clothing', etc.)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, related_name='sub_category', null=True, blank=True)  # Link to category

    def __str__(self):
        return self.name

    # Optional: for better display in admin
    class Meta:
        verbose_name_plural = "SubCategories"


    
# parent: This is a foreign key that points to the same Category model. It is used to define subcategories. If a category doesn't have a parent (like "Electronics"), this field will be null.
# related_name='subcategories': This allows you to access the subcategories of a parent category, e.g., category.subcategories.all().
# get_subcategories(): A helper method to retrieve the subcategories of a category.


class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    discount_percentage = models.DecimalField(max_digits=5, decimal_places=0, blank=True, null=True)  # Discount percentage
    stock = models.PositiveIntegerField(default=0)
    image = models.ImageField(upload_to='products/', null=True, blank=True)
    vendor_creating_product = models.ForeignKey(CustomUser, on_delete=models.CASCADE)  # Track which user is the vendor
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)  # Link to category
    subcategory = models.ForeignKey(SubCategory, on_delete=models.SET_NULL, null=True, blank=True)  # Link to subcategory
    created_at = models.DateTimeField(auto_now_add=True)
    
    @property
    def discounted_price(self):
        """Calculate the price after applying the discount."""
        if self.discount_percentage:
            discount_amount = (self.discount_percentage / 100) * self.price
            return self.price - discount_amount
        return self.price  # If no discount, return the original price

    @property
    def discount_amount(self):
        """Calculate the discount amount in currency."""
        if self.discount_percentage:
            return (self.discount_percentage / 100) * self.price
        return 0  # If no discount, return 0

    def formatted_price(self):
        """Format the price with commas and currency symbol."""
        return f"#{self.price:,.0f}"

    def formatted_discounted_price(self):
        """Format the discounted price with commas and currency symbol."""
        return f"#{self.discounted_price:,.0f}"

    def formatted_discount_amount(self):
        """Format the discount amount with commas and currency symbol."""
        return f"#{self.discount_amount:,.0f}"

    def __str__(self):
        return self.name


   

class Cart(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    items = models.ManyToManyField(Product)

    def __str__(self):
        return f"Cart for {self.user.username}"


