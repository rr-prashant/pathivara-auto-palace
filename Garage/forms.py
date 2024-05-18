from django.forms import ModelForm
from .models import *



class UpdateSuppliersForm(ModelForm):
    class Meta:
        model = Supplier
        fields = '__all__'

class AddSupplierForm(ModelForm):
    class Meta:
        model = Supplier
        fields = '__all__'

class AddStockForm(ModelForm):
    class Meta:
        model = Stock
        fields = '__all__'

class AddDebentureForm(ModelForm):
    class Meta:
        model = Debenture
        fields = ['Name', 'Debenture_type', 'Amount', 'Remarks']

class UpdateStocksForm(ModelForm):
    class Meta:
        model = Stock
        fields = ['Part_Name', 'Part_Quantity', 'Cost_Price', 'Selling_Price', 'Part_Number']

# class UpdateSalesForm(ModelForm):
#     class Meta:
#         model = Sales
#         fields = ['Part_Name', 'Part_Number', 'Quantity', 'Unit_Price']
