from django.core.files.storage import FileSystemStorage
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import login, logout
from django.urls import reverse
from django.contrib import messages
from sdu_beta_web_app.Email import Email
from sdu_beta_web_app.models import *
from django.utils.encoding import force_bytes, force_text, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.sites.shortcuts import get_current_site
from .utils import token_generator
from django.core.mail import EmailMessage
import re
STUDENT_REGEX = re.compile(r'^[0-9]+@stu\.sdu\.edu\.kz$')
STAFF_REGEX = re.compile(r'^[a-z.]+@sdu\.edu\.kz$')

# Create your views here.

def showLogin(request):
    if request.user.is_authenticated:
        if request.user.user_type == "1":
            return HttpResponseRedirect(reverse('admin_home'))
        if request.user.user_type == "2":
            return HttpResponseRedirect(reverse('staff_home'))
        elif request.user.user_type == "3":
            return HttpResponseRedirect(reverse("company_home"))
        else:
            return HttpResponseRedirect(reverse("student_home"))
    else:
        return render(request, "login_page.html")

def signup(request):
    return render(request, "signup.html")

def signin(request):
    if request.method != "POST":
        return HttpResponseRedirect('/')
    else:
        user = Email.authenticate(request, username=request.POST.get("email"), password=request.POST.get("password"))
        if user != None:
            login(request, user)
            if user.user_type == "1":
                return HttpResponseRedirect('/admin_home')
            elif user.user_type == "2":
                return HttpResponseRedirect(reverse("staff_home"))
            elif user.user_type == "3":
                return HttpResponseRedirect(reverse("company_home"))
            else:
                return HttpResponseRedirect(reverse("student_home"))
        else:
            messages.error(request, "Invalid login. Please, enter the correct username and password")
            return HttpResponseRedirect("/")

def log_out(request):
    logout(request)
    return HttpResponseRedirect("/")

def save_user(request):
    if request.method != "POST":
        return HttpResponseRedirect(reverse("sign_up"))
    else:
        email = request.POST.get("email")
        password = request.POST.get("password")
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        c_username = request.POST.get("c_username")
        s_username = request.POST.get("s_username")
        username = email.replace("@stu.sdu.edu.kz", "")
        address = request.POST.get("address")
        gender = request.POST.get("gender")
        user_type = request.POST.get("user_type")
        print(user_type)
        if request.FILES.get('picture', False):
            picture = request.FILES['picture']
            fs = FileSystemStorage()
            filename = fs.save(picture.name, picture)
            picture_url = fs.url(filename)
        else:
            picture_url = '/media/default.jpg'
        try:
            check_exist = CustomUser.objects.filter(email=email).exists()
            check_username = CustomUser.objects.filter(username=username).exists()
            check_cusername = CustomUser.objects.filter(username=c_username).exists()
            check_susername = CustomUser.objects.filter(username=s_username).exists()
            if not check_exist and not check_username and not check_cusername and not check_susername:
                if user_type == "Staff" and STAFF_REGEX.match(email):
                    user = CustomUser.objects.create_user(email=email, password=password, username=s_username,
                                                          last_name=last_name, first_name=first_name, user_type=2)
                    user.staffs.address = address
                    user.staffs.gender = gender
                    user.staffs.display_image = picture_url
                    user.is_active = False
                    user.save()
                    uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
                    domain = get_current_site(request).domain
                    link = reverse('activate', kwargs={'uidb64': uidb64, 'token': token_generator.make_token(user)})
                    activate_url = 'http://' + domain + link
                    email_subject = 'Activate your account'
                    email_body = 'Hi ' + user.username + '! Please use this link to verify your account\n' + activate_url
                    email = EmailMessage(
                        email_subject,
                        email_body,
                        'noreply@semycolon.com',
                        [email], )
                    email.send(fail_silently=False)
                    messages.success(request, "An email has been sent")
                    return HttpResponseRedirect(reverse("show_login"))
                elif user_type == "Student" and STUDENT_REGEX.match(email):
                    user = CustomUser.objects.create_user(email=email, password=password, username=username,
                                                          last_name=last_name, first_name=first_name, user_type=4)
                    user.students.address = address
                    user.students.gender = gender
                    user.students.display_image = picture_url
                    user.is_active = False
                    user.save()
                    uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
                    domain = get_current_site(request).domain
                    link = reverse('activate', kwargs={'uidb64': uidb64, 'token': token_generator.make_token(user)})
                    activate_url = 'http://' + domain + link
                    email_subject = 'Activate your account'
                    email_body = 'Hi ' + user.username + '! Please use this link to verify your account\n' + activate_url
                    email = EmailMessage(
                        email_subject,
                        email_body,
                        'noreply@semycolon.com',
                        [email], )
                    email.send(fail_silently=False)
                    messages.success(request, "An email has been sent")
                    return HttpResponseRedirect(reverse("show_login"))
                elif user_type == "Company":
                    user = CustomUser.objects.create_user(email=email, password=password, username=c_username,
                                                          last_name=last_name, first_name=first_name, user_type=3)
                    user.company.address = address
                    user.company.display_image = picture_url
                    user.is_active = False
                    user.save()
                    uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
                    domain = get_current_site(request).domain
                    link = reverse('activate', kwargs={'uidb64': uidb64, 'token': token_generator.make_token(user)})
                    activate_url = 'http://' + domain + link
                    email_subject = 'Activate your account'
                    email_body = 'Hi ' + user.username + '! Please use this link to verify your account\n' + activate_url
                    email = EmailMessage(
                        email_subject,
                        email_body,
                        'noreply@semycolon.com',
                        [email], )
                    email.send(fail_silently=False)
                    messages.success(request, "An email has been sent")
                    return HttpResponseRedirect(reverse("show_login"))
                else:
                    return HttpResponseRedirect(reverse("sing_up"))
            else:
                messages.error(request, "This email or username is already being used by another account")
                return HttpResponseRedirect(reverse("sign_up"))
        except:
            messages.error(request, "Failed to Sign Up")
            return HttpResponseRedirect(reverse("sign_up"))

def activate(request, uidb64, token):
    try:
        id = force_text(urlsafe_base64_decode(uidb64))
        user = CustomUser.objects.get(id=id)
        if user.is_active:
            messages.error(request, "User already activated")
            return redirect('/')
        user.is_active = True
        user.save()
        messages.success(request, "Your account has been successfully activated")
        return redirect('/')
    except:
        messages.error(request, "Account not activated")
        return redirect('/')

def error_404(request, exception):
    return render(request, "404.html")










