from django.core.files.storage import FileSystemStorage
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from sdu_beta_web_app.filters import *
from sdu_beta_web_app.models import *
from django.core.paginator import Paginator, EmptyPage
import datetime
import xlwt
from django.core.mail import EmailMessage


from django.utils.encoding import force_bytes, force_text, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.sites.shortcuts import get_current_site
from .utils import token_generator

import re
STUDENT_REGEX = re.compile(r'^[0-9]+@stu\.sdu\.edu\.kz$')
STAFF_REGEX = re.compile(r'^[a-z.]+@sdu\.edu\.kz$')


def admin_home(request):
    return render(request, "admin_template/home.html")

def admin_profile(request):
    user = CustomUser.objects.get(id=request.user.id)
    admin = Admin.objects.get(admin=request.user.id)
    return render(request, "admin_template/admin_profile.html", {"user": user, "admin": admin})

def edit_admin_profile(request):
    user = CustomUser.objects.get(id=request.user.id)
    return render(request, "admin_template/edit_profile.html", {"user": user})

def update_admin_profile(request):
    if request.method != "POST":
        return HttpResponseRedirect(reverse("admin_profile"))
    else:
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        username = request.POST.get("username")
        if request.FILES.get('picture', False):
            picture = request.FILES['picture']
            fs = FileSystemStorage()
            filename = fs.save(picture.name, picture)
            picture_url = fs.url(filename)
        else:
            picture_url = None
        try:
            user = CustomUser.objects.get(id=request.user.id)
            user.username = username
            user.first_name = first_name
            user.last_name = last_name
            user.save()
            admin = Admin.objects.get(admin=request.user.id)

            if picture_url is not None:
                admin.display_image = picture_url
            admin.save()
            messages.success(request, "Admin profile updated successfully")
            return HttpResponseRedirect(reverse("admin_profile"))
        except:
            messages.error(request, "Failed to update Admin profile")
            return HttpResponseRedirect(reverse("admin_profile"))

def add_staff(request):
    return render(request, "admin_template/add_staff.html")


def save_staff(request):
    if request.method != "POST":
        return HttpResponseRedirect(reverse("add_staff"))
    else:
        email = request.POST.get("email")
        password = request.POST.get("password")
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        username = request.POST.get("username")
        address = request.POST.get("address")
        gender = request.POST.get("gender")
        if request.FILES.get('picture', False):
            picture = request.FILES['picture']
            fs = FileSystemStorage()
            filename = fs.save(picture.name, picture)
            picture_url = fs.url(filename)
        else:
            picture_url = '/media/default.jpg'
        try:
            staff_email = CustomUser.objects.filter(email=email).exists()
            if STAFF_REGEX.match(email) and not staff_email:
                user = CustomUser.objects.create_user(email=email, password=password, username=username,
                                                      last_name=last_name, first_name=first_name, user_type=2)
                user.staffs.address = address
                user.staffs.gender = gender
                user.staffs.display_image = picture_url
                user.save()
                messages.success(request, "Staff has been successfully added")
                return HttpResponseRedirect(reverse("manage_staff"))
            else:
                messages.error(request, "Please use SDU email or this email is already being used by another account")
                return HttpResponseRedirect(reverse("add_staff"))
        except:
            messages.error(request, "Failed to Add Staff")
            return HttpResponseRedirect(reverse("add_staff"))


def manage_staff(request):
    staffs = Staffs.objects.all().order_by("staff__last_name", "staff__first_name")
    my_filter = StaffFilter(request.GET, queryset=staffs)
    staffs = my_filter.qs
    p = Paginator(staffs, 5)
    page_num = request.GET.get('page', 1)
    try:
        page = p.page(page_num)
    except EmptyPage:
        page = p.page(1)
    return render(request, "admin_template/manage_staff.html", {"staffs": page})


def edit_staff(request, staff_id):
    try:
        staff = Staffs.objects.get(staff=staff_id)
        return render(request, "admin_template/edit_staff.html", {"staff": staff, "id": staff_id})
    except:
        return redirect('/manage_staff')


def update_staff(request):
    if request.method != "POST":
        return HttpResponseRedirect(reverse("edit_staff"))
    else:
        staff_id = request.POST.get("staff_id")
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        username = request.POST.get("username")
        address = request.POST.get("address")
        gender = request.POST.get("gender")
        if request.FILES.get('picture', False):
            picture = request.FILES['picture']
            fs = FileSystemStorage()
            filename = fs.save(picture.name, picture)
            picture_url = fs.url(filename)
        else:
            picture_url = None
        try:
            user = CustomUser.objects.get(id=staff_id)
            user.first_name = first_name
            user.last_name = last_name
            user.username = username
            user.save()

            staff = Staffs.objects.get(staff=staff_id)
            staff.address = address
            staff.gender = gender
            if picture_url is not None:
                staff.display_image = picture_url
            staff.save()
            messages.success(request, "Staff profile updated successfully")
            return HttpResponseRedirect(reverse("manage_staff"))
        except:
            messages.error(request, "Failed to update Staff profile")
            return HttpResponseRedirect(reverse("edit_staff", kwargs={"staff_id": staff_id}))


def delete_staff(request, staff_id):
    try:
        staff = Staffs.objects.get(staff=staff_id)
        staff.delete()
        user = CustomUser.objects.get(id=staff_id)
        user.delete()
        return redirect('/manage_staff')
    except:
        return redirect('/manage_staff')


def add_company(request):
    return render(request, "admin_template/add_company.html")


def save_company(request):
    if request.method != "POST":
        return HttpResponseRedirect(reverse("add_company"))
    else:
        email = request.POST.get("email")
        password = request.POST.get("password")
        username = request.POST.get("username")
        address = request.POST.get("address")
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        if request.FILES.get('picture', False):
            picture = request.FILES['picture']
            fs = FileSystemStorage()
            filename = fs.save(picture.name, picture)
            picture_url = fs.url(filename)
        else:
            picture_url = '/media/default.jpg'
        try:
            user = CustomUser.objects.create_user(email=email, password=password, username=username, last_name=last_name, first_name=first_name, user_type=3)
            user.company.address = address
            user.company.display_image = picture_url
            user.save()
            messages.success(request, "Company has been successfully added")
            return HttpResponseRedirect(reverse("manage_company"))
        except:
            messages.error(request, "Failed to Add Company")
            return HttpResponseRedirect(reverse("add_company"))

def manage_company(request):
    companies = Company.objects.all().order_by("company__last_name", "company__first_name")
    my_filter = CompanyFilter(request.GET, queryset=companies)
    companies = my_filter.qs
    p = Paginator(companies, 5)
    page_num = request.GET.get('page', 1)
    try:
        page = p.page(page_num)
    except EmptyPage:
        page = p.page(1)
    return render(request, "admin_template/manage_company.html", {"companies": page})


def edit_company(request, company_id):
    try:
        company = Company.objects.get(company=company_id)
        return render(request, "admin_template/edit_company.html", {"company": company, "id": company_id})
    except:
        return redirect('/manage_company')

def update_company(request):
    if request.method != "POST":
        return HttpResponseRedirect(reverse("edit_company"))
    else:
        company_id = request.POST.get("company_id")
        username = request.POST.get("username")
        address = request.POST.get("address")
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        if request.FILES.get('picture', False):
            picture = request.FILES['picture']
            fs = FileSystemStorage()
            filename = fs.save(picture.name, picture)
            picture_url = fs.url(filename)
        else:
            picture_url = None
        try:
            user = CustomUser.objects.get(id=company_id)
            user.username = username
            user.first_name = first_name
            user.last_name = last_name
            user.save()

            company = Company.objects.get(company=company_id)
            company.address = address
            if picture_url is not None:
                company.display_image = picture_url
            company.save()
            messages.success(request, "Company profile updated successfully")
            return HttpResponseRedirect(reverse("manage_company"))
        except:
            messages.error(request, "Failed to update Company profile")
            return HttpResponseRedirect(reverse("edit_company", kwargs={"company_id": company_id}))


def delete_company(request, company_id):
    try:
        company = Company.objects.get(company=company_id)
        company.delete()
        user = CustomUser.objects.get(id=company_id)
        user.delete()
        return redirect('/manage_company')
    except:
        return redirect('/manage_company')

@csrf_exempt
def whitelist(request):
    if request.method != "POST":
        return HttpResponseRedirect(reverse("manage_company"))
    else:
        uncheck_id = request.POST.getlist("uncheck_id[]")
        for id in uncheck_id:
            company = Company.objects.get(id=id)
            company.in_whitelist = False
            company.save()
        company_id = request.POST.getlist("id[]")
        for id in company_id:
            company = Company.objects.get(id=id)
            company.in_whitelist = True
            company.save()
        return HttpResponseRedirect(reverse("manage_company"))


def add_student(request):
    return render(request, "admin_template/add_student.html")


def save_student(request):
    if request.method != "POST":
        return HttpResponseRedirect(reverse("add_student"))
    else:
        email = request.POST.get("email")
        password = request.POST.get("password")
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        address = request.POST.get("address")
        gender = request.POST.get("gender")
        username = email.replace("@stu.sdu.edu.kz", "")
        if request.FILES.get('picture', False):
            picture = request.FILES['picture']
            fs = FileSystemStorage()
            filename = fs.save(picture.name, picture)
            picture_url = fs.url(filename)
        else:
            picture_url = '/media/default.jpg'
        try:
            student_email = CustomUser.objects.filter(email=email).exists()
            if STUDENT_REGEX.match(email) and not student_email:
                user = CustomUser.objects.create_user(email=email, password=password, username=username,
                                                      last_name=last_name, first_name=first_name, user_type=4)
                user.students.address = address
                user.students.gender = gender
                user.students.display_image = picture_url
                user.save()
                messages.success(request, "Student has been successfully added")
                return HttpResponseRedirect(reverse("manage_student"))
            else:
                messages.error(request, "Please use SDU email or this email is already being used by another account")
                return HttpResponseRedirect(reverse("add_student"))
        except:
            messages.error(request, "Failed to Add Student")
            return HttpResponseRedirect(reverse("add_student"))


def manage_student(request):
    students = Students.objects.all().order_by("student__last_name", "student__first_name")
    my_filter = StudentFilter(request.GET, queryset=students)
    students = my_filter.qs
    p = Paginator(students, 5)
    page_num = request.GET.get('page', 1)
    try:
        page = p.page(page_num)
    except EmptyPage:
        page = p.page(1)

    return render(request, "admin_template/manage_student.html", {"students": page})


def edit_student(request, student_id):
    try:
        student = Students.objects.get(student=student_id)
        return render(request, "admin_template/edit_student.html", {"student": student, "id": student_id})
    except:
        return redirect('/manage_student')

def update_student(request):
    if request.method != "POST":
        return HttpResponseRedirect(reverse("edit_student"))
    else:
        student_id = request.POST.get("student_id")
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        address = request.POST.get("address")
        gender = request.POST.get("gender")
        if request.FILES.get('picture', False):
            picture = request.FILES['picture']
            fs = FileSystemStorage()
            filename = fs.save(picture.name, picture)
            picture_url = fs.url(filename)
        else:
            picture_url = None
        try:
            user = CustomUser.objects.get(id=student_id)
            user.first_name = first_name
            user.last_name = last_name
            user.save()

            student = Students.objects.get(student=student_id)
            student.address = address
            student.gender = gender
            if picture_url is not None:
                student.display_image = picture_url
            student.save()
            messages.success(request, "Student profile updated successfully")
            return HttpResponseRedirect(reverse("manage_student"))
        except:
            messages.error(request, "Failed to update Student profile")
            return HttpResponseRedirect(reverse("edit_student", kwargs={"student_id": student_id}))


def delete_student(request, student_id):
    try:
        student = Students.objects.get(student_id=student_id)
        student.delete()
        user = CustomUser.objects.get(id=student_id)
        user.delete()
        return redirect('/manage_student')
    except:
        return redirect('/manage_student')


def student_messages(request):
    feedbacks = Students_feedback.objects.all()
    return render(request, "admin_template/student_messages.html", {"feedbacks": feedbacks})

def staff_messages(request):
    feedbacks = Staff_feedback.objects.all()
    return render(request, "admin_template/staff_messages.html", {"feedbacks": feedbacks})

def company_messages(request):
    feedbacks = Company_feedback.objects.all()
    return render(request, "admin_template/company_messages.html", {"feedbacks": feedbacks})

@csrf_exempt
def student_reply(request):
    feedback_id = request.POST.get("id")
    feedback_message = request.POST.get("message")
    try:
        feedback = Students_feedback.objects.get(id=feedback_id)
        feedback.feedback_reply = feedback_message
        feedback.save()
        return HttpResponse("True")
    except:
        return HttpResponseRedirect(reverse("student_messages"))

@csrf_exempt
def staff_reply(request):
    feedback_id = request.POST.get("id")
    feedback_message = request.POST.get("message")
    try:
        feedback = Staff_feedback.objects.get(id=feedback_id)
        feedback.feedback_reply = feedback_message
        feedback.save()
        return HttpResponse("True")
    except:
        return HttpResponseRedirect(reverse("staff_messages"))

@csrf_exempt
def company_reply(request):
    feedback_id = request.POST.get("id")
    feedback_message = request.POST.get("message")
    try:
        feedback = Company_feedback.objects.get(id=feedback_id)
        feedback.feedback_reply = feedback_message
        feedback.save()
        return HttpResponse("True")
    except:
        return HttpResponseRedirect(reverse("company_messages"))

def set_end_date(request):
    if request.method != "POST":
        return HttpResponseRedirect(reverse("manage_registration"))
    else:
        end_date = request.POST.get("expiry_date")
        try:
            exp_date = Expiration_date(end_date=end_date)
            exp_date.save()
            messages.success(request, "Registration date successfully set")
            return HttpResponseRedirect(reverse("manage_registration"))
        except:
            messages.error(request, "Failed to set registration date")
            return HttpResponseRedirect(reverse("manage_registration"))


def manage_registration(request):
    registrations = Students_registration.objects.all().order_by("student_id__student__last_name", "student_id__student__first_name")
    my_filter = RegistrationFilter(request.GET, queryset=registrations)
    registrations = my_filter.qs
    p = Paginator(registrations, 15)
    page_num = request.GET.get('page', 1)
    try:
        page = p.page(page_num)
    except EmptyPage:
        page = p.page(1)
    exp_date = Expiration_date.objects.last()
    return render(request, "admin_template/manage_registration.html", {"registrations": page, "exp_date": exp_date, "my_filter": my_filter})

def reg_approve(request, student_id):
    try:
        registration = Students_registration.objects.get(student_id=student_id)
        registration.registration_status = 1
        registration.save()
        student = Students.objects.get(id=student_id)
        check_exists = Grades_List.objects.filter(student_id=student).exists()
        if not check_exists:
            grade_list = Grades_List(student_id=student, report_marks=0)
            grade_list.save()
        return redirect('/manage_registration')
    except:
        return redirect('/manage_registration')

def reg_reject(request, student_id):
    try:
        registration = Students_registration.objects.get(student_id=student_id)
        registration.registration_status = 2
        registration.save()
        return redirect('/manage_registration')
    except:
        return redirect('/manage_registration')

def reg_cancel(request, student_id):
    try:
        registration = Students_registration.objects.get(student_id=student_id)
        registration.registration_status = 0
        registration.reject_reason = ""
        registration.save()
        student = Students.objects.get(id=student_id)
        try:
            grade_list = Grades_List.objects.get(student_id=student)
            grade_list.delete()
        except:
            return redirect('/manage_registration')
        return redirect('/manage_registration')
    except:
        return redirect('/manage_registration')

@csrf_exempt
def reject_reply(request):
    registration_id = request.POST.get("id")
    reject_reason = request.POST.get("message")
    try:
        registration = Students_registration.objects.get(id=registration_id)
        registration.reject_reason = reject_reason
        registration.save()
        return HttpResponse("True")
    except:
        return HttpResponseRedirect(reverse("manage_registration"))

def add_report(request):
    return render(request, "admin_template/add_report.html")

def save_report(request):
    if request.method != "POST":
        return HttpResponseRedirect(reverse("add_report"))
    else:
        report_name = request.POST.get("report_name")
        report_detail = request.POST.get("report_detail")
        due_date = request.POST.get("due_date")
        try:
            report = Reports(report_name=report_name, report_detail=report_detail, due_date=due_date)
            report.save()
            messages.success(request, "Report has been successfully added")
            return HttpResponseRedirect(reverse("manage_report"))
        except:
            messages.error(request, "Failed to Add Report")
            return HttpResponseRedirect(reverse("add_report"))

def manage_report(request):
    reports = Reports.objects.all()
    return render(request, "admin_template/manage_report.html", {"reports": reports})

def edit_report(request, report_id):
    try:
        report = Reports.objects.get(id=report_id)
        return render(request, "admin_template/edit_report.html", {"report": report, "id": report_id})
    except:
        return redirect('/manage_report')

def update_report(request):
    if request.method != "POST":
        return HttpResponseRedirect(reverse("manage_report"))
    else:
        report_id = request.POST.get("report_id")
        report_name = request.POST.get("report_name")
        report_detail = request.POST.get("report_detail")
        due_date = request.POST.get("due_date")
        try:
            report = Reports.objects.get(id=report_id)
            report.report_name = report_name
            report.report_detail = report_detail
            report.due_date = due_date
            report.save()
            messages.success(request, "Report updated successfully")
            return HttpResponseRedirect(reverse("manage_report"))
        except:
            messages.error(request, "Failed to updated Report")
            return HttpResponseRedirect(reverse("manage_report"))

def delete_report(request, report_id):
    try:
        report = Reports.objects.get(id=report_id)
        report.delete()
        messages.success(request, "Report is deleted")
        return HttpResponseRedirect(reverse("manage_report"))
    except:
        messages.error(request, "Report doesn't exist")
        return HttpResponseRedirect(reverse("manage_report"))

def view_report(request, report_id):
    reports = Report_submitting.objects.filter(report_id=report_id).order_by("student_id__student__last_name", "student_id__student__first_name")
    my_filter = ReportFilter(request.GET, queryset=reports)
    reports = my_filter.qs
    report_id = Reports.objects.get(id=report_id)
    return render(request, "admin_template/view_report.html", {"reports": reports, "report_id": report_id, "my_filter": my_filter})

def set_grade(request):
    if request.method != "POST":
        return HttpResponseRedirect(reverse("manage_report"))
    else:
        try:
            report_id = request.POST.get("report_id")
            submit_id = request.POST.getlist("submit_id")
            grade = request.POST.getlist("grade")
            zipped_data = zip(submit_id, grade)
            for s, g in zipped_data:
                submit_report = Report_submitting.objects.get(id=s)
                student = Students.objects.get(student=submit_report.student_id.student)
                if submit_report.submission_status == 0:
                    continue
                else:
                    if submit_report.grade != 0:
                        try:
                            grade_list = Grades_List.objects.get(student_id=student)
                            grade_list.report_marks = grade_list.report_marks - submit_report.grade + int(g)
                            grade_list.save()
                        except Grades_List.DoesNotExist:
                            grade_list = Grades_List(student_id=student, report_marks=0)
                            grade_list.report_marks = int(g)
                            grade_list.save()
                    else:
                        try:
                            grade_list = Grades_List.objects.get(student_id=student)
                            grade_list.report_marks = grade_list.report_marks + int(g)
                            grade_list.save()
                        except Grades_List.DoesNotExist:
                            grade_list = Grades_List(student_id=student, report_marks=0)
                            grade_list.report_marks = int(g)
                            grade_list.save()
                    submit_report.grade = g
                    submit_report.submission_status = 2
                    submit_report.save()
            messages.success(request, "Grades have been successfully submitted")
            return HttpResponseRedirect(reverse("view_report", kwargs={"report_id": report_id}))
        except:
            messages.error(request, "Failed to Set Grade")
            return HttpResponseRedirect(reverse("view_report", kwargs={"report_id": report_id}))


def grades(request):
    registrations = Students_registration.objects.filter(registration_status=1).order_by("student_id__student__last_name", "student_id__student__first_name")
    my_filter = RegistrationFilter(request.GET, queryset=registrations)
    registrations = my_filter.qs
    p = Paginator(registrations, 15)
    page_num = request.GET.get('page', 1)
    try:
        page = p.page(page_num)
    except EmptyPage:
        page = p.page(1)
    return render(request, "admin_template/grades.html", {"registrations": page, "my_filter": my_filter})

def view_grade(request, student_id):
    coordinator = CustomUser.objects.get(id=request.user.id)
    try:
        student = Students.objects.get(student=student_id)
        registered = Students_registration.objects.get(student_id=student)
    except:
        student = None
        registered = None
    if registered and registered.registration_status == 1:
        supervisor = CustomUser.objects.get(id=registered.supervisor_id.id)
        grade = 0
        s_mark = 0
        f_mark = 0
        try:
            grade_list = Grades_List.objects.get(student_id=student)
            s_mark = grade_list.supervisor_marks
            f_mark = grade_list.final_marks
            grade = grade_list.report_marks
        except Grades_List.DoesNotExist:
            grade_list = Grades_List(student_id=student)
            grade_list.save()
        grade = round(grade/15)
        total = s_mark * 0.6 + grade * 0.15 + f_mark * 0.25
        total = round(total)
        return render(request, "admin_template/grades_list.html", {"s_mark": s_mark, "f_mark": f_mark, "grade": grade, "total": total, "supervisor": supervisor, "coordinator": coordinator, "id": student_id, "student": student, "grade_list": grade_list})
    else:
        return HttpResponseRedirect(reverse("grades"))

@csrf_exempt
def set_final_grade(request):
    if request.method != "POST":
        return HttpResponseRedirect(reverse("grades"))
    else:
            grade_id = request.POST.get("grade_id")
            student_id = request.POST.get("student_id")
            final_grade = request.POST.get("final_grade")
            try:
                grade = Grades_List.objects.get(id=grade_id)
                grade.final_marks = final_grade
                grade.save()
                return HttpResponse("True")
            except:
                return HttpResponseRedirect(reverse("view_grade", kwargs={"student_id": student_id}))

@csrf_exempt
def reset_final_grade(request):
    if request.method != "POST":
        return HttpResponseRedirect(reverse("grades"))
    else:
            grade_id = request.POST.get("grade_id")
            student_id = request.POST.get("student_id")
            try:
                grade = Grades_List.objects.get(id=grade_id)
                grade.final_marks = 0
                grade.save()
                return HttpResponse("True")
            except:
                return HttpResponseRedirect(reverse("view_grade", kwargs={"student_id": student_id}))

def add_post(request):
    return render(request, "admin_template/add_post.html")

def save_post(request):
    if request.method != "POST":
        return HttpResponseRedirect(reverse("add_post"))
    else:
        title = request.POST.get("title")
        body = request.POST.get("body")
        author = Admin.objects.get(admin=request.user.id)
        try:
            post = Post(title=title, body=body, author=author)
            post.save()
            messages.success(request, "Post has been successfully added")
            return HttpResponseRedirect(reverse("manage_post"))
        except:
            messages.error(request, "Failed to Add Report")
            return HttpResponseRedirect(reverse("add_post"))

def manage_post(request):
    posts = Post.objects.all()
    return render(request, "admin_template/manage_post.html", {"posts": posts})

def edit_post(request, post_id):
    try:
        post = Post.objects.get(id=post_id)
        return render(request, "admin_template/edit_post.html", {"post": post, "id": post_id})
    except:
        return redirect('/manage_post')

def update_post(request):
    if request.method != "POST":
        return HttpResponseRedirect(reverse("manage_post"))
    else:
        post_id = request.POST.get("post_id")
        title = request.POST.get("title")
        body = request.POST.get("body")
        try:
            post = Post.objects.get(id=post_id)
            post.title = title
            post.body = body
            post.save()
            messages.success(request, "Post updated successfully")
            return HttpResponseRedirect(reverse("manage_post"))
        except:
            messages.error(request, "Failed to updated Post")
            return HttpResponseRedirect(reverse("manage_post"))

def delete_post(request, post_id):
    try:
        post = Post.objects.get(id=post_id)
        post.delete()
        messages.success(request, "Post is deleted")
        return HttpResponseRedirect(reverse("manage_post"))
    except:
        messages.error(request, "Post doesn't exist")
        return HttpResponseRedirect(reverse("manage_post"))

def view_post(request, post_id):
    try:
        post = Post.objects.get(id=post_id)
        author = Admin.objects.get(admin=request.user.id)
        comments = Comments.objects.filter(post=post_id)
        commentCount = Comments.objects.filter(post=post_id).count()
        return render(request, "admin_template/view_post.html", {"post": post, "id": post_id, "author": author, "comments": comments, "commentCount":commentCount})
    except:
        messages.error(request, "Post doesn't exist")
        return HttpResponseRedirect(reverse("manage_post"))

def admin_comment(request):
    if request.method != "POST":
        return HttpResponseRedirect(reverse("manage_post"))
    else:
        post_id = request.POST.get("post_id")
        body = request.POST.get("comment")
        post = Post.objects.get(id=post_id)
        author = CustomUser.objects.get(id=request.user.id)
        try:
            comment = Comments(post=post, body=body, author=author)
            comment.save()
            return HttpResponseRedirect(reverse("view_post", kwargs={"post_id": post_id}))
        except:
            messages.error(request, "Failed to Comment")
            return HttpResponseRedirect(reverse("manage_post"))

def delete_comment(request, comment_id, post_id):
    try:
        comment = Comments.objects.get(id=comment_id)
        comment.delete()
        return HttpResponseRedirect(reverse("view_post", kwargs={"post_id": post_id}))
    except:
        messages.error(request, "Comment doesn't exist")
        return HttpResponseRedirect(reverse("manage_post"))

def export_excel(request):
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename=Grades List ' + str(datetime.datetime.now()) + '.xls'
    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('Grades List')
    row_num = 0
    font_style = xlwt.XFStyle()
    font_style.font.bold = True

    columns = ['Student name', 'Student surname', 'Student ID', 'Mentors mark/60', 'Reports mark/15', 'Defenses mark/25', 'Total']
    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)

    font_style = xlwt.XFStyle()

    grades_list = Grades_List.objects.all().values_list('student_id__student__first_name', 'student_id__student__last_name', 'student_id__student__username', 'supervisor_marks', 'report_marks', 'final_marks')

    for row in grades_list:
        row_num +=1

        for col_num in range(len(row)):
            if col_num == 4:
                report_mark = round(int(row[col_num])/15)
                ws.write(row_num, col_num, report_mark, font_style)
            else:
                ws.write(row_num, col_num, row[col_num], font_style)
        total = row[3] * 0.6 + round(row[4]/15) * 0.15 + row[5] * 0.25
        total = round(total)
        ws.write(row_num, 6, str(total), font_style)
    wb.save(response)
    return response