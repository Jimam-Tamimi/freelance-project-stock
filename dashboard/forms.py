from . models import *
from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column


class PortfolioForm(forms.ModelForm):

    class Meta:
        model = Portfolio
        widgets = {
          'description': forms.Textarea(attrs={'rows':3, 'cols':15}),
        }
        fields = ['name',
                  'description',
                  'live_quotes',
                  'update_every',
                  'default_commission',
                  'cash',
                  'include_cash_balance',
                  'update_cash_balance_with_transaction',                  
                  ]

        
        

class TransactionForm(forms.ModelForm):
    
    # purchase_date = forms.DateTimeField(input_formats=['%d/%m/%Y %H:%M'], required=False)
    
    
    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
        
        
    #     self.helper = FormHelper()
    #     self.helper.layout = Layout(
    #       'symbol',
    #       'transaction_type',
    #         Row(
    #             Column('purchase_date', css_class='form-group col-md-6 mb-0'),
    #             css_class='form-row'
    #         ),
    #         Row(
    #             Column('quantity', css_class='form-group col-md-6 mb-0'),
    #             Column('price', css_class='form-group col-md-6 mb-0'),
    #             css_class='form-row'
    #         ),
    #         'update_cash_balance',

    #         Row(
    #             Column('fees', css_class='form-group col-md-6 mb-0'),
    #             Column('commissions', css_class='form-group col-md-6 mb-0'),
    #             css_class='form-row'
    #         ),
            
    #         'comments',
    #     )
        

    class Meta:
        model = Transaction
        fields = '__all__'
        exclude = ('portfolio',)


        
        
        


        
    
    
    