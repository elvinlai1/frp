from django.db import models


class Date(models.Model):
    year = models.CharField(max_length=4)
    month = models.CharField(max_length=2)
    day = models.CharField(max_length=2)
    hour = models.CharField(max_length=2)
    minute = models.CharField(max_length=2)


class Employee(models.Model):
    employeeType = models.IntegerField()
    departmentID = models.IntegerField()
    isEmployee = models.BooleanField()
    employeeNumber = models.IntegerField()
    employeePIN = models.IntegerField()
    employeeHourlyRate = models.FloatField()
    employeeTotalHoursPayout = models.FloatField()
    
    #verifyDataAccess() bool
    #setMetaData(array) bool
    #checkClockedHours() float

class Manager(models.Model):
 employeeNumber = models.IntegerField()
 isManager = models.BooleanField()

    #getEmployeeData(employeeNumber) array
    #setEmployeeData(employeeData) bool
    #getDepartmentEmployeeData(deparmentID) bool

class Admin(models.Model):
    employeeNumber = models.IntegerField()
    isAdmin = models.BooleanField()

     #getEmployeeData(employeeNumber) array
     #setEmployeeData(employeeData) bool

        
   








        
    
      