from django.db import models

# Create your models here.
from django.db import models
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.models import AbstractUser, BaseUserManager,PermissionsMixin


class UserManager(BaseUserManager):

    def create_user(self, username, email, password=None, **kwargs):
        
        if username is None:
            raise TypeError('User should have username')
        if email is None:
            raise TypeError('User should have email address')
        if password is None:
            raise TypeError('Password should not be empty')

        user = self.model(username=username, email=self.normalize_email(email), **kwargs)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, username, email, password=None,  **extra_fields):

        if password is None:
            raise TypeError('Password should not be empty')

        user = self.create_user(username, email, password, **extra_fields)
        user.is_superuser = True
        user.save()
        return user
"---------------------------------------------------------------------------------------------------------------------"
class department(models.Model):
    name = models.CharField(max_length = 10)
    def __str__(self):
        return self.name
    
class gender(models.Model):
    name = models.CharField(max_length = 20)
    def __str__(self):
        return self.name
    
class arrears(models.Model):
    count = models.IntegerField()

class studentData(models.Model):
    rollNo =models.CharField(max_length = 50)
    email = models.EmailField(unique=True)
    department = models.ForeignKey(department, on_delete = models.CASCADE, related_name = "department")
    CGPA = models.FloatField()
    gender = models.ForeignKey(gender, on_delete = models.CASCADE, related_name = "gender")
    standing_Arrears = models.ForeignKey(arrears, on_delete = models.CASCADE, related_name = "arrears_standing")
    arrear_history = models.ForeignKey(arrears, on_delete = models.CASCADE, related_name = "arrears_history")
    def __str__(self) :
        return self.rollNo
"---------------------------------------------------------------------------------------------------------------------"
class CIRData(models.Model):
    empId = models.CharField(max_length = 20)
"---------------------------------------------------------------------------------------------------------------------"
class jobPreRequisites(models.Model):
    requisites = models.CharField(max_length=100)

class jobDescription(models.Model):
    role = models.CharField(max_length = 100)
    preRequisites = models.ManyToManyField(jobPreRequisites)

class Qualification(models.Model):
    qualification_name = models.CharField(max_length=20)

class companyData(models.Model):
    companyName = models.CharField(max_length=100)
    companyDescription = models.TextField(null = True)
    jobRole = models.ManyToManyField(jobDescription)
    CGPA_Required = models.FloatField()
    qualification = models.ManyToManyField(Qualification)
    eligibleDepartments = models.ManyToManyField(department)
    CTC = models.CharField(max_length = 20)
    serviceAgreement = models.CharField(max_length=30)
    trainingPeriodandStipend = models.TextField()
    workLocation = models.CharField(max_length = 100)
    evalationProcess = models.TextField() 
    
"---------------------------------------------------------------------------------------------------------------------"
class addUserExcel(models.Model):
    excelFile = models.FileField(upload_to='uploads/')

"---------------------------------------------------------------------------------------------------------------------"
class userRoles(models.Model):
    role = models.CharField(max_length =20,null=True)
    def __str__(self):
        return self.role


class user(AbstractUser,PermissionsMixin):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    email = models.EmailField(max_length=50, unique=True)
    is_active = models.BooleanField(default=True)
    username = models.CharField(max_length=255, unique=True)
    roles= models.ForeignKey(userRoles, on_delete= models.CASCADE, related_name = 'userRole')
    
    objects = UserManager() 
    
    
    first_name = None
    last_name = None
    date_joined=None
    is_staff=None
    last_login=None
    
    def __str__(self):
        return self.email
    
    def tokens(self):
        refresh_token = RefreshToken.for_user(self)
        
        return {
            'refresh_token': str(refresh_token),
            'access_token': str(refresh_token.access_token)
        }


