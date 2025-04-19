from django.db import models
from django.contrib.auth.models import AbstractUser
from datetime import timedelta


# Adding a custom user model
class User(AbstractUser):
    role = models.CharField(max_length=50, choices=[('student', 'Student'), ('teacher', 'Teacher')], default='student')
    Profile = models.OneToOneField('Profile', on_delete=models.CASCADE, blank=True, null=True, related_name='user_profile')

    def __str__(self):
        return f"{self.username} - {self.role}"
    
# category model
class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.name}"


# Course model
class Course(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    instructor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='courses')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    students = models.ManyToManyField(User, related_name='enrolled_courses', blank=True)
    image = models.ImageField(upload_to='course_images/', blank=True, null=True)
    total_duration = models.DurationField(default=timedelta(seconds=0))
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    average_rating = models.FloatField(default=0.0)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='courses', blank=True, null=True)

    def __str__(self):
        return f"{self.title}"
    
# Lesson model
class Lesson(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='lessons')
    title = models.CharField(max_length=200)
    content = models.TextField()
    document = models.FileField(upload_to='lesson_documents/', blank=True, null=True)
    video = models.FileField(upload_to='lesson_videos/', blank=True, null=True)
    image = models.ImageField(upload_to='lesson_images/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title} - {self.course.title}"
    
# Enrollment model
class Enrollment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='enrollments')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='enrollments')
    enrolled_at = models.DateTimeField(auto_now_add=True)
    percentage_completed = models.FloatField(default=0.0)

    def __str__(self):
        return f"{self.user.username} enrolled in {self.course.title}"
    

# Profile model
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=100)
    bio = models.TextField(blank=True)
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)
    date_of_birth = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"{self.full_name}'s Profile"
    

# comment model
class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    Course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='comments')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username} - {self.content[:20]} - {self.Course.title}"
    
# Additional resourses URL
class AdditionalResoursesUrl(models.Model):
    cuorse = models.ForeignKey(Course,on_delete=models.CASCADE,related_name='urls')
    title = models.CharField(max_length=100)
    url = models.URLField()

    def __str__(self):
        return f"{self.title}"
    

# إضافة نموذج CompletedLesson لتتبع الدروس المكتملة
class CompletedLesson(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='completed_lessons')
    lesson = models.ForeignKey('Lesson', on_delete=models.CASCADE, related_name='completions')
    enrollment = models.ForeignKey('Enrollment', on_delete=models.CASCADE, related_name='completed_lessons')
    completed_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'lesson')  # لضمان عدم تكرار إكمال الدرس للمستخدم نفسه

    def __str__(self):
        return f"{self.user.username} completed {self.lesson.title}"