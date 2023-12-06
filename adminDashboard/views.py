from django.shortcuts import render
from django.contrib.auth.decorators import user_passes_test
# Create your views here.
@user_passes_test(lambda u: u.is_staff)  # Restrict access to staff members
def custom_dashboard_view(request):
    return render(request, 'admin/dashboard/change_list.html')