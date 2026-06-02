from django.db import models
from django.contrib.auth.models import AbstractUser
from  django.db.models.signals import post_save
from django.dispatch import receiver
from django.db.models import Max

# Create your models here.

class User(AbstractUser):
    role_options = [
        ('Student','Student'),
        ('Instructor','Instructor'),
    ]
    role = models.CharField(max_length=50,choices=role_options,default="Student")

class InstructorProfile(models.Model):
    expertise = models.CharField(max_length=100)
    instructor_profile = models.ImageField(upload_to="Instructor_picture",default="profile.jpg")
    about = models.CharField(max_length=500)
    instructor = models.OneToOneField(User,on_delete=models.CASCADE,related_name="instructor_profile")

    def __str__(self):
        return self.instructor.username

# check this -------------------------------------------- 
@receiver(post_save,sender=User)
def create_instructor_profile(sender,instance,created,**kwargs):
    if created and instance.role == 'Instructor':
        InstructorProfile.objects.create(instructor = instance)
# check this -------------------------------------------- 


class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
    
class Course(models.Model):
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=500)
    price = models.DecimalField(max_digits=7,decimal_places=2)
    instructor = models.ForeignKey(User,on_delete=models.CASCADE,related_name="course")
    is_free = models.BooleanField(default=False)
    course_picture = models.ImageField(upload_to="Course_picture")
    thumbnail  = models.TextField()
    category = models.ManyToManyField(Category)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
    
class Module(models.Model):
    title = models.CharField(max_length=100)
    course = models.ForeignKey(Course,on_delete=models.CASCADE,related_name="modules")
    order_number = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.order_number}.{self.title}"
    
    def save(self, *args ,**kwargs):
        max_order = Module.objects.filter(course=self.course).aggregate(max = Max("order_number")).get('max') or 0
        self.order_number=max_order+1
        return super().save(*args,**kwargs)
    
    class Meta :
        ordering = ['order_number']
    

class Lesson(models.Model):
    title = models.CharField(max_length=100)
    module = models.ForeignKey(Module,on_delete=models.CASCADE,related_name="lessons")
    video = models.TextField()
    order_number = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.order_number}.{self.title}"
    
    # look at this max order taking method
    def save(self,*args,**kwargs):
        max_order = Lesson.objects.filter(module=self.module).aggregate(max = Max('order_number')).get('max') or 0
        self.order_number =max_order+ 1
        return super().save(*args,**kwargs)
    
    # to get the order number correctly else added items will be in the order
    class Meta:
        ordering = ['order_number']