from django.db import models
import pytz
from datetime import datetime

class Pathivara_infos(models.Model):
    Admin_name = models.CharField(max_length = 100, null = False, blank = False)
    Website_name = models.CharField(max_length = 100, null = True, blank = False)
    Website_desc = models.TextField(null = True, blank = False)
    Admin_phonenumber = models.CharField(max_length = 100, null = True, blank = False)
    Admin_address = models.CharField(max_length = 100, null = True, blank = False)
    Admin_email = models.CharField(max_length = 100, null = True, blank = False)
    Opening_hours = models.CharField(max_length = 100, null = True, blank = False)
    copyright = models.CharField(max_length = 100, null = True, blank = False)
    Service_desc = models.CharField(max_length = 1000, null = True, blank = False)
    facebook_link = models.CharField(max_length = 500, null = True, blank = False)
    googlemap_link = models.CharField(max_length = 500, null = True, blank = False)

    def __str__(self) ->str:
        return self.Admin_name
    
class service(models.Model):
    service_icon = models.ImageField(null=False, blank=False)
    service_title = models.CharField(max_length=100, null=False, blank=False)
    
    def __str__(self):
        return self.service_title
    
class Gallery(models.Model):
    Picture = models.ImageField(null=False, blank=False)



class Supplier(models.Model):
    Supplier_Name = models.CharField(max_length = 100, null = False, blank = False)
    Address = models.CharField(max_length = 100, null = False, blank = False)
    PhoneNumber = models.CharField(max_length = 100, null = False, blank = False)
    PAN_Number = models.CharField(max_length = 100, null = False, blank = False, unique=True)
    Date = models.DateField(auto_now_add=True, blank=True)

    def __str__(self) ->str:
        return self.Supplier_Name
    

class Stock(models.Model):
    Part_Name = models.CharField(max_length = 100, null = False, blank = False)
    Part_Quantity = models.PositiveIntegerField(null = False, blank= False)
    Cost_Price = models.FloatField(null = False, blank= False)
    Selling_Price = models.FloatField(null = False, blank= False)
    Part_Number = models.CharField(max_length = 100, null = False, blank = False)
    Supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE, blank= False)
    Date = models.DateField(auto_now_add=True, blank=True, null=True)


    def __str__(self) ->str:
        return self.Part_Name
    

class Sales(models.Model):
    Part_Name = models.ForeignKey(Stock, on_delete=models.CASCADE, blank= False)
    Part_Number = models.CharField(max_length = 100, null = False, blank = False)
    Unit_Price = models.FloatField(null = False, blank= False)
    Quantity = models.PositiveIntegerField()
    Total_Amount = models.FloatField(null = True, blank= True)
    Date = models.DateField(auto_now_add=True, blank=True, null=True)

    def save(self, *args, **kwargs):
        # Convert quantity and price to appropriate numeric types
        Quantity = int(self.Quantity)
        Unit_Price = float(self.Unit_Price)
        
        # Calculate the price based on the quantity
        self.Total_Amount = Quantity * Unit_Price
        
        super().save(*args, **kwargs)

    def __str__(self) ->str:
        return self.Part_Number
    

class Review(models.Model):
    Customer_Name = models.CharField(max_length = 100, null = False, blank = False)
    Customer_Phonenumber = models.CharField(max_length = 100, null = True, blank = False)
    Bike_Model = models.CharField(max_length = 100, null = False, blank = False)
    Service_Type = models.CharField(max_length = 100, null = False, blank = False)
    Remarks = models.TextField(null = True, blank = True)
    Feedback = models.TextField(null = True, blank = True)
    Status = (
        ('Pending', 'PENDING'),
        ('Review_Done', 'REVIEW_DONE'),
    )
    Followup_Status = (
        ('Pending', 'PENDING'),
        ('Follow_up_Done', 'FOLLOW_UP_DONE'),
    )
    registration_number = models.CharField(max_length = 100, null = True, blank = False)
    Follow_up_Status = models.CharField(max_length = 20, choices= Followup_Status, default= 'Pending', null= True, blank= True)
    Review_Status = models.CharField(max_length = 20, choices= Status, default= 'Pending', null= True, blank= True)
    Date = models.DateField(auto_now_add=True, blank=True)

    def __str__(self) ->str:
        return self.Customer_Name


class ServiceRequest(models.Model):
    Customer_Name = models.CharField(max_length = 100, null = False, blank = False)
    Customer_Email = models.CharField(max_length = 100, null = False, blank = False)
    Customer_PhoneNumber = models.CharField(max_length = 100, null = False, blank = False)
    Customer_Profession = models.CharField(max_length = 100, null = False, blank = False)
    Bike_Model_Name = models.CharField(max_length = 100, null = False, blank = False)
    Preferred_Date = models.DateTimeField(null = True, blank = True)
    Customer_Address = models.CharField(max_length = 100, null = True, blank = True)
    type = (
        ('Paid Service', 'Paid Service'),
        ('Accidental', 'Accidental'),
        ('AMC', 'AMC'),
        ('QRC', 'QRC'),
    )
    service_type = models.CharField(max_length = 20, choices= type, default=' ')
    Status = (
        ('Pending', 'PENDING'),
        ('Request_Accepted', 'REQUEST_ACCEPTED'),
        ('Request_Canceled', 'REQUEST_CANCELED')
    )
    Order_Status = models.CharField(max_length = 20, choices= Status, default= 'Pending', null= True, blank= True)
    Date = models.DateField(verbose_name="DateTime", auto_now_add=True, null= True, blank= True)

    def save(self, *args, **kwargs):
       nepal_tz = pytz.timezone('Asia/Kathmandu')
       current_datetime = datetime.now(pytz.utc).astimezone(nepal_tz)
       self.datetime_field = current_datetime
       super().save(*args, **kwargs)


    def __str__(self) ->str:
        return self.Customer_Name
    

class JobCard(models.Model):
    jobcard_number = models.CharField(max_length = 200, null = True, blank = False, unique=True, editable=True)
    Remarks = models.TextField(null=True, blank= True)
    customer_name = models.CharField(max_length = 200, null = False, blank = False)
    customer_phonenumber = models.CharField(max_length = 200, null = False, blank = False)
    customer_email = models.CharField(max_length = 200, null = False, blank = False)
    customer_address = models.CharField(max_length = 200, null = False, blank = False)
    engine_number = models.CharField(max_length = 200, null = True, blank = True)
    chasis_number = models.CharField(max_length = 200, null = True, blank = True)
    bike_model = models.CharField(max_length = 200, null = False, blank = False)
    registration_number = models.CharField(max_length = 200, null = False, blank = False)
    ODO_meter_reading = models.CharField(max_length = 200, null = False, blank = False)
    type = (
        ('Paid Service', 'Paid Service'),
        ('Accidental', 'Accidental'),
        ('AMC', 'AMC'),
        ('QRC', 'QRC'),
    )
    service_type = models.CharField(max_length = 20, choices= type, default=' ')
    issued_DateTime = models.DateTimeField()
    DeliveryDateTime = models.DateTimeField()
    Date = models.DateField(auto_now_add=True, blank=True)

    def __str__(self):
        return self.customer_name

class StockBill(models.Model):
    job_card = models.ForeignKey(JobCard, on_delete=models.CASCADE, related_name='stock_bills')
    Part_Name = models.ForeignKey(Stock, on_delete=models.CASCADE, blank= False)
    Part_Number = models.CharField(max_length = 200, null = False, blank = False)
    Unit_Price = models.FloatField(null = False, blank= False)
    Quantity = models.PositiveIntegerField()
    Total_Amount = models.FloatField(null = True, blank= True)
    Date = models.DateTimeField(auto_now_add=True, blank=True, null=True)

    def save(self, *args, **kwargs):
        # Convert quantity and price to appropriate numeric types
        Quantity = int(self.Quantity)
        Unit_Price = float(self.Unit_Price)
        
        # Calculate the price based on the quantity
        self.Total_Amount = Quantity * Unit_Price
        
        super().save(*args, **kwargs)

    def __str__(self) ->str:
        return self.Part_Number
    

class Debenture(models.Model):
    Name = models.CharField(max_length = 100, null = False, blank = False)
    type = (
        ('Credit', 'CREDIT'),
        ('Debit', 'DEBIT'),
    )
    Debenture_type = models.CharField(max_length = 20, choices= type, default=' ')
    Amount = models.PositiveIntegerField(null=False, blank=False)
    Date = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    Remarks = models.TextField(null = True, blank = True)

    def __str__(self) ->str:
        return self.Name

