from django.db import models



class Complaintdb(models.Model):
    Student_name = models.CharField(max_length=100, null=True, blank=True)
    Room_no = models.CharField(max_length=10, null=True, blank=True)
    Complaint_type = models.CharField(max_length=50, null=True, blank=True)
    Description = models.TextField(null=True, blank=True)
    Reply = models.TextField(null=True, blank=True)
    Status = models.CharField(max_length=20, default="Pending")


