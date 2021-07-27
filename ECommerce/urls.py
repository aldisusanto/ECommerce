"""ECommerce URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path

from ECommerce import settings
from ECommerceApp import views, admin_views

urlpatterns = [
                  path('admin/', admin.site.urls),
                  path('admin_login', views.AdminLogin, name="admin_login"),
                  path('admin_login_process', views.AdminLoginProcess, name="admin_login_process"),
                  path('admin_logout_process', views.AdminLogoutProcess, name="admin_logout_process"),

                  # Admin Page
                  path('admin_home', admin_views.AdminHome, name="admin_home"),
                  # Admin Page - Categories
                  path('category_list', admin_views.CategoriesListView.as_view(), name="category_list"),
                  path('category_create', admin_views.CategoriesCreate.as_view(), name="category_create"),
                  path('category_update/<slug:pk>', admin_views.CategoriesUpdate.as_view(), name="category_update"),
                  # Admin Page - Sub Categories
                  path('sub_category_list', admin_views.SubCategoryListView.as_view(), name="sub_category_list"),
                  path('sub_category_create', admin_views.SubCategoryCreate.as_view(), name="sub_category_create"),
                  path('sub_category_update/<slug:pk>', admin_views.SubCategoryUpdate.as_view(),
                       name="sub_category_update"),
                  # Admin Page - Merchant User
                  path('merchant_user_list', admin_views.MerchantUserListView.as_view(), name="merchant_user_list"),
                  path('merchant_user_create', admin_views.MerchantUserCreate.as_view(), name="merchant_user_create"),
                  path('merchant_user_update/<slug:pk>', admin_views.MerchantUserUpdate.as_view(),
                       name="merchant_user_update"),
                  # Admin Page - Staff User
                  path("staff_user_list", admin_views.StaffUserListView.as_view(), name="staff_user_list"),
                  path("staff_user_create", admin_views.StaffUserCreate.as_view(), name="staff_user_create"),
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + static(settings.STATIC_URL,
                                                                                         document_root=settings.STATIC_ROOT)
