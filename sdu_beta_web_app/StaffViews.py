
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.contrib import messages
from sdu_beta_web_app.models import *
from django.core.files.storage import FileSystemStorage

def staff_home(request):
    return render(request, "staff_template/home.html")

def staff_profile(request):
    user = CustomUser.objects.get(id=request.user.id)
    return render(request, "staff_template/staff_profile.html", {"user": user})

def edit_staff_profile(request):
    user = CustomUser.objects.get(id=request.user.id)
    return render(request, "staff_template/edit_profile.html", {"user": user})

def update_staff_profile(request):
    if request.method != "POST":
        return HttpResponseRedirect(reverse("staff_profile"))
    else:
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        username = request.POST.get("username")
        address = request.POST.get("address")
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
            staff = Staffs.objects.get(staff=request.user.id)

            if picture_url is not None:
                staff.display_image = picture_url
            staff.address = address
            staff.save()
            messages.success(request, "Staff profile updated successfully")
            return HttpResponseRedirect(reverse("staff_profile"))
        except:
            messages.error(request, "Failed to update Staff profile")
            return HttpResponseRedirect(reverse("staff_profile"))

def staff_feedback(request):
    staff_id = Staffs.objects.get(staff=request.user.id)
    feedbacks = Staff_feedback.objects.filter(staff_id=staff_id)
    return render(request, "staff_template/staff_feedback.html", {"feedbacks": feedbacks})

def save_staff_feedback(request):
    if request.method != "POST":
        return HttpResponseRedirect(reverse("staff_feedback"))
    else:
        feedback_message = request.POST.get("feedback")
        staff_id = Staffs.objects.get(staff=request.user.id)
        try:
            feedback = Staff_feedback(staff_id=staff_id, feedback_message=feedback_message, feedback_reply="")
            feedback.save()
            messages.success(request, "Feedback sent successfully")
            return HttpResponseRedirect(reverse("staff_feedback"))
        except:
            messages.error(request, "Failed to send Feedback")
            return HttpResponseRedirect(reverse("staff_feedback"))

def my_students(request):
    supervisor = CustomUser.objects.get(id=request.user.id)
    reg = Students_registration.objects.filter(supervisor_id=supervisor.id, registration_status=1)
    studentList = Students_registration.objects.filter(supervisor_id=supervisor.id, registration_status=1).values_list('student_id', flat=True)
    for s in studentList:
        student = Students.objects.get(id=s)
        try:
            grade_list = Grades_List.objects.get(student_id=s)
        except:
            grade_list = Grades_List(student_id=student)
            grade_list.save()
    grades_list = Grades_List.objects.filter(student_id__in=studentList)
    return render(request, "staff_template/my_students.html", {"reg": reg, "grades_list": grades_list, "studentList": studentList})

def supervisor_grade(request):
    if request.method != "POST":
        return HttpResponseRedirect(reverse("my_students"))
    else:
        try:
            reg_id = request.POST.getlist("reg_id")
            grade = request.POST.getlist("sup_grade")
            zipped_data = zip(reg_id, grade)
            for s, g in zipped_data:
                student = Students.objects.get(id=s)
                try:
                    grades_list = Grades_List.objects.get(student_id=s)
                    grades_list.supervisor_marks = g
                    grades_list.save()
                except Grades_List.DoesNotExist:
                    grades_list = Grades_List(student_id=student, supervisor_marks=g)
                    grades_list.save()
            messages.success(request, "Grades have been successfully submitted")
            return HttpResponseRedirect(reverse("my_students"))
        except:
            messages.error(request, "Failed to set grades")
            return HttpResponseRedirect(reverse("my_students"))


def add_vacancy(request):
    return render(request, "staff_template/add_vacancy.html")

def vacancy_list(request):
    supervisor = CustomUser.objects.get(id=request.user.id)
    vacancies = VacancyList.objects.filter(supervisor=supervisor)
    return render(request, "staff_template/vacancy_list.html", {"vacancies": vacancies})

def save_vacancy(request):
    if request.method != "POST":
        return HttpResponseRedirect(reverse("vacancy_list"))
    else:
        name = request.POST.get("vacancy_name")
        requirements = request.POST.get("requirements")
        amount = request.POST.get("amount")
        supervisor = CustomUser.objects.get(id=request.user.id)
        try:
            vacancy = VacancyList(vacancy_name=name, requirements=requirements, amount=amount, supervisor=supervisor)
            vacancy.save()
            messages.success(request, "Vacancy has been successfully added")
            return HttpResponseRedirect(reverse("vacancy_list"))
        except:
            messages.error(request, "Failed to Add Vacancy")
            return HttpResponseRedirect(reverse("add_vacancy"))

def edit_vacancy(request, vacancy_id):
    try:
        vacancy = VacancyList.objects.get(id=vacancy_id)
        return render(request, "staff_template/edit_vacancy.html", {"vacancy": vacancy, "id": vacancy_id})
    except:
        return redirect('/vacancy_list')

def update_vacancy(request):
    if request.method != "POST":
        return HttpResponseRedirect(reverse("vacancy_list"))
    else:
        vacancy_id = request.POST.get("vacancy_id")
        name = request.POST.get("vacancy_name")
        requirements = request.POST.get("requirements")
        amount = request.POST.get("amount")
        try:
            vacancy = VacancyList.objects.get(id=vacancy_id)
            vacancy.vacancy_name = name
            vacancy.requirements = requirements
            vacancy.amount = amount
            vacancy.save()
            messages.success(request, "Vacancy updated successfully ")
            return HttpResponseRedirect(reverse("vacancy_list"))
        except:
            messages.error(request, "Failed to update Vacancy")
            return HttpResponseRedirect(reverse("vacancy_list"))

def delete_vacancy(request, vacancy_id):
    try:
        vacancy = VacancyList.objects.get(id=vacancy_id)
        respond = Vacancy_respond.objects.filter(vacancy_id=vacancy)
        respond.delete()
        vacancy.delete()
        messages.success(request, "Vacancy is deleted")
        return HttpResponseRedirect(reverse("vacancy_list"))
    except:
        messages.error(request, "Vacancy doesn't exist")
        return HttpResponseRedirect(reverse("vacancy_list"))

def view_respond(request, vacancy_id):
    try:
        vacancy = VacancyList.objects.get(id=vacancy_id)
        respond = Vacancy_respond.objects.filter(vacancy_id=vacancy)
        return render(request, "staff_template/view_respond.html", {"vacancy": vacancy, "id": vacancy_id, "respond": respond})
    except:
        return redirect('/vacancy_list')

def approve(request, student_id, vacancy_id):
    try:
        vacancy = VacancyList.objects.get(id=vacancy_id)
        respond = Vacancy_respond.objects.get(student_id=student_id, vacancy_id=vacancy)
        respond.vacancy_status = 1
        respond.save()
        vacancy.amount = vacancy.amount-1
        vacancy.save()
        return HttpResponseRedirect(reverse("view_respond", kwargs={"vacancy_id": vacancy_id}))
    except:
        return redirect('/vacancy_list')

def reject(request, student_id, vacancy_id):
    try:
        vacancy = VacancyList.objects.get(id=vacancy_id)
        respond = Vacancy_respond.objects.get(student_id=student_id, vacancy_id=vacancy)
        respond.vacancy_status = 2
        respond.save()
        return HttpResponseRedirect(reverse("view_respond", kwargs={"vacancy_id": vacancy_id}))
    except:
        return redirect('/vacancy_list')

def cancel(request, student_id, vacancy_id):
    try:
        vacancy = VacancyList.objects.get(id=vacancy_id)
        respond = Vacancy_respond.objects.get(student_id=student_id, vacancy_id=vacancy)
        if respond.vacancy_status == 1:
            vacancy.amount = vacancy.amount + 1
            vacancy.save()
        respond.vacancy_status = 0
        respond.save()
        return HttpResponseRedirect(reverse("view_respond", kwargs={"vacancy_id": vacancy_id}))
    except:
        return redirect('/vacancy_list')
