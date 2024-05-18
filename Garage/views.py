from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from . models import *
from datetime import datetime
from django.core.mail import send_mail
from .forms import * 
from django.urls import reverse
from django.http import HttpResponse
from django.contrib import messages
from django.http import JsonResponse


#Customer Homepage view

# def CustomerHomepage(request):
#     infos = Pathivara_infos.objects.all()
#     services = service.objects.all()
#     gallery = Gallery.objects.all()
#     return render(request, "Customer/index.html", locals())


def CustomerHomepage(request):
    infos = Pathivara_infos.objects.all()
    gallery = Gallery.objects.all()
    services = service.objects.all()

    if request.method == 'POST':
        customer_name = request.POST.get('Customer_Name')
        customer_email = request.POST.get('Customer_Email')
        customer_address = request.POST.get('Customer_Address')
        customer_phone = request.POST.get('Customer_PhoneNumber')
        customer_profession = request.POST.get('Customer_Profession')
        preferred_date = request.POST.get('Preferred_Date')
        bike_model = request.POST.get('Bike_Model_Name')
        service_type = request.POST.get('service_type')

        # Create a new ServiceRequest instance
        new_request = ServiceRequest(
            Customer_Name=customer_name,
            Customer_Email=customer_email,
            Customer_Address=customer_address,
            Customer_PhoneNumber=customer_phone,
            Customer_Profession=customer_profession,
            Preferred_Date=preferred_date,
            Bike_Model_Name=bike_model,
            service_type=service_type,
        )
        new_request.save()

        # Send email notification
        subject = f"Greetings from Pathivara Auto Palace - {customer_name}"
        message = f"Dear {customer_name},\n\nBooking request for your {service_type} has been sent. We'll notify you shortly.\n\nThank you."
        from_email = "tests101.quad@gmail.com"  # Replace with your email address
        to_email = customer_email
        send_mail(subject, message, from_email, [to_email])

        # You can also add a success message or any other logic here
        response_data = {'success': True}
        return JsonResponse(response_data)

    return render(request, "Customer/index.html", {'infos': infos, 'gallery': gallery, 'services': services})




# Login and Registration views

def AdminLogin(request):
    if request.method=='POST':
        user= request.POST.get('user')
        pass1 = request.POST.get('password')
        user= authenticate(request, username = user, password = pass1)

        if user is not None:
            if user.is_staff:
                login(request, user)
                return redirect('Admin-Sales')
            else:
                return render(request, 'Login/Admin_Login.html', {'error': 'Invalid user'})
        else:
            return render(request, 'Login/Admin_Login.html', {'error': 'Username or Password incorrect!'})
        
    return render(request, "Login/Admin_Login.html")


def StaffLogin(request):
    if request.method=='POST':
        user= request.POST.get('user')
        pass1 = request.POST.get('password')
        user= authenticate(request, username = user, password = pass1)

        if user is not None:
            login(request,user)
            return redirect('Staff-Sales')
        else:
            return render(request, 'Login/Staff_Login.html', {'error': 'Username or Password incorrect!'})

    return render(request, "Login/Staff_Login.html")


@login_required
def LogoutView(request):
    logout(request)
    return redirect('Admin-Login')

# End Login and Registration views



# Admin-panel views

#Admin Suppliers views

@login_required(login_url='Admin-Login')
def Admin_Suppliers(request):
    suppliers = Supplier.objects.all().order_by('-Date')
    return render(request, "Admin-Suppliers/Supplier.html", locals())

@login_required(login_url='Admin-Login')
def Admin_Suppliers_view(request, pk):
    suppliers = get_object_or_404(Supplier, pk=pk)
    context = {
        'Supplier': suppliers
    }
    return render(request, "Admin-Suppliers/viewSupplier.html", context=context)  

@login_required(login_url='Admin-Login')
def Admin_Add_Suppliers(request):
    if request.method == "POST":
        add_form = AddSupplierForm(data=request.POST)
        if add_form.is_valid():
            add_stock = add_form.save(commit=False)
            add_stock.save()
            return redirect(reverse("Admin-Supplier"))
    else: 
        add_form = AddSupplierForm()

    return render(request, "Admin-Suppliers/AddSupplier.html", {"form": add_form})

@login_required(login_url='Admin-Login')
def Admin_Delete_Supplier(request, pk):
    suppliers = get_object_or_404(Supplier, pk=pk)
    suppliers.delete()
    return redirect(reverse("Admin-Supplier"))

@login_required(login_url='Admin-Login')
def Admin_Update_Supplier(request, pk):
    suppliers = get_object_or_404(Supplier, pk=pk)
    if request.method == "POST":
       updateForm = UpdateSuppliersForm(data=request.POST)
       if updateForm.is_valid():
           suppliers.Supplier_Name = updateForm.data['Supplier_Name']
           suppliers.Address = updateForm.data['Address']
           suppliers.PhoneNumber = updateForm.data['PhoneNumber']
           suppliers.PAN_Number = updateForm.data['PAN_Number']
           suppliers.save()
           return redirect(reverse("Admin-Supplier-view", kwargs={'pk': pk}))
       
    else: 
        updateForm = UpdateSuppliersForm(instance=suppliers)
    
    context = {"form": updateForm}
    return render(request, "Admin-Suppliers/EditSupplier.html", context=context)


@login_required(login_url='Admin-Login')
def Admin_Search_Supplier(request):
    query = request.GET.get('searchSupplier', '')
    if query:
        searchSupplier = Supplier.objects.filter(Supplier_Name__icontains=query)
    else:
        searchSupplier = []
    return render(request, "Admin-Suppliers/searchSupplier.html", {'searchSupplier': searchSupplier})


# Admin Debenture views
@login_required(login_url='Admin-Login')
def Admin_Debenture(request):
    debenture = Debenture.objects.all().order_by('-Date')
    return render(request, "Admin-Debentures/Debentures.html", locals())


@login_required(login_url='Admin-Login')
def Admin_Add_Debenture(request):
    if request.method == "POST":
        add_form = AddDebentureForm(data=request.POST)
        if add_form.is_valid():
            add_debt = add_form.save(commit=False)
            add_debt.save()
            return redirect(reverse("Admin-Debenture"))
    else: 
        add_form = AddDebentureForm()

    return render(request, "Admin-Debentures/AddDebenture.html", {"form": add_form})


@login_required(login_url='Admin-Login')
def Debenture_view(request, pk):
    debenture = get_object_or_404(Debenture, pk=pk)
    context = {
        'debenture': debenture
    }

    try:
        debentures = Debenture.objects.get(id=pk)
    except Debenture.DoesNotExist:
        return HttpResponse("Debenture not found")

    if request.method == "POST":
        try:
            debentures.Name = request.POST.get('Name')
            debentures.Amount = request.POST.get('Amount')
            debentures.Remarks = request.POST.get('Remarks')
            debentures.save()

            
            return redirect(reverse('view_debenture', kwargs={'pk': pk}))
        except:
            return render(request, 'Admin-Debentures/viewDebentures.html', {'error': 'An error occurred'})
    return render(request, "Admin-Debentures/viewDebentures.html", context=context) 


@login_required(login_url='Admin-Login')
def delete_debenture(request, pk):
    debenture = get_object_or_404(Debenture, pk=pk)
    debenture.delete()
    return redirect(reverse("Admin-Debenture"))

@login_required(login_url='Admin-Login')
def Admin_Search_Debenture(request):
    query = request.GET.get('searchDebentures', '')
    if query:
        searchDebentures = Debenture.objects.filter(Name__icontains=query)
    else:
        searchDebentures = []
    return render(request, "Admin-Debentures/searchDebentures.html", {'searchDebentures': searchDebentures})




#Admin Stock views

@login_required(login_url='Admin-Login')
def Admin_Stocks(request):
    stocks = Stock.objects.all().order_by('-Date')
    return render(request, "Admin-Stocks/Stock.html", locals())

@login_required(login_url='Admin-Login')
def Admin_Add_Stocks(request):
    if request.method == "POST":
        add_form = AddStockForm(data=request.POST)
        if add_form.is_valid():
            add_stock = add_form.save(commit=False)
            add_stock.save()
            return redirect(reverse("Admin-Stock"))
    else: 
        add_form = AddStockForm()

    return render(request, "Admin-Stocks/AddStock.html", {"form": add_form})

@login_required(login_url='Admin-Login')
def Admin_Search_Stocks(request):
    query = request.GET.get('searchStocks', '')
    if query:
        searchStocks = Stock.objects.filter(Part_Name__icontains=query)
    else:
        searchStocks = []
    return render(request, "Admin-Stocks/searchStocks.html", {'searchStocks': searchStocks})

@login_required(login_url='Admin-Login')
def Admin_Stocks_View(request, pk):
    stocks = get_object_or_404(Stock, pk=pk)
    context = {
        'stocks': stocks
    }
    return render(request, "Admin-Stocks/viewStock.html", context=context)

@login_required(login_url='Admin-Login')
def Admin_Delete_Stock(request, pk):
    stocks = get_object_or_404(Stock, pk=pk)
    stocks.delete()
    return redirect(reverse("Admin-Stock"))  


@login_required(login_url='Admin-Login')
def Admin_Update_Stock(request, pk):
    stocks = get_object_or_404(Stock, pk=pk)
    if request.method == "POST":
       updateForm = UpdateStocksForm(data=request.POST)
       if updateForm.is_valid():
           stocks.Part_Name = updateForm.data['Part_Name']
           stocks.Part_Quantity = updateForm.data['Part_Quantity']
           stocks.Cost_Price = updateForm.data['Cost_Price']
           stocks.Selling_Price = updateForm.data['Selling_Price']
           stocks.Part_Number = updateForm.data['Part_Number']
           stocks.save()
           return redirect(reverse("Admin-Stock-View", kwargs={'pk': pk}))
       
    else: 
        updateForm = UpdateStocksForm(instance=stocks)
    
    context = {"form": updateForm}
    return render(request, "Admin-Stocks/EditStock.html", context=context)



#Admin Feedback view
@login_required(login_url='Admin-Login')
def Reviews(request):
    reviews = Review.objects.all().order_by('-Date')
    # Check if a date filter is applied
    issued_date = request.GET.get('issued_Date')
    if issued_date:
        try:
            filter_date = datetime.strptime(issued_date, '%Y-%m-%d').date()
            reviews = reviews.filter(Date=filter_date)
        except ValueError:
            # Handle invalid date format if needed
            pass
    return render(request, "Admin-Reviews/Feedback.html", locals())

@login_required(login_url='Admin-Login')
def review_view(request, pk):
    reviews = get_object_or_404(Review, pk=pk)
    context = {
        'Review': reviews
    }

    try:
        review = Review.objects.get(id=pk)
    except Review.DoesNotExist:
        return HttpResponse("JobCard not found")

    if request.method == "POST":
        try:
            review.Follow_up_Status = request.POST.get('followUpStatus')
            review.Feedback = request.POST.get('feedback')
            review.Review_Status = request.POST.get('reviewStatus')
            
            review.save()

            
            return redirect(reverse('view_review', kwargs={'pk': pk}))
        except:
            return render(request, 'Admin-Reviews/viewFeedback.html', {'error': 'An error occurred'})
        
    return render(request, "Admin-Reviews/viewFeedback.html", context=context)    


@login_required(login_url='Admin-Login')
def reviewsearch(request):
    query = request.GET.get('reviewsearch', '')
    if query:
        searchreview = Review.objects.filter(Customer_Name__icontains=query)
    else:
        searchreview = []
    return render(request, "Admin-Reviews/reviewsearch.html", {'searchreview': searchreview})


@login_required(login_url='Admin-Login')
def delete_review(request, pk):
    Reviews = get_object_or_404(Review, pk=pk)
    Reviews.delete()
    return redirect(reverse("Review"))



#Admin Service-Request views

@login_required(login_url='Admin-Login')
def Service(request):
    service = ServiceRequest.objects.all().order_by('-Date')
    issued_date = request.GET.get('issued_Date')
    if issued_date:
        try:
            filter_date = datetime.strptime(issued_date, '%Y-%m-%d').date()
            service = service.filter(Date=filter_date)
        except ValueError:
            # Handle invalid date format if needed
            pass
    return render(request, "Admin-Bookings/Service_Request.html", locals())

@login_required(login_url='Admin-Login')
def Service_view(request, pk):
    service = get_object_or_404(ServiceRequest, pk=pk)

    if request.method == 'POST':
        status = request.POST.get('status')
        service.Order_Status = status
        service.save()
        # Send email notification
        subject = f"Pathivara Auto Palace Service Status - {service.Customer_Name}"
        message = f"Dear {service.Customer_Name},\n\nYour booking request for your vehicle service has been accepted. Please bring your vehicle on your booked day and time.\n\nThank you."
        from_email = "tests101.quad@gmail.com"  # Replace with your email address
        to_email = service.Customer_Email
        send_mail(subject, message, from_email, [to_email])
        return redirect(reverse("viewService", kwargs={'pk': service.pk}))

    context = {
        'service': service
    }
    return render(request, "Admin-Bookings/view_ServiceRequest.html", context=context)


# Admin Sales views

@login_required(login_url='Admin-Login')
def Admin_Sales(request):
    stocks = Stock.objects.all()
    sales = Sales.objects.all().order_by('-Date')

    if request.method == "POST":
        part_number = request.POST.get('part_number')
        part_name_id = request.POST.get('part_id')
        quantity = int(request.POST.get('quantity'))
        price = float(request.POST.get('price'))
        part_name = request.POST.get('part_name')
        
        stock_instance = Stock.objects.get(pk=int(part_name_id))
        
        if stock_instance.Part_Quantity >= quantity:
            sale = Sales.objects.create(
                Part_Number=part_number,
                Part_Name=stock_instance,
                Unit_Price=price,
                Quantity=quantity,
            )
            
            stock_instance.Part_Quantity -= quantity
            stock_instance.save()
            return redirect(reverse('Admin-Sales'))
        
        else:
            messages.warning(request, f"Sorry, You have no stock left for {part_name}")

    # Check if a date filter is applied
    issued_date = request.GET.get('issued_Date')
    if issued_date:
        try:
            filter_date = datetime.strptime(issued_date, '%Y-%m-%d').date()
            sales = sales.filter(Date=filter_date)
        except ValueError:
            # Handle invalid date format if needed
            pass

    return render(request, "Admin-Sales/Sales.html", locals())

# @login_required(login_url='Admin-Login')
# def Admin_Sales(request):
#     stocks = Stock.objects.all()
#     sales = Sales.objects.all().order_by('-Date')

#     if request.method == "POST":
#         part_number = request.POST.get('part_number')
#         part_name_id = request.POST.get('part_id')
#         quantity = int(request.POST.get('quantity'))  # Convert to integer
#         price = float(request.POST.get('price'))
#         part_name = request.POST.get('part_name')  # Convert to float
        
#         stock_instance = Stock.objects.get(pk=int(part_name_id))
        
#         # Check if there's enough stock available before creating the sale
#         if stock_instance.Part_Quantity >= quantity:
#             sale = Sales.objects.create(
#                 Part_Number=part_number,
#                 Part_Name=stock_instance,
#                 Unit_Price=price,
#                 Quantity=quantity,
#             )
            
#             # Update the stock quantity by subtracting the sold quantity
#             stock_instance.Part_Quantity -= quantity
#             stock_instance.save()
#             return redirect(reverse('Admin-Sales'))
        
#         else:
#             messages.warning(request, f"Sorry, You have no stock left for {part_name}")

#     return render(request, "Admin-Sales/Sales.html", locals())


@login_required(login_url='Admin-Login')
def Admin_Sales_View(request, pk):
    sales = get_object_or_404(Sales, pk=pk)
    context = {
        'sales': sales
    }
    return render(request, "Admin-Sales/viewSales.html", context=context)

@login_required(login_url='Admin-Login')
def Admin_Sales_Delete(request, pk):
    sales = get_object_or_404(Sales, pk=pk)
    sales.delete()
    return redirect(reverse("Admin-Sales"))

# @login_required
# def Admin_Update_Sales(request, pk):
#     sales = get_object_or_404(Sales, pk=pk)
#     if request.method == "POST":
#        updateForm = UpdateSalesForm(data=request.POST)
#        if updateForm.is_valid():
#            sales.Part_Name = updateForm.data['Part_Name']
#            sales.Part_Number = updateForm.data['Part_Number']
#            sales.Quantity = updateForm.data['Quantity']
#            sales.Unit_Price = updateForm.data['Price']     
#            sales.save()
#            return redirect(reverse("Admin-Sales-View", kwargs={'pk': pk}))
       
#     else: 
#         updateForm = UpdateSalesForm(instance=sales)
    
#     context = {"form": updateForm}
#     return render(request, "Admin-Sales/EditSales.html", context=context)




# Admin-Jobcard views

@login_required(login_url='Admin-Login')
def Admin_Jobcard(request):
    cards = JobCard.objects.all().order_by('-Date')
    issued_date = request.GET.get('issued_Date')
    if issued_date:
        try:
            filter_date = datetime.strptime(issued_date, '%Y-%m-%d').date()
            cards = cards.filter(Date=filter_date)
        except ValueError:
            # Handle invalid date format if needed
            pass
    return render(request, "Admin-JobCards/JobCard.html", locals())

@login_required(login_url='Admin-Login')
def Admin_Add_Jobcard(request):
    if request.method == "POST":
        try:
            jobcard_number = request.POST.get('jobcard_number')
            Remarks = request.POST.get('Remarks')
            customer_name = request.POST.get('customer_name')
            customer_address = request.POST.get('customer_address')
            customer_phonenumber = request.POST.get('customer_phonenumber')
            customer_email = request.POST.get('customer_email')
            engine_number = request.POST.get('engine_number')
            chasis_number = request.POST.get('chasis_number')
            bike_model = request.POST.get('bike_model')
            registration_number = request.POST.get('registration_number')
            ODO_meter_reading = request.POST.get('ODO_meter_reading')
            service_type = request.POST.get('service_type')
            issued_DateTime = request.POST.get('issued_DateTime')
            DeliveryDateTime = request.POST.get('DeliveryDateTime')
            
            job_card = JobCard.objects.create(
                jobcard_number = jobcard_number,
                Remarks = Remarks,
                customer_name=customer_name,
                customer_address=customer_address,
                customer_phonenumber=customer_phonenumber,
                customer_email=customer_email,
                engine_number=engine_number,
                chasis_number=chasis_number,
                bike_model=bike_model,
                registration_number=registration_number,
                ODO_meter_reading=ODO_meter_reading, 
                service_type=service_type, 
                issued_DateTime=issued_DateTime, 
                DeliveryDateTime=DeliveryDateTime
            )

            feedback = Review.objects.create(Customer_Name=customer_name,
                                             Remarks = Remarks,
                                             Bike_Model= bike_model,
                                             Service_Type = service_type,
                                             Customer_Phonenumber = customer_phonenumber,
                                             registration_number = registration_number)

            return redirect(reverse('Admin_StockBill', kwargs={'job_card_id': job_card.id}))
        except:
            return render(request, 'Admin-JobCards/AddJobcard.html', {'error': 'An error occurred'})
    else:
        return render(request, 'Admin-JobCards/AddJobcard.html')
    
@login_required(login_url='Admin-Login')
def Admin_StockBillFormView(request, job_card_id):
    stocks = Stock.objects.all()
    job_card = JobCard.objects.get(id=job_card_id)
    stock_bills = StockBill.objects.filter(job_card=job_card)
    
    if request.method == "POST":
        part_number = request.POST.get('part_number')
        part_name_id = request.POST.get('part_id')
        quantity = int(request.POST.get('quantity'))  # Convert to integer
        price = float(request.POST.get('price'))
        part_name = request.POST.get('part_name')  # Convert to float
        
        stock_instance = Stock.objects.get(pk=int(part_name_id))
        
        # Check if there's enough stock available before creating the sale
        if stock_instance.Part_Quantity >= quantity:
            sale = Sales.objects.create(
                Part_Number=part_number,
                Part_Name=stock_instance,
                Unit_Price=price,
                Quantity=quantity,
            )
            
            # Update the stock quantity by subtracting the sold quantity
            stock_instance.Part_Quantity -= quantity
            stock_instance.save()


            stock_bill = StockBill.objects.create(
            job_card=job_card,
            Part_Number=part_number,
            Part_Name = stock_instance,
            Unit_Price = price,
            Quantity=quantity,
            Total_Amount=price)


            return redirect(reverse('Admin_StockBill', kwargs={'job_card_id': job_card_id}))
        
        else:
            messages.warning(request, f"Sorry, You have no stock left for {part_name}")

    context = {
        'stocks': stocks,
        'job_card': job_card,
        'stock_bills': stock_bills,
    }
    
    return render(request, 'Admin-JobCards/stockbill_form.html', context)

@login_required(login_url='Admin-Login')
def Admin_Jobcard_View(request, pk):
    card = JobCard.objects.get(id=pk)
    stock_bills = StockBill.objects.filter(job_card=card)
    stocks = Stock.objects.all()

    if request.method == "POST":
        part_number = request.POST.get('part_number')
        part_name_id = request.POST.get('part_id')
        quantity = int(request.POST.get('quantity'))  # Convert to integer
        price = float(request.POST.get('price'))
        part_name = request.POST.get('part_name')  # Convert to float
        
        stock_instance = Stock.objects.get(pk=int(part_name_id))
        job_card = JobCard.objects.get(id=pk)
        
        # Check if there's enough stock available before creating the sale
        if stock_instance.Part_Quantity >= quantity:
            sale = Sales.objects.create(
                Part_Number=part_number,
                Part_Name=stock_instance,
                Unit_Price=price,
                Quantity=quantity,
            )
            
            # Update the stock quantity by subtracting the sold quantity
            stock_instance.Part_Quantity -= quantity
            stock_instance.save()


            stock_bill = StockBill.objects.create(
            job_card=job_card,
            Part_Number=part_number,
            Part_Name = stock_instance,
            Unit_Price = price,
            Quantity=quantity,
            Total_Amount=price)


            return redirect(reverse('Admin-JobCard-View', kwargs={'pk': pk}))
        
        else:
            messages.warning(request, f"Sorry, You have no stock left for {part_name}")

    context = {
        'cards': card,
        'stocks': stocks,
        'stock_bills': stock_bills
    }

    return render(request, "Admin-JobCards/viewJobcard.html", context=context)

@login_required(login_url='Admin-Login')
def Admin_Delete_Jobcard(request, pk):
    card = get_object_or_404(JobCard, pk=pk)
    card.delete()
    return redirect(reverse("Admin-JobCards"))


@login_required(login_url='Admin-Login')
def Admin_Update_JobCard(request, pk):
    try:
        job_card = JobCard.objects.get(id=pk)
    except JobCard.DoesNotExist:
        return HttpResponse("JobCard not found")

    if request.method == "POST":
        try:
            job_card.customer_name = request.POST.get('customer_name')
            job_card.customer_address = request.POST.get('customer_address')
            job_card.customer_phonenumber = request.POST.get('customer_phonenumber')
            job_card.customer_email = request.POST.get('customer_email')
            job_card.engine_number = request.POST.get('engine_number')
            job_card.chasis_number = request.POST.get('chasis_number')
            job_card.bike_model = request.POST.get('bike_model')
            job_card.registration_number = request.POST.get('registration_number')
            job_card.ODO_meter_reading = request.POST.get('ODO_meter_reading')
            job_card.service_type = request.POST.get('service_type')
            job_card.issued_DateTime = request.POST.get('issued_DateTime')
            job_card.DeliveryDateTime = request.POST.get('DeliveryDateTime')

            job_card.save()

            
            return redirect(reverse('Admin-JobCard-View', kwargs={'pk': pk}))
        except:
            return render(request, 'Admin-JobCards/UpdateJobCard.html', {'error': 'An error occurred'})
    else:
        context = {
            'job_card': job_card
        }
        return render(request, 'Admin-JobCards/UpdateJobCard.html', context=context)
    
@login_required(login_url='Admin-Login')
def Admin_Search_JobCards(request):
    query = request.GET.get('searchJobcards', '')
    if query:
        searchJobcards = JobCard.objects.filter(customer_name__icontains=query)
    else:
        searchJobcards = []
    return render(request, "Admin-JobCards/searchJobcards.html", {'searchJobcards': searchJobcards})



# End Admin-panel views



# Staff-Panel views

# Staff Sales views

@login_required(login_url='Staff-Login')
def Staff_Sales(request):
    stocks = Stock.objects.all()
    sales = Sales.objects.all().order_by('-Date')

    if request.method == "POST":
        part_number = request.POST.get('part_number')
        part_name_id = request.POST.get('part_id')
        quantity = int(request.POST.get('quantity'))  # Convert to integer
        price = float(request.POST.get('price'))
        part_name = request.POST.get('part_name')  # Convert to float
        
        stock_instance = Stock.objects.get(pk=int(part_name_id))
        
        # Check if there's enough stock available before creating the sale
        if stock_instance.Part_Quantity >= quantity:
            sale = Sales.objects.create(
                Part_Number=part_number,
                Part_Name=stock_instance,
                Unit_Price=price,
                Quantity=quantity,
            )
            
            # Update the stock quantity by subtracting the sold quantity
            stock_instance.Part_Quantity -= quantity
            stock_instance.save()
            return redirect(reverse('Staff-Sales'))
        
        else:
            messages.warning(request, f"Sorry, You have no stock left for {part_name}")

    issued_date = request.GET.get('issued_Date')
    if issued_date:
        try:
            filter_date = datetime.strptime(issued_date, '%Y-%m-%d').date()
            sales = sales.filter(Date=filter_date)
        except ValueError:
            # Handle invalid date format if needed
            pass

    return render(request, "Staff-Sales/Sales.html", locals())

#Admin & Staff Feedback view
@login_required(login_url='Staff-Login')
def Staff_Reviews(request):
    reviews = Review.objects.all().order_by('-Date')
    issued_date = request.GET.get('issued_Date')
    if issued_date:
        try:
            filter_date = datetime.strptime(issued_date, '%Y-%m-%d').date()
            reviews = reviews.filter(Date=filter_date)
        except ValueError:
            # Handle invalid date format if needed
            pass
    return render(request, "Staff-Reviews/Feedback.html", locals())


@login_required(login_url='Staff-Login')
def Staff_review_view(request, pk):
    reviews = get_object_or_404(Review, pk=pk)
    context = {
        'Review': reviews
    }
    try:
        review = Review.objects.get(id=pk)
    except Review.DoesNotExist:
        return HttpResponse("JobCard not found")

    if request.method == "POST":
        try:
            review.Follow_up_Status = request.POST.get('followUpStatus')
            review.Feedback = request.POST.get('feedback')
            review.Review_Status = request.POST.get('reviewStatus')
            
            review.save()

            
            return redirect(reverse('Staff-view_review', kwargs={'pk': pk}))
        except:
            return render(request, 'Staff-Reviews/viewFeedback.html', {'error': 'An error occurred'})
   
    return render(request, "Staff-Reviews/viewFeedback.html", context=context)    

@login_required(login_url='Staff-Login')
def Staff_reviewsearch(request):
    query = request.GET.get('reviewsearch', '')
    if query:
        searchreview = Review.objects.filter(Customer_Name__icontains=query)
    else:
        searchreview = []
    return render(request, "Staff-Reviews/reviewsearch.html", {'searchreview': searchreview})


# Admin-Jobcard views

@login_required(login_url='Staff-Login')
def Staff_Jobcard(request):
    cards = JobCard.objects.all().order_by('-issued_DateTime')
    issued_date = request.GET.get('issued_Date')
    if issued_date:
        try:
            filter_date = datetime.strptime(issued_date, '%Y-%m-%d').date()
            cards = cards.filter(Date=filter_date)
        except ValueError:
            # Handle invalid date format if needed
            pass
    return render(request, "Staff-JobCards/JobCard.html", locals())

@login_required(login_url='Staff-Login')
def Staff_Add_Jobcard(request):
    if request.method == "POST":
        try:
            jobcard_number = request.POST.get('jobcard_number')
            Remarks = request.POST.get('Remarks')
            customer_name = request.POST.get('customer_name')
            customer_address = request.POST.get('customer_address')
            customer_phonenumber = request.POST.get('customer_phonenumber')
            customer_email = request.POST.get('customer_email')
            engine_number = request.POST.get('engine_number')
            chasis_number = request.POST.get('chasis_number')
            bike_model = request.POST.get('bike_model')
            registration_number = request.POST.get('registration_number')
            ODO_meter_reading = request.POST.get('ODO_meter_reading')
            service_type = request.POST.get('service_type')
            issued_DateTime = request.POST.get('issued_DateTime')
            DeliveryDateTime = request.POST.get('DeliveryDateTime')
            
            job_card = JobCard.objects.create(
                jobcard_number = jobcard_number,
                Remarks = Remarks,
                customer_name=customer_name,
                customer_address=customer_address,
                customer_phonenumber=customer_phonenumber,
                customer_email=customer_email,
                engine_number=engine_number,
                chasis_number=chasis_number,
                bike_model=bike_model,
                registration_number=registration_number,
                ODO_meter_reading=ODO_meter_reading, 
                service_type=service_type, 
                issued_DateTime=issued_DateTime, 
                DeliveryDateTime=DeliveryDateTime
            )

            feedback = Review.objects.create(Customer_Name=customer_name,
                                             Bike_Model= bike_model,
                                             Service_Type = service_type,
                                             Customer_Phonenumber = customer_phonenumber,
                                             registration_number = registration_number)

            return redirect(reverse('Staff_StockBill', kwargs={'job_card_id': job_card.id}))
        except:
            return render(request, 'Staff-JobCards/AddJobcard.html', {'error': 'An error occurred'})
    else:
        return render(request, 'Staff-JobCards/AddJobcard.html')
    
@login_required(login_url='Staff-Login')
def Staff_StockBillFormView(request, job_card_id):
    stocks = Stock.objects.all()
    job_card = JobCard.objects.get(id=job_card_id)
    stock_bills = StockBill.objects.filter(job_card=job_card)
    
    if request.method == "POST":
        part_number = request.POST.get('part_number')
        part_name_id = request.POST.get('part_id')
        quantity = int(request.POST.get('quantity'))  # Convert to integer
        price = float(request.POST.get('price'))
        part_name = request.POST.get('part_name')  # Convert to float
        
        stock_instance = Stock.objects.get(pk=int(part_name_id))
        
        # Check if there's enough stock available before creating the sale
        if stock_instance.Part_Quantity >= quantity:
            sale = Sales.objects.create(
                Part_Number=part_number,
                Part_Name=stock_instance,
                Unit_Price=price,
                Quantity=quantity,
            )
            
            # Update the stock quantity by subtracting the sold quantity
            stock_instance.Part_Quantity -= quantity
            stock_instance.save()


            stock_bill = StockBill.objects.create(
            job_card=job_card,
            Part_Number=part_number,
            Part_Name = stock_instance,
            Unit_Price = price,
            Quantity=quantity,
            Total_Amount=price)


            return redirect(reverse('Staff_StockBill', kwargs={'job_card_id': job_card_id}))
        
        else:
            messages.warning(request, f"Sorry, You have no stock left for {part_name}")

    context = {
        'stocks': stocks,
        'job_card': job_card,
        'stock_bills': stock_bills,
    }
    
    return render(request, 'Staff-JobCards/stockbill_form.html', context)

@login_required(login_url='Staff-Login')
def Staff_Jobcard_View(request, pk):
    card = JobCard.objects.get(id=pk)
    stock_bills = StockBill.objects.filter(job_card=card)
    stocks = Stock.objects.all()

    if request.method == "POST":
        part_number = request.POST.get('part_number')
        part_name_id = request.POST.get('part_id')
        quantity = int(request.POST.get('quantity'))  # Convert to integer
        price = float(request.POST.get('price'))
        part_name = request.POST.get('part_name')  # Convert to float
        
        stock_instance = Stock.objects.get(pk=int(part_name_id))
        job_card = JobCard.objects.get(id=pk)
        
        # Check if there's enough stock available before creating the sale
        if stock_instance.Part_Quantity >= quantity:
            sale = Sales.objects.create(
                Part_Number=part_number,
                Part_Name=stock_instance,
                Unit_Price=price,
                Quantity=quantity,
            )
            
            # Update the stock quantity by subtracting the sold quantity
            stock_instance.Part_Quantity -= quantity
            stock_instance.save()


            stock_bill = StockBill.objects.create(
            job_card=job_card,
            Part_Number=part_number,
            Part_Name = stock_instance,
            Unit_Price = price,
            Quantity=quantity,
            Total_Amount=price)


            return redirect(reverse('Staff-JobCard-View', kwargs={'pk': pk}))
        
        else:
            messages.warning(request, f"Sorry, You have no stock left for {part_name}")

    context = {
        'cards': card,
        'stocks': stocks,
        'stock_bills': stock_bills
    }

    return render(request, "Staff-JobCards/viewJobcard.html", context=context)


@login_required(login_url='Staff-Login')
def Staff_Search_JobCards(request):
    query = request.GET.get('searchJobcards', '')
    if query:
        searchJobcards = JobCard.objects.filter(customer_name__icontains=query)
    else:
        searchJobcards = []
    return render(request, "Staff-JobCards/searchJobcards.html", {'searchJobcards': searchJobcards})




#Admin Service-Request views

@login_required(login_url='Staff-Login')
def Staff_Service(request):
    service = ServiceRequest.objects.all().order_by('-Date')
    issued_date = request.GET.get('issued_Date')
    if issued_date:
        try:
            filter_date = datetime.strptime(issued_date, '%Y-%m-%d').date()
            service = service.filter(Date=filter_date)
        except ValueError:
            # Handle invalid date format if needed
            pass
    return render(request, "Staff-Bookings/Service_Request.html", locals())

@login_required(login_url='Staff-Login')
def Staff_Service_view(request, pk):
    service = get_object_or_404(ServiceRequest, pk=pk)

    if request.method == 'POST':
        status = request.POST.get('status')
        service.Order_Status = status
        service.save()
        # Send email notification
        subject = f"Service Request Status Update - {service.Customer_Name}"
        message = f"Dear {service.Customer_Name},\n\nYour service request status has been updated to: {status}\n\nThank you."
        from_email = "tests101.quad@gmail.com"  # Replace with your email address
        to_email = service.Customer_Email
        send_mail(subject, message, from_email, [to_email])
        return redirect(reverse("Staff-viewService", kwargs={'pk': service.pk}))

    context = {
        'service': service
    }
    return render(request, "Staff-Bookings/view_ServiceRequest.html", context=context)

