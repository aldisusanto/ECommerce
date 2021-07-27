from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.messages.views import SuccessMessageMixin
from django.core.files.storage import FileSystemStorage
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.views.generic import ListView, CreateView, UpdateView, DetailView

from ECommerceApp.forms import MerchantForm
from ECommerceApp.models import Category, SubCategories, CustomUser, Merchant


@login_required(login_url="/admin_login/")
def AdminHome(request):
    return render(request, "admin_templates/home_template.html")


class CategoriesListView(ListView):
    model = Category
    template_name = "admin_templates/category_list.html"
    paginate_by = 4

    def get_queryset(self):
        filter_val = self.request.GET.get("filter", "")
        order_by = self.request.GET.get("orderby", "id")
        if filter_val != "":
            category = Category.objects.filter(
                Q(title__contains=filter_val) | Q(description__contains=filter_val)).order_by(order_by)
        else:
            category = Category.objects.all().order_by(order_by)

        return category

    def get_context_data(self, **kwargs):
        context = super(CategoriesListView, self).get_context_data(**kwargs)
        context["filter"] = self.request.GET.get("filter", "")
        context["orderby"] = self.request.GET.get("orderby", "id")
        context["all_table_fields"] = Category._meta.get_fields()
        return context


class CategoriesCreate(SuccessMessageMixin, CreateView):
    model = Category
    success_message = "Category Added"
    fields = "__all__"
    template_name = "admin_templates/category_create.html"


class CategoriesUpdate(SuccessMessageMixin, UpdateView):
    model = Category
    success_message = "Category Successfully Updated"
    fields = "__all__"
    template_name = "admin_templates/category_update.html"


# View Sub Category
class SubCategoryListView(ListView):
    model = SubCategories
    template_name = "admin_templates/sub_category_list.html"


class SubCategoryCreate(SuccessMessageMixin, CreateView):
    model = SubCategories
    success_message = "Sub Category Successfully Added!!"
    fields = "__all__"
    template_name = "admin_templates/sub_category_create.html"


class SubCategoryUpdate(SuccessMessageMixin, UpdateView):
    model = SubCategories
    success_message = "Sub Category Successfully Update"
    fields = "__all__"
    template_name = "admin_templates/sub_category_update.html"


class MerchantUserListView(ListView):
    model = Merchant
    template_name = "admin_templates/merchant_user_list.html"


class MerchantUserCreate(SuccessMessageMixin, CreateView):
    model = CustomUser
    success_message = "Merchant User Successfully Added!!"
    fields = ["first_name", "last_name", "email", "username", "password"]
    template_name = "admin_templates/merchant_user_create.html"

    def form_valid(self, form):
        # Save CustomUser for Merchant User
        user = form.save(commit=False)
        user.is_active = True
        user.user_type = 3
        user.set_password(form.cleaned_data["password"])
        user.save()

        # Save Merchant User Profile
        profile_pic = self.request.FILES["profile_pic"]
        fs = FileSystemStorage()
        filename = fs.save(profile_pic.name, profile_pic)
        profile_pic_url = fs.url(filename)

        user.merchant.profile_pic = profile_pic_url
        user.merchant.company_name = self.request.POST.get("company_name")
        user.merchant.gst_details = self.request.POST.get("gst")
        user.merchant.address = self.request.POST.get("address")

        added_by_admin = False
        if self.request.POST.get("added_by_admin") == "on":
            added_by_admin = True

        user.merchant.added_by_admin = added_by_admin
        user.save()

        messages.success(self.request, "Merchant User Successfully Added")
        return HttpResponseRedirect(reverse('merchant_user_list'))


class MerchantUserUpdate(SuccessMessageMixin, UpdateView):
    model = CustomUser
    success_message = "Merchant User Successfully Update!!"
    fields = ["first_name", "last_name", "email", "username"]
    template_name = "admin_templates/merchant_user_update.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        merchant = Merchant.objects.get(auth_user_id=self.object.pk)
        context["merchant"] = merchant
        return context

    def form_valid(self, form):
        # Save CustomUser for Merchant User
        user = form.save(commit=False)
        user.save()

        # Save Merchant User Profile
        merchantuser = Merchant.objects.get(auth_user_id=user.id)
        if self.request.FILES.get("profile_pic", False):
            profile_pic = self.request.FILES["profile_pic"]
            fs = FileSystemStorage()
            filename = fs.save(profile_pic.name, profile_pic)
            profile_pic_url = fs.url(filename)

            merchantuser.profile_pic = profile_pic_url
        merchantuser.company_name = self.request.POST.get("company_name")
        merchantuser.gst_details = self.request.POST.get("gst")
        merchantuser.address = self.request.POST.get("address")

        added_by_admin = False
        if self.request.POST.get("added_by_admin") == "on":
            added_by_admin = True

        merchantuser.added_by_admin = added_by_admin
        merchantuser.save()

        messages.success(self.request, "Merchant User Successfully Update")
        return HttpResponseRedirect(reverse('merchant_user_list'))


class StaffUserListView(ListView):
    model = CustomUser
    template_name = "admin_templates/staff_user_list.html"


class StaffUserCreate(SuccessMessageMixin, CreateView):
    model = CustomUser
    success_message = "Staff User Successfully Added!!"
    fields = ["first_name", "last_name", "email", "username", "password"]
    template_name = "admin_templates/staff_user_create.html"

    def form_valid(self, form):
        # Save CustomUser for Staff User
        user = form.save(commit=False)
        user.is_active = True
        user.user_type = 2
        user.set_password(form.cleaned_data["password"])
        user.save()

        profile_pic = self.request.FILES["profile_pic"]
        fs = FileSystemStorage()
        filename = fs.save(profile_pic.name, profile_pic)
        profile_pic_url = fs.url(filename)
        user.staff.profile_pic = profile_pic_url
        user.save()

        messages.success(self.request, "Staff User Successfully Added !!")
        return HttpResponseRedirect(reverse("staff_user_list"))
