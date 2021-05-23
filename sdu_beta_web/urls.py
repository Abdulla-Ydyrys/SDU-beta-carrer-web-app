"""sdu_beta_web URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from sdu_beta_web_app import views, AdminViews, StaffViews, CompanyViews, StudentViews

urlpatterns = [
    path('', views.showLogin, name="show_login"),
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    path('sign_in', views.signin, name="sign_in"),
    path('sign_up', views.signup, name="sign_up"),
    path('save_user', views.save_user, name="save_user"),
    path('log_out', views.log_out, name="logout"),
    path('activate/<uidb64>/<token>', views.activate, name="activate"),
    # Admin Path
    path('admin_home', AdminViews.admin_home, name="admin_home"),
    path('admin_profile', AdminViews.admin_profile, name="admin_profile"),
    path('edit_admin_profile', AdminViews.edit_admin_profile, name="edit_admin_profile"),
    path('update_admin_profile', AdminViews.update_admin_profile, name="update_admin_profile"),
    path('add_staff', AdminViews.add_staff, name="add_staff"),
    path('save_staff', AdminViews.save_staff, name="save_staff"),
    path('manage_staff', AdminViews.manage_staff, name="manage_staff"),
    path('edit_staff/<str:staff_id>', AdminViews.edit_staff, name="edit_staff"),
    path('update_staff', AdminViews.update_staff, name="update_staff"),
    path('delete_staff/<str:staff_id>', AdminViews.delete_staff, name="delete_staff"),
    path('add_company', AdminViews.add_company, name="add_company"),
    path('save_company', AdminViews.save_company, name="save_company"),
    path('manage_company', AdminViews.manage_company, name="manage_company"),
    path('whitelist', AdminViews.whitelist, name="whitelist"),
    path('edit_company/<str:company_id>', AdminViews.edit_company, name="edit_company"),
    path('update_company', AdminViews.update_company, name="update_company"),
    path('delete_company/<str:company_id>', AdminViews.delete_company, name="delete_company"),
    path('add_student', AdminViews.add_student, name="add_student"),
    path('save_student', AdminViews.save_student, name="save_student"),
    path('manage_student', AdminViews.manage_student, name="manage_student"),
    path('edit_student/<str:student_id>', AdminViews.edit_student, name="edit_student"),
    path('update_student', AdminViews.update_student, name="update_student"),
    path('delete_student/<str:student_id>', AdminViews.delete_student, name="delete_student"),
    path('student_messages', AdminViews.student_messages, name="student_messages"),
    path('staff_messages', AdminViews.staff_messages, name="staff_messages"),
    path('company_messages', AdminViews.company_messages, name="company_messages"),
    path('student_reply', AdminViews.student_reply, name="student_reply"),
    path('staff_reply', AdminViews.staff_reply, name="staff_reply"),
    path('company_reply', AdminViews.company_reply, name="company_reply"),
    path('set_end_date', AdminViews.set_end_date, name="set_end_date"),
    path('manage_registration', AdminViews.manage_registration, name="manage_registration"),
    path('reg_approve/<str:student_id>', AdminViews.reg_approve, name="reg_approve"),
    path('reg_reject/<str:student_id>', AdminViews.reg_reject, name="reg_reject"),
    path('reg_cancel/<str:student_id>', AdminViews.reg_cancel, name="reg_cancel"),
    path('reject_reply', AdminViews.reject_reply, name="reject_reply"),
    path('add_report', AdminViews.add_report, name="add_report"),
    path('save_report', AdminViews.save_report, name="save_report"),
    path('manage_report', AdminViews.manage_report, name="manage_report"),
    path('edit_report/<str:report_id>', AdminViews.edit_report, name="edit_report"),
    path('update_report', AdminViews.update_report, name="update_report"),
    path('delete_report/<str:report_id>', AdminViews.delete_report, name="delete_report"),
    path('view_report/<str:report_id>', AdminViews.view_report, name="view_report"),
    path('set_grade', AdminViews.set_grade, name="set_grade"),
    path('grades', AdminViews.grades, name="grades"),
    path('view_grade/<str:student_id>', AdminViews.view_grade, name="view_grade"),
    path('set_final_grade', AdminViews.set_final_grade, name="set_final_grade"),
    path('reset_final_grade', AdminViews.reset_final_grade, name="reset_final_grade"),
    path('add_post', AdminViews.add_post, name="add_post"),
    path('save_post', AdminViews.save_post, name="save_post"),
    path('manage_post', AdminViews.manage_post, name="manage_post"),
    path('edit_post/<str:post_id>', AdminViews.edit_post, name="edit_post"),
    path('update_post', AdminViews.update_post, name="update_post"),
    path('delete_post/<str:post_id>', AdminViews.delete_post, name="delete_post"),
    path('view_post/<str:post_id>', AdminViews.view_post, name="view_post"),
    path('admin_comment', AdminViews.admin_comment, name="admin_comment"),
    path('delete_comment/<str:comment_id>/<str:post_id>', AdminViews.delete_comment, name="delete_comment"),
    path('export_excel', AdminViews.export_excel, name="export-excel"),
    # Staff Path
    path('staff_home', StaffViews.staff_home, name="staff_home"),
    path('staff_profile', StaffViews.staff_profile, name="staff_profile"),
    path('edit_staff_profile', StaffViews.edit_staff_profile, name="edit_staff_profile"),
    path('update_staff_profile', StaffViews.update_staff_profile, name="update_staff_profile"),
    path('my_students', StaffViews.my_students, name="my_students"),
    path('supervisor_grade', StaffViews.supervisor_grade, name="supervisor_grade"),
    path('vacancy_list', StaffViews.vacancy_list, name="vacancy_list"),
    path('add_vacancy', StaffViews.add_vacancy, name="add_vacancy"),
    path('save_vacancy', StaffViews.save_vacancy, name="save_vacancy"),
    path('edit_vacancy/<str:vacancy_id>', StaffViews.edit_vacancy, name="edit_vacancy"),
    path('update_vacancy', StaffViews.update_vacancy, name="update_vacancy"),
    path('delete_vacancy/<str:vacancy_id>', StaffViews.delete_vacancy, name="delete_vacancy"),
    path('view_respond/<str:vacancy_id>', StaffViews.view_respond, name="view_respond"),
    path('approve/<str:student_id>/<str:vacancy_id>', StaffViews.approve, name="approve"),
    path('reject/<str:student_id>/<str:vacancy_id>', StaffViews.reject, name="reject"),
    path('cancel/<str:student_id>/<str:vacancy_id>', StaffViews.cancel, name="cancel"),
    path('staff_feedback', StaffViews.staff_feedback, name="staff_feedback"),
    path('save_staff_feedback', StaffViews.save_staff_feedback, name="save_staff_feedback"),

    # Company Path
    path('company_home', CompanyViews.company_home, name="company_home"),
    path('company_profile', CompanyViews.company_profile, name="company_profile"),
    path('edit_company_profile', CompanyViews.edit_company_profile, name="edit_company_profile"),
    path('update_company_profile', CompanyViews.update_company_profile, name="update_company_profile"),
    path('my_interns', CompanyViews.my_interns, name="my_interns"),
    path('company_grade', CompanyViews.company_grade, name="company_grade"),
    path('company_feedback', CompanyViews.company_feedback, name="company_feedback"),
    path('save_company_feedback', CompanyViews.save_company_feedback, name="save_company_feedback"),
    path('vacancy_lists', CompanyViews.vacancy_lists, name="vacancy_lists"),
    path('add_company_vacancy', CompanyViews.add_company_vacancy, name="add_company_vacancy"),
    path('save_company_vacancy', CompanyViews.save_company_vacancy, name="save_company_vacancy"),
    path('edit_company_vacancy/<str:vacancy_id>', CompanyViews.edit_company_vacancy, name="edit_company_vacancy"),
    path('update_company_vacancy', CompanyViews.update_company_vacancy, name="update_company_vacancy"),
    path('delete_company_vacancy/<str:vacancy_id>', CompanyViews.delete_company_vacancy, name="delete_company_vacancy"),
    path('view_respondent/<str:vacancy_id>', CompanyViews.view_respondent, name="view_respondent"),
    path('approved/<str:student_id>/<str:vacancy_id>', CompanyViews.approved, name="approved"),
    path('rejected/<str:student_id>/<str:vacancy_id>', CompanyViews.rejected, name="rejected"),
    path('canceled/<str:student_id>/<str:vacancy_id>', CompanyViews.canceled, name="canceled"),

    # Student Path
    path('student_home', StudentViews.student_home, name="student_home"),
    path('student_profile', StudentViews.student_profile, name="student_profile"),
    path('edit_student_profile', StudentViews.edit_student_profile, name="edit_student_profile"),
    path('update_student_profile', StudentViews.update_student_profile, name="update_student_profile"),
    path('student_feedback', StudentViews.student_feedback, name="student_feedback"),
    path('save_feedback', StudentViews.save_feedback, name="save_feedback"),
    path('student_registration', StudentViews.student_registration, name="student_registration"),
    path('confirm_registration', StudentViews.confirm_registration, name="confirm_registration"),
    path('cancel_registration', StudentViews.cancel_registration, name="cancel_registration"),
    path('reports', StudentViews.reports, name="reports"),
    path('report/<str:report_id>', StudentViews.report_detail, name="report_detail"),
    path('submit_report', StudentViews.submit_report, name="submit_report"),
    path('cancel_report', StudentViews.cancel_report, name="cancel_report"),
    path('grades_list', StudentViews.grades_list, name="grades_list"),
    path('posts', StudentViews.posts, name="posts"),
    path('student_comment', StudentViews.student_comment, name="student_comment"),
    path('delete_student_comment/<str:comment_id>/<str:post_id>', StudentViews.delete_student_comment, name="delete_student_comment"),
    path('vacancy', StudentViews.vacancy, name="vacancy"),
    path('respond', StudentViews.respond, name="respond"),
    path('cancel_respond/<str:vacancy_id>', StudentViews.cancel_respond, name="cancel_respond"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

handler404 = 'sdu_beta_web_app.views.error_404'