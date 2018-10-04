from django.db import models
from django.core.validators import RegexValidator

# Create your models here.
class People(models.Model):
    MALE = 'M'
    FEMALE = 'F'
    SEX_CHOICES = (
        (MALE, 'Male'),
        (FEMALE, 'Female'),
        )
    WIFE = 'W'
    OWN_CHILD = 'OC'
    HUSBAND = 'H'
    NOT_IN_FAMILY = 'NIF'
    OTHER_RELATIVE = 'OR'
    UNMARRIED = 'U'
    RELATIONSHIP = (
        (WIFE,'Wife'),
        (OWN_CHILD,'Own-child'),
        (HUSBAND,'Husband'),
        (NOT_IN_FAMILY,'Not-in-family'),
        (OTHER_RELATIVE,'Other-relative'),
        (UNMARRIED,'Unmarried')
        )
    Name = models.CharField(max_length = 50)
    age  = models.IntegerField(blank = True, null = True)
    email = models.EmailField(max_length=120)
    sex = models.CharField(max_length = 1,choices=SEX_CHOICES, blank=True, null=True)
    height = models.IntegerField(blank=True, null = True)
    weight = models.IntegerField(blank = True, null = True)
    relationship = models.CharField(max_length=30, choices=RELATIONSHIP, blank=True, null=True)
    address = models.ForeignKey('Address', on_delete=models.CASCADE)

    def __str__(self):
        return str(self.Name)

    def male(self):
        return People.objects.filter(sex='M')

class Address(models.Model):
    street = models.TextField(max_length = 50)
    city = models.CharField(max_length = 30)
    State = models.CharField(max_length = 20)
    Zip_code = models.CharField(max_length=6, validators=[RegexValidator(r'^\d{ 6 }$')], blank = True, null=True)

    def __str__(self):
        return str(self.State)

