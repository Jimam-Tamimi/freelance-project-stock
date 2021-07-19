from . models import *
from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column, ButtonHolder, Submit
from crispy_forms.bootstrap import InlineField

      
class PortfolioForm(forms.ModelForm):
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        
        self.helper = FormHelper()
        self.helper.layout = Layout(
          'name',
          'description',
            Row(
                Column('live_quotes', css_class='form-group col-md-6 mb-0'),
                Column('update_every', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
            
            Row(
                Column('default_commission', css_class='form-group col-md-4 mb-0'),
                Column('cash', css_class='form-group col-md-4 mb-0'),
                Column('currency', css_class='form-group col-md-4 mb-0'),
                css_class='form-row'
            ),

            #  ButtonHolder(
            #     Submit('submit', 'Submit', css_class='button')
            # )          
        )
        self.helper.add_input(Submit('submit', 'Submit', css_class='btn btn-indigo'))
        # self.helper.form_method = 'POST'
        
    
    class Meta:
        model = Portfolio
        widgets = {
          'description': forms.Textarea(attrs={'rows':3, 'cols':15}),
        }
        fields = '__all__'
        exclude = ('user',)
        # fields = ['name',
        #           'description',
        #           'live_quotes',
        #           'update_every',
        #           'default_commission',
        #           'cash',
        #           'currency'
        #           ]

        
        

class TransactionForm(forms.ModelForm):
    
    purchase_date = forms.DateField(widget=forms.DateInput(attrs={'class':'datepicker'}))
    symbol = forms.CharField(widget=forms.TextInput(attrs={'autocomplete':'off'}))
    
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('symbol', css_class='form-group col-md-12 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('transaction_type', css_class='form-group col-md-6 mb-0'),
                Column('quantity', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('purchase_date', css_class='form-group col-md-6 mb-0'),
                Column('price', css_class='form-group col-md-6 mb-0'),
                css_class='align-items-center'
            ),
            'update_cash_balance',
           
             
            

            Row(
                Column('fees', css_class='form-group col-md-6 mb-0'),
                Column('commissions', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
            
            'comments',  
            #  ButtonHolder(
            #     Submit('submit', 'Submit', css_class='button')
            # )          
        )
        self.helper.add_input(Submit('submit', 'Submit', css_class='btn btn-indigo'))
        # self.helper.form_method = 'POST'
        

    class Meta:
        model = Transaction
        fields = '__all__'
        widgets = {
          'comments': forms.Textarea(attrs={'rows':3, 'cols':15}),
        }
        exclude = ('portfolio',)


        
        
        

class WatchlistForm(forms.ModelForm):
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        
        self.helper = FormHelper()
        self.helper.layout = Layout(
          'watchlist_name',
          'watchlist_description',
            Row(
                Column('watchlist_live_quotes', css_class='form-group col-md-6 mb-0'),
                Column('watchlist_update_every', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
                                
        )
        self.helper.add_input(Submit('submit', 'Submit', css_class='btn btn-indigo'))
        
    
    class Meta:
        model = Watchlist
        widgets = {
          'description': forms.Textarea(attrs={'rows':3, 'cols':15}),
        }
        fields = '__all__'
        exclude = ('user',)        
        
    
    


class AddToWatchlistForm(forms.ModelForm):
    
    symbol = forms.CharField(widget=forms.TextInput(attrs={'autocomplete':'off'}))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('symbol', css_class='form-group col-md-12 mb-0'),
                css_class='form-row'
            ),

        )
        self.helper.add_input(Submit('submit', 'Submit', css_class='btn btn-indigo'))
        

    class Meta:
        model = WatchlistStock
        fields = '__all__'
        exclude = ('watchlist',)