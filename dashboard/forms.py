from . models import *
from django import forms



class PortfolioForm(forms.ModelForm):
    
    class Meta:
        model = Portfolio
        widgets = {
          'description': forms.Textarea(attrs={'rows':3, 'cols':15}),
        }
        fields = '__all__'
        
        
        
    
    
    