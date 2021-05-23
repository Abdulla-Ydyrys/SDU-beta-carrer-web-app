
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.contrib import messages
from sdu_beta_web_app.models import *
from django.core.files.storage import FileSystemStorage


def company_home(request):
    return render(request, "company_template/home.html")

def company_profile(request):
    user = CustomUser.objects.get(id=request.user.id)
    return render(request, "company_template/company_profile.html", {"user": user})

def edit_company_profile(request):
    user = CustomUser.objects.get(id=request.user.id)
    return render(request, "company_template/edit_profile.html", {"user": user})

def update_company_profile(request):
    if request.method != "POST":
        return HttpResponseRedirect(reverse("company_profile"))
    else:
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
            user = CustomUser.objects.get(id=request.user.id)
            user.username = username
            user.first_name = first_name
            user.last_name = last_name
            user.save()
            company = Company.objects.get(company=request.user.id)
            if picture_url is not None:
                company.display_image = picture_url
            company.address = address
            company.save()
            messages.success(request, "Company profile updated successfully")
            return HttpResponseRedirect(reverse("company_profile"))
        except:
            messages.error(request, "Failed to update Company profile")
            return HttpResponseRedirect(reverse("company_profile"))

def my_interns(request):
    supervisor = CustomUser.objects.get(id=request.user.id)
    if supervisor.company.in_whitelist == True:
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
        return render(request, "company_template/my_interns.html", {"reg": reg, "grades_list": grades_list, "studentList": studentList})
    else:
        messages.error(request, "Your account is pending approval. Please be patient till your admin adds your company to the whitelist.")
        return HttpResponseRedirect(reverse("company_home"))

def company_grade(request):
    if request.method != "POST":
        return HttpResponseRedirect(reverse("my_interns"))
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
            return HttpResponseRedirect(reverse("my_interns"))
        except:
            messages.error(request, "Failed to set grades")
            return HttpResponseRedirect(reverse("my_interns"))

def company_feedback(request):
    company_id = Company.objects.get(company=request.user.id)
    feedbacks = Company_feedback.objects.filter(company_id=company_id)
    return render(request, "company_template/company_feedback.html", {"feedbacks": feedbacks})

def save_company_feedback(request):
    if request.method != "POST":
        return HttpResponseRedirect(reverse("company_feedback"))
    else:
        feedback_message = request.POST.get("feedback")
        company_id = Company.objects.get(company=request.user.id)
        try:
            feedback = Company_feedback(company_id=company_id, feedback_message=feedback_message, feedback_reply="")
            feedback.save()
            messages.success(request, "Feedback sent successfully")
            return HttpResponseRedirect(reverse("company_feedback"))
        except:
            messages.error(request, "Failed to send Feedback")
            return HttpResponseRedirect(reverse("company_feedback"))

def add_company_vacancy(request):
    supervisor = CustomUser.objects.get(id=request.user.id)
    if supervisor.company.in_whitelist == True:
        return render(request, "company_template/add_vacancy.html")
    else:
        messages.error(request, "Your account is pending approval. Please be patient till your admin adds your company to the whitelist.")
        return HttpResponseRedirect(reverse("company_home"))

def vacancy_lists(request):
    supervisor = CustomUser.objects.get(id=request.user.id)
    if supervisor.company.in_whitelist == True:
        vacancies = VacancyList.objects.filter(supervisor=supervisor)
        return render(request, "company_template/vacancy_list.html", {"vacancies": vacancies})
    else:
        messages.error(request, "Your account is pending approval. Please be patient till your admin adds your company to the whitelist.")
        return HttpResponseRedirect(reverse("company_home"))

def save_company_vacancy(request):
    if request.method != "POST":
        return HttpResponseRedirect(reverse("vacancy_lists"))
    else:
        name = request.POST.get("vacancy_name")
        requirements = request.POST.get("requirements")
        amount = request.POST.get("amount")
        supervisor = CustomUser.objects.get(id=request.user.id)
        try:
            vacancy = VacancyList(vacancy_name=name, requirements=requirements, amount=amount, supervisor=supervisor)
            vacancy.save()
            messages.success(request, "Vacancy has been successfully added")
            return HttpResponseRedirect(reverse("vacancy_lists"))
        except:
            messages.error(request, "Failed to Add Vacancy")
            return HttpResponseRedirect(reverse("add_company_vacancy"))

def edit_company_vacancy(request, vacancy_id):
    supervisor = CustomUser.objects.get(id=request.user.id)
    if supervisor.company.in_whitelist == True:
        try:
            vacancy = VacancyList.objects.get(id=vacancy_id)
            return render(request, "company_template/edit_vacancy.html", {"vacancy": vacancy, "id": vacancy_id})
        except:
            return redirect('/vacancy_lists')
    else:
        messages.error(request, "Your account is pending approval. Please be patient till your admin adds your company to the whitelist.")
        return HttpResponseRedirect(reverse("company_home"))

def update_company_vacancy(request):
    if request.method != "POST":
        return HttpResponseRedirect(reverse("vacancy_lists"))
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
            messages.success(request, "Vacancy updated successfully")
            return HttpResponseRedirect(reverse("vacancy_lists"))
        except:
            messages.error(request, "Failed to update Vacancy")
            return HttpResponseRedirect(reverse("vacancy_lists"))

def delete_company_vacancy(request, vacancy_id):
    supervisor = CustomUser.objects.get(id=request.user.id)
    if supervisor.company.in_whitelist == True:
        try:
            vacancy = VacancyList.objects.get(id=vacancy_id)
            respond = Vacancy_respond.objects.filter(vacancy_id=vacancy)
            respond.delete()
            vacancy.delete()
            messages.success(request, "Vacancy is deleted")
            return HttpResponseRedirect(reverse("vacancy_lists"))
        except:
            messages.error(request, "Vacancy doesn't exist")
            return HttpResponseRedirect(reverse("vacancy_lists"))
    else:
        messages.error(request, "Your account is pending approval. Please be patient till your admin adds your company to the whitelist.")
        return HttpResponseRedirect(reverse("company_home"))

def view_respondent(request, vacancy_id):
    supervisor = CustomUser.objects.get(id=request.user.id)
    if supervisor.company.in_whitelist == True:
        try:
            vacancy = VacancyList.objects.get(id=vacancy_id)
            respond = Vacancy_respond.objects.filter(vacancy_id=vacancy)
            return render(request, "company_template/view_respond.html", {"vacancy": vacancy, "id": vacancy_id, "respond": respond})
        except:
            return redirect('/vacancy_lists')
    else:
        messages.error(request, "Your account is pending approval. Please be patient till your admin adds your company to the whitelist.")
        return HttpResponseRedirect(reverse("company_home"))

def approved(request, student_id, vacancy_id):
    supervisor = CustomUser.objects.get(id=request.user.id)
    if supervisor.company.in_whitelist == True:
        try:
            vacancy = VacancyList.objects.get(id=vacancy_id)
            respond = Vacancy_respond.objects.get(student_id=student_id, vacancy_id=vacancy)
            respond.vacancy_status = 1
            respond.save()
            vacancy.amount = vacancy.amount-1
            vacancy.save()
            return HttpResponseRedirect(reverse("view_respondent", kwargs={"vacancy_id": vacancy_id}))
        except:
            return redirect('/vacancy_lists')
    else:
        messages.error(request, "Your account is pending approval. Please be patient till your admin adds your company to the whitelist.")
        return HttpResponseRedirect(reverse("company_home"))

def rejected(request, student_id, vacancy_id):
    supervisor = CustomUser.objects.get(id=request.user.id)
    if supervisor.company.in_whitelist == True:
        try:
            vacancy = VacancyList.objects.get(id=vacancy_id)
            respond = Vacancy_respond.objects.get(student_id=student_id, vacancy_id=vacancy)
            respond.vacancy_status = 2
            respond.save()
            return HttpResponseRedirect(reverse("view_respondent", kwargs={"vacancy_id": vacancy_id}))
        except:
            return redirect('/vacancy_lists')
    else:
        messages.error(request, "Your account is pending approval. Please be patient till your admin adds your company to the whitelist.")
        return HttpResponseRedirect(reverse("company_home"))

def canceled(request, student_id, vacancy_id):
    supervisor = CustomUser.objects.get(id=request.user.id)
    if supervisor.company.in_whitelist == True:
        try:
            vacancy = VacancyList.objects.get(id=vacancy_id)
            respond = Vacancy_respond.objects.get(student_id=student_id, vacancy_id=vacancy)
            if respond.vacancy_status == 1:
                vacancy.amount = vacancy.amount + 1
                vacancy.save()
            respond.vacancy_status = 0
            respond.save()
            return HttpResponseRedirect(reverse("view_respondent", kwargs={"vacancy_id": vacancy_id}))
        except:
            return redirect('/vacancy_lists')
    else:
        messages.error(request, "Your account is pending approval. Please be patient till your admin adds your company to the whitelist.")
        return HttpResponseRedirect(reverse("company_home"))