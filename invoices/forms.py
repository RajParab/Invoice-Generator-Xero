from django import forms


class InvoiceForm(forms.Form):
	date=forms.DateField(widget=forms.widgets.DateInput(attrs={'type': 'date'}))
	dueDate=forms.DateField(widget=forms.widgets.DateInput(attrs={'type': 'date'}))

	def __init__(self, reps, *args, **kwargs):
		super(InvoiceForm, self).__init__(*args, **kwargs)
		for i in range(reps):
			self.fields['description']=forms.CharField(max_length=100)
			self.fields['quantity']=forms.IntegerField()
			self.fields['amount_per_unit']=forms.DecimalField(max_digits=20)

