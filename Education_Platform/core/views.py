from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate
from .forms import CustomUserCreationForm, CustomAuthenticationForm, ProfileUpdateForm
from .models import Course, Lesson, Enrollment, User, Category, Comment, AdditionalResoursesUrl, CompletedLesson
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.forms import UserChangeForm
from .models import Profile
from django.utils import timezone,  date
from django.contrib.auth.decorators import login_required
def signup_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')  # تغيير إلى الصفحة المناسبة بعد التسجيل
    else:
        form = CustomUserCreationForm()
    return render(request, 'core/signup.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')  # تغيير إلى الصفحة المناسبة بعد تسجيل الدخول
    else:
        form = CustomAuthenticationForm()
    return render(request, 'core/login.html', {'form': form})

# profile page
@login_required
def profile_view(request):
    if request.user.is_authenticated:
        user = request.user
        enrollments = Enrollment.objects.filter(user=user)
        return render(request, 'core/profile.html', {'user': user, 'enrollments': enrollments})
    else:
        return redirect('login')  # تغيير إلى صفحة تسجيل الدخول إذا لم يكن المستخدم مسجلاً الدخول

# home page
def home_view(request):
    courses = Course.objects.all()
    return render(request, 'core/home.html', {'courses': courses})

# courses page
def courses_view(request):
    courses = Course.objects.all()
    return render(request, 'core/courses.html', {'courses': courses})

@login_required
def update_profile(request):
    if request.method == 'POST':
        # تحديث البيانات الأساسية فقط
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        username = request.POST.get('username')
        email = request.POST.get('email')
        bio = request.POST.get('bio')
        
        # التحقق من صحة البيانات
        if not username or not email:
            messages.error(request, 'يرجى ملء جميع الحقول المطلوبة')
            return redirect('update_profile')
        
        # التحقق من عدم تكرار اسم المستخدم
        if User.objects.filter(username=username).exclude(id=request.user.id).exists():
            messages.error(request, 'اسم المستخدم مستخدم بالفعل')
            return redirect('update_profile')
        
        # التحقق من عدم تكرار البريد الإلكتروني
        if User.objects.filter(email=email).exclude(id=request.user.id).exists():
            messages.error(request, 'البريد الإلكتروني مستخدم بالفعل')
            return redirect('update_profile')
        
        # تحديث بيانات المستخدم
        user = request.user
        user.first_name = first_name
        user.last_name = last_name
        user.username = username
        user.email = email
        user.save()
        
        # تحديث الملف الشخصي
        # التحقق من وجود ملف شخصي للمستخدم
        try:
            # البحث عن ملف شخصي مرتبط بالمستخدم
            profile = Profile.objects.get(user=user)
        except Profile.DoesNotExist:
            # إنشاء ملف شخصي جديد إذا لم يكن موجودًا
            profile = Profile(user=user)
        
        profile.bio = bio
        
        # تحديث الصورة الشخصية إذا تم تحميلها
        if 'profile_picture' in request.FILES:
            profile.profile_picture = request.FILES['profile_picture']
        
        profile.save()
        
        # تحديث العلاقة بين المستخدم والملف الشخصي
        user.Profile = profile
        user.save()
        
        messages.success(request, 'تم تحديث الملف الشخصي بنجاح')
        return redirect('profile')
    
    return render(request, 'core/update_profile.html')


@login_required
def course_detail(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    lessons = course.lessons.all().order_by('id')
    
    # التحقق مما إذا كان المستخدم مسجلاً في الدورة
    is_enrolled = False
    enrollment = None
    if request.user.is_authenticated:
        try:
            enrollment = Enrollment.objects.get(user=request.user, course=course)
            is_enrolled = True
        except Enrollment.DoesNotExist:
            pass
    
    # الحصول على التعليقات
    comments = course.comments.all().order_by('-created_at')
    
    context = {
        'course': course,
        'lessons': lessons,
        'is_enrolled': is_enrolled,
        'enrollment': enrollment,
        'comments': comments,
    }
    
    return render(request, 'core/course_detail.html', context)

@login_required
def lesson_detail(request, course_id, lesson_id):
    course = get_object_or_404(Course, id=course_id)
    lesson = get_object_or_404(Lesson, id=lesson_id, course=course)
    
    # التحقق مما إذا كان المستخدم مسجلاً في الدورة
    try:
        enrollment = Enrollment.objects.get(user=request.user, course=course)
    except Enrollment.DoesNotExist:
        messages.error(request, 'يجب عليك التسجيل في الدورة أولاً للوصول إلى الدروس.')
        return redirect('course_detail', course_id=course_id)
    
    # الحصول على الدروس الأخرى في الدورة
    lessons = course.lessons.all().order_by('id')
    
    # الحصول على الروابط الإضافية للدورة
    additional_urls = AdditionalResoursesUrl.objects.filter(cuorse=course)
    
    context = {
        'course': course,
        'lesson': lesson,
        'lessons': lessons,
        'enrollment': enrollment,
        'additional_urls': additional_urls,
    }
    
    return render(request, 'core/lesson_detail.html', context)

@login_required
def enroll_course(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    
    # التحقق مما إذا كان المستخدم مسجلاً بالفعل
    if Enrollment.objects.filter(user=request.user, course=course).exists():
        messages.info(request, 'أنت مسجل بالفعل في هذه الدورة.')
    else:
        # إنشاء تسجيل جديد
        enrollment = Enrollment(user=request.user, course=course)
        enrollment.save()
        
        # إضافة المستخدم إلى قائمة الطلاب في الدورة
        course.students.add(request.user)
        
        messages.success(request, 'تم تسجيلك بنجاح في الدورة.')
    
    return redirect('course_detail', course_id=course_id)


@login_required
def add_comment(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    
    # التحقق مما إذا كان المستخدم مسجلاً في الدورة
    try:
        enrollment = Enrollment.objects.get(user=request.user, course=course)
    except Enrollment.DoesNotExist:
        messages.error(request, 'يجب عليك التسجيل في الدورة أولاً لإضافة تعليق.')
        return redirect('course_detail', course_id=course_id)
    
    if request.method == 'POST':
        content = request.POST.get('content')
        
        if content:
            # إنشاء تعليق جديد - تأكد من استخدام الأسماء الصحيحة للحقول
            comment = Comment(
                user=request.user,
                course=course,  # تأكد من أن هذا الاسم يتطابق مع اسم الحقل في نموذج Comment
                content=content,
                created_at=timezone.now()
            )
            comment.save()
            messages.success(request, 'تم إضافة تعليقك بنجاح.')
        else:
            messages.error(request, 'لا يمكن إضافة تعليق فارغ.')
    
    return redirect('course_detail', course_id=course_id)


@login_required
def add_comment(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    
    # التحقق مما إذا كان المستخدم مسجلاً في الدورة
    try:
        enrollment = Enrollment.objects.get(user=request.user, course=course)
    except Enrollment.DoesNotExist:
        messages.error(request, 'يجب عليك التسجيل في الدورة أولاً لإضافة تعليق.')
        return redirect('course_detail', course_id=course_id)
    
    if request.method == 'POST':
        content = request.POST.get('content')
        
        if content:
            # إنشاء تعليق جديد - تصحيح اسم الحقل من course إلى Course
            comment = Comment(
                user=request.user,
                Course=course,  # تم تغيير الاسم ليتطابق مع نموذج Comment
                content=content,
                created_at=timezone.now()
            )
            comment.save()
            messages.success(request, 'تم إضافة تعليقك بنجاح.')
        else:
            messages.error(request, 'لا يمكن إضافة تعليق فارغ.')
    
    return redirect('course_detail', course_id=course_id)

@login_required
def mark_lesson_completed(request, course_id, lesson_id):
    course = get_object_or_404(Course, id=course_id)
    lesson = get_object_or_404(Lesson, id=lesson_id, course=course)
    
    # التحقق مما إذا كان المستخدم مسجلاً في الدورة
    try:
        enrollment = Enrollment.objects.get(user=request.user, course=course)
    except Enrollment.DoesNotExist:
        messages.error(request, 'يجب عليك التسجيل في الدورة أولاً لتسجيل إكمال الدرس.')
        return redirect('course_detail', course_id=course_id)
    
    # التحقق مما إذا كان الدرس مكتملاً بالفعل
    completed, created = CompletedLesson.objects.get_or_create(
        user=request.user,
        lesson=lesson,
        enrollment=enrollment
    )
    
    if created:
        # حساب نسبة الإكمال الجديدة
        total_lessons = course.lessons.count()
        completed_lessons = CompletedLesson.objects.filter(
            user=request.user,
            lesson__course=course
        ).count()
        
        # تحديث نسبة الإكمال ف
        if total_lessons > 0:
            enrollment.percentage_completed = (completed_lessons / total_lessons) * 100
            enrollment.save()
        
        messages.success(request, 'تم تسجيل إكمال الدرس بنجاح!')
    else:
        messages.info(request, 'لقد أكملت هذا الدرس بالفعل.')
    
    return redirect('lesson_detail', course_id=course_id, lesson_id=lesson_id)