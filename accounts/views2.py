from accounts import serializers
from accounts.decorators import (admin_required, lecturer_required,
                                 student_required)
from course.models import Course
from django.contrib import messages
from django.contrib.auth import authenticate, login, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.decorators import method_decorator
from django.views import View
from django.views.generic import ListView

# from accounts.forms import (ProfileUpdateForm, StaffAddForm, StudentAddForm,
#                             UserLoginForm, UserSignupForm)


##################################
##################################
##################################


# class IndexView(View):
#     template_name = "index.html"

#     def get(self, request, *args, **kwargs):
#         context = {}
#         return render(request, self.template_name, context)


# class SignupView(View):
#     template_name = "accounts/auth/signup.html"

#     def get(self, request, *args, **kwargs):
#         form = UserSignupForm()
#         context = {'form': form}
#         return render(request, self.template_name, context)

#     def post(self, request, *args, **kwargs):
#         form = UserSignupForm(request.POST)
#         if form.is_valid():
#             user = form.save()
#             user = authenticate(email=form.cleaned_data['email'], password=form.cleaned_data['password1'])
#             login(request, user)
#             return redirect('index')
#         context = {'form': form}
#         return render(request, self.template_name, context)


# class LoginView(View):
#     template_name = "accounts/auth/login.html"

#     def get(self, request, *args, **kwargs):
#         form = UserLoginForm()
#         context = {'form': form}
#         return render(request, self.template_name, context)

#     def post(self, request, *args, **kwargs):
#         form = UserLoginForm(request=request, data=request.POST)
#         if form.is_valid():
#             email = form.cleaned_data.get('username')
#             password = form.cleaned_data.get('password')
#             print(email)
#             user = authenticate(request=request, email=email, password=password)
#             if user is not None:
#                 login(request, user)
#                 return redirect('index')
#         context = {'form': form}
#         return render(request, self.template_name, context)
    

################################################################################
################################################################################

# @login_required
# def profile(request):
#     """ Show profile of any user that fire out the request """
#     try:
#         current_session = get_object_or_404(Session, is_current_session=True)
#         current_semester = get_object_or_404(Semester, is_current_semester=True, session=current_session)
        
#     except Semester.MultipleObjectsReturned and Semester.DoesNotExist and Session.DoesNotExist:
#         raise Http404

#     if request.user.is_lecturer:
#         courses = Course.objects.filter(allocated_course__lecturer__pk=request.user.id).filter(
#             semester=current_semester)
#         return render(request, 'accounts/profile.html', {
#             'title': request.user.get_full_name,
#             "courses": courses,
#             'current_session': current_session,
#             'current_semester': current_semester,
#         })
#     elif request.user.is_student:
#         level = Student.objects.get(student__pk=request.user.id)
#         courses = TakenCourse.objects.filter(student__student__id=request.user.id, course__level=level.level)
#         context = {
#             'title': request.user.get_full_name,
#             'courses': courses,
#             'level': level,
#             'current_session': current_session,
#             'current_semester': current_semester,
#         }
#         return render(request, 'accounts/profile.html', context)
#     else:
#         staff = User.objects.filter(is_lecturer=True)
#         return render(request, 'accounts/profile.html', {
#             'title': request.user.get_full_name,
#             "staff": staff,
#             'current_session': current_session,
#             'current_semester': current_semester,
#         })


# @login_required
# @admin_required
# def profile_single(request, id):
#     """ Show profile of any selected user """
#     if request.user.id == id:
#         return redirect("/profile/")

#     current_session = get_object_or_404(Session, is_current_session=True)
#     current_semester = get_object_or_404(Semester, is_current_semester=True, session=current_session)
#     user = User.objects.get(pk=id)
#     if user.is_lecturer:
#         courses = Course.objects.filter(allocated_course__lecturer__pk=id).filter(semester=current_semester)
#         context = {
#             'title': user.get_full_name,
#             "user": user,
#             "user_type": "Lecturer",
#             "courses": courses,
#             'current_session': current_session,
#             'current_semester': current_semester,
#         }
#         return render(request, 'accounts/profile_single.html', context)
#     elif user.is_student:
#         student = Student.objects.get(student__pk=id)
#         courses = TakenCourse.objects.filter(student__student__id=id, course__level=student.level)
#         context = {
#             'title': user.get_full_name,
#             'user': user,
#             "user_type": "student",
#             'courses': courses,
#             'student': student,
#             'current_session': current_session,
#             'current_semester': current_semester,
#         }
#         return render(request, 'accounts/profile_single.html', context)
#     else:
#         context = {
#             'title': user.get_full_name,
#             "user": user,
#             "user_type": "superuser",
#             'current_session': current_session,
#             'current_semester': current_semester,
#         }
#         return render(request, 'accounts/profile_single.html', context)


# @login_required
# @admin_required
# def admin_panel(request):
#     return render(request, 'setting/admin_panel.html', {})

################################################################################
################################################################################

################################################################################
# Setting views
################################################################################

# @login_required
# def profile_update(request):
#     if request.method == 'POST':
#         form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user)
#         if form.is_valid():
#             form.save()
#             messages.success(request, 'Your profile has been updated successfully.')
#             return redirect('profile')
#         else:
#             messages.error(request, 'Please correct the error(s) below.')
#     else:
#         form = ProfileUpdateForm(instance=request.user)
#     return render(request, 'setting/profile_info_change.html', {
#         'title': 'Setting | Project School',
#         'form': form,
#     })


# @login_required
# def change_password(request):
#     if request.method == 'POST':
#         form = PasswordChangeForm(request.user, request.POST)
#         if form.is_valid():
#             user = form.save()
#             update_session_auth_hash(request, user)
#             messages.success(request, 'Your password was successfully updated!')
#             return redirect('profile')
#         else:
#             messages.error(request, 'Please correct the error(s) below. ')
#     else:
#         form = PasswordChangeForm(request.user)
#     return render(request, 'setting/password_change.html', {
#         'form': form,
#     })


################################################################################
################################################################################


# class StudentAddView(View):
#     template_name = "accounts/student/student-add.html"

#     def get(self, request):
#         form = StudentAddForm()
#         context = {'form': form}
#         return render(request, self.template_name, context)

#     def post(self, request):
#         form = StudentAddForm(request.POST)
#         if form.is_valid():
#             form.save()
#             messages.success(request, f'Account created successfully.')
#         else:
#             messages.error(request, f'Something is not correct, please fill all fields correctly.')
#         context = {'form': form}
#         return render(request, self.template_name, context)
    

# @method_decorator([login_required, admin_required], name='dispatch')
# class StudentListView(ListView):
#     template_name = "accounts/student/student-list.html"
#     paginate_by = 10  # if pagination is desired

#     def get_queryset(self):
#         queryset = Student.objects.all()
#         query = self.request.GET.get('student_id')
#         if query is not None:
#             queryset = queryset.filter(Q(department=query))
#         return queryset

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['title'] = "Students | Project School"
#         return context
    

# @method_decorator([login_required, admin_required], name='dispatch')
# class EditStudentView(View):
#     template_name = "accounts/student/student-edit.html"
#     def get(self, request, *args, **kwargs):
#         pk = kwargs["pk"]
#         instance = get_object_or_404(User, is_student=True, pk=pk)
#         form = ProfileUpdateForm(instance=instance)
#         return render(request, self.template_name, {
#             'title': 'Edit-profile | Project School',
#             'form': form,
#         })

#     def post(self, request, *args, **kwargs):
#         pk = kwargs["pk"]
#         instance = get_object_or_404(User, is_student=True, pk=pk)
#         form = ProfileUpdateForm(request.POST, request.FILES, instance=instance)
#         full_name = instance.get_full_name
#         if form.is_valid():
#             form.save()
#             messages.success(request, ('Student ' + full_name + ' has been updated.'))
#             return redirect('student_list')
#         else:
#             messages.error(request, 'Please correct the error below.')
#             return render(request, self.template_name, {
#                 'title': 'Edit-profile | Project School',
#                 'form': form,
#             })

# @method_decorator([login_required, admin_required], name='dispatch')
# class DeleteStudentView(View):
#     def get(self, request, *args, **kwargs):
#         pk = kwargs["pk"]
#         student = get_object_or_404(Student, pk=pk)
#         student.delete()
#         messages.success(request, 'Student has been deleted.')
#         return redirect('student_list')
