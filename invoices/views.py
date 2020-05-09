from django.shortcuts import render,redirect
from .forms import InvoiceForm
from .XeroAPI import Xero
# Create your views here.



def invoiceView(request):
	xero=Xero()

	
	access_token,refresh_token=xero.XeroRefreshToken(xero.XeroNewRefreshToken())

	tenantID=xero.XeroTenantID(access_token)


	invoice_dict={}
	if request.method=='POST':
		payment_form=InvoiceForm(10,request.POST)

		if payment_form.is_valid():
			date=payment_form.cleaned_data['date']
			dueDate=payment_form.cleaned_data['date']
			description=payment_form.cleaned_data['description']
			quantity=payment_form.cleaned_data['quantity']
			amount_per_unit=payment_form.cleaned_data['amount_per_unit']

			invoice_dict=(request.POST).dict()
		
			invoice_dict['contactID']='537a9fae-753b-47c6-919e-4dee8e8172a0'
			xero.XeroCreateInvoice(access_token,tenantID,invoice_dict)

			return redirect('invoices:success')
	else:
		payment_form=InvoiceForm(10)

	return render(request,'invoiceForm.html',{'payment_form':payment_form})


def success(request):

	return render(request,'success.html',{})

def homepage(request):
	return render(request,'homePage.html',{})