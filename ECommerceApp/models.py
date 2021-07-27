from django.contrib.auth.models import AbstractUser
from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_save

# Create your models here.
from django.urls import reverse


class CustomUser(AbstractUser):
    user_type_choice = ((1, "Admin"), (2, "Staff"), (3, "Merchant"), (4, "Customer"))
    user_type = models.CharField(max_length=255, default=1, choices=user_type_choice)


class Admin(models.Model):
    profile_pic = models.FileField(default="")
    auth_user_id = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    objects = models.Manager()


class Staff(models.Model):
    profile_pic = models.FileField(default="")
    auth_user_id = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    objects = models.Manager()


class Merchant(models.Model):
    profile_pic = models.FileField(default="")
    auth_user_id = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    company_name = models.CharField(max_length=255)
    gst_details = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    added_by_admin = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    objects = models.Manager()


class Customer(models.Model):
    profile_pic = models.FileField(default="")
    auth_user_id = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    objects = models.Manager()


class Category(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255)
    url_slug = models.CharField(max_length=255)
    thumbnail = models.FileField()
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.IntegerField(default=1)
    objects = models.Manager()

    def get_absolute_url(self):
        return reverse('category_list')

    def __str__(self):
        return self.title


class SubCategories(models.Model):
    id = models.AutoField(primary_key=True)
    category_id = models.ForeignKey(Category, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    url_slug = models.CharField(max_length=255)
    thumbnail = models.FileField()
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.IntegerField(default=1)
    objects = models.Manager()

    def get_absolute_url(self):
        return reverse('sub_category_list')


class Products(models.Model):
    id = models.AutoField(primary_key=True)
    sub_categories_id = models.ForeignKey(SubCategories, on_delete=models.CASCADE)
    url_slug = models.CharField(max_length=255)
    product_name = models.CharField(max_length=255)
    brand = models.CharField(max_length=255)
    product_max_price = models.CharField(max_length=255)
    product_discount = models.CharField(max_length=255)
    product_description = models.TextField()
    product_long_description = models.TextField()
    added_by_merchant = models.ForeignKey(Merchant, on_delete=models.CASCADE)
    in_stock_total = models.IntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.IntegerField(default=1)
    objects = models.Manager()


class ProductMedia(models.Model):
    id = models.AutoField(primary_key=True)
    product_id = models.ForeignKey(Products, on_delete=models.CASCADE)
    media_type_choice = ((1, "Image"), (2, "Video"))
    media_type = models.CharField(max_length=255, choices=media_type_choice)
    media_content = models.FileField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.IntegerField(default=1)
    objects = models.Manager()


class ProductTransaction(models.Model):
    id = models.AutoField(primary_key=True)
    product_id = models.ForeignKey(Products, on_delete=models.CASCADE)
    transaction_type_choice = ((1, "BUY"), (2, "SELL"))
    transaction_type = models.CharField(choices=transaction_type_choice, max_length=255)
    transaction_product_count = models.IntegerField(default=1)
    transaction_description = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    objects = models.Manager()


class ProductDetails(models.Model):
    id = models.AutoField(primary_key=True)
    product_id = models.ForeignKey(Products, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    title_description = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.IntegerField(default=1)
    objects = models.Manager()


class ProductAbout(models.Model):
    id = models.AutoField(primary_key=True)
    product_id = models.ForeignKey(Products, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.IntegerField(default=1)
    objects = models.Manager()


class ProductTag(models.Model):
    id = models.AutoField(primary_key=True)
    product_id = models.ForeignKey(Products, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.IntegerField(default=1)
    objects = models.Manager()


class ProductQuestion(models.Model):
    id = models.AutoField(primary_key=True)
    product_id = models.ForeignKey(Products, on_delete=models.CASCADE)
    user_id = models.ForeignKey(Customer, on_delete=models.CASCADE)
    question = models.TextField()
    answer = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.IntegerField(default=1)
    objects = models.Manager()


class ProductReview(models.Model):
    id = models.AutoField(primary_key=True)
    product_id = models.ForeignKey(Products, on_delete=models.CASCADE)
    user_id = models.ForeignKey(Customer, on_delete=models.CASCADE)
    rating = models.CharField(default=5, max_length=255)
    review_image = models.FileField()
    review = models.TextField(default="")
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.IntegerField(default=1)
    objects = models.Manager()


class ProductReviewVoting(models.Model):
    id = models.AutoField(primary_key=True)
    product_review_id = models.ForeignKey(ProductReview, on_delete=models.CASCADE)
    user_voting_id = models.ForeignKey(Customer, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.IntegerField(default=1)
    objects = models.Manager()


class ProductVariant(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    objects = models.Manager()


class ProductVariantItem(models.Model):
    id = models.AutoField(primary_key=True)
    product_variant_id = models.ForeignKey(ProductVariant, on_delete=models.CASCADE)
    product_id = models.ForeignKey(Products, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    objects = models.Manager()


class CustomerOrder(models.Model):
    id = models.AutoField(primary_key=True)
    product_id = models.ForeignKey(Products, on_delete=models.CASCADE)
    # user_id = models.ForeignKey(Customer, on_delete=models.CASCADE)
    purchase_price = models.CharField(max_length=255)
    coupon_code = models.CharField(max_length=255)
    discount_mt = models.CharField(max_length=255)
    product_status = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    objects = models.Manager()


class OrderDeliveryStatus(models.Model):
    id = models.AutoField(primary_key=True)
    order_id = models.ForeignKey(CustomerOrder, on_delete=models.CASCADE)
    status = models.CharField(max_length=255)
    status_message = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now_add=True)
    objects = models.Manager()


@receiver(post_save, sender=CustomUser)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        if instance.user_type == 1:
            Admin.objects.create(auth_user_id=instance)
        if instance.user_type == 2:
            Staff.objects.create(auth_user_id=instance)
        if instance.user_type == 3:
            Merchant.objects.create(auth_user_id=instance, company_name="", gst_details="", address="")
        if instance.user_type == 4:
            Customer.objects.create(auth_user_id=instance)


@receiver(post_save, sender=CustomUser)
def save_user_profile(sender, instance, **kwargs):
    if instance.user_type == 1:
        instance.admin.save()
    if instance.user_type == 2:
        instance.staff.save()
    if instance.user_type == 3:
        instance.merchant.save()
    if instance.user_type == 4:
        instance.customer.save()
