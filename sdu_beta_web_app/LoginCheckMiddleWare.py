from django.http import HttpResponseRedirect
from django.urls import reverse
from django.utils.deprecation import MiddlewareMixin

class LoginCheckMiddleWare(MiddlewareMixin):

    @staticmethod
    def process_view(request, view_func, view_args, view_kwargs):
        module_name = view_func.__module__
        user = request.user
        if user.is_authenticated:
            if user.user_type == "1":
                if module_name == "sdu_beta_web_app.AdminViews":
                    pass
                elif module_name == "sdu_beta_web_app.views" or module_name == "django.views.static":
                    pass
                else:
                    return HttpResponseRedirect(reverse("admin_home"))
            elif user.user_type == "2":
                if module_name == "sdu_beta_web_app.StaffViews":
                    pass
                elif module_name == "sdu_beta_web_app.views" or module_name == "django.views.static":
                    pass
                else:
                    return HttpResponseRedirect(reverse("staff_home"))
            elif user.user_type == "3":
                if module_name == "sdu_beta_web_app.CompanyViews":
                    pass
                elif module_name == "sdu_beta_web_app.views" or module_name == "django.views.static":
                    pass
                else:
                    return HttpResponseRedirect(reverse("company_home"))
            elif user.user_type == "4":
                if module_name == "sdu_beta_web_app.StudentViews":
                    pass
                elif module_name == "sdu_beta_web_app.views" or module_name == "django.views.static":
                    pass
                else:
                    return HttpResponseRedirect(reverse("student_home"))
            else:
                return HttpResponseRedirect(reverse("show_login"))

        else:
            if module_name == 'sdu_beta_web_app.views' or module_name == "django.contrib.auth.views":
                pass
            else:
                return HttpResponseRedirect(reverse("show_login"))