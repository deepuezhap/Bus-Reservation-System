from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Bus,Profile



class CreateUserForm(UserCreationForm):
    first_name = forms.CharField(max_length=30,required=True,widget=forms.TextInput(attrs={'class':'form-control'}))
    last_name = forms.CharField(max_length=30,required=True,widget=forms.TextInput(attrs={'class':'form-control'}))
    email = forms.EmailField(required=True,widget=forms.EmailInput(attrs={'class':'form-control'}))
    

    class Meta:
        model = User
        fields = ['username','first_name','last_name','email','password1','password2']

    def __init__(self,*args,**kwargs):
        super(CreateUserForm,self).__init__(*args,**kwargs)

        self.fields['username'].widget.attrs['class']='form-control'
        self.fields['password1'].widget.attrs['class']='form-control'
        self.fields['password2'].widget.attrs['class']='form-control'

class BusOperatorChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return obj.first_name

class BusForm(forms.ModelForm):
    bus_operator = BusOperatorChoiceField(
        queryset=User.objects.filter(groups__name='bus_operator'),
        label='Bus operator'
    )

    class Meta:
        model = Bus
        fields = ['bname', 'source', 'dest', 'nos', 'fare', 'departure_time', 'arrival_time', 'bus_operator']

class ProfileForm(forms.ModelForm):
    user = forms.ModelChoiceField(queryset=User.objects.filter(groups__name='bus_operator'),label = 'user')

    class Meta:
        model = Profile
        fields = ['user','contact']  
	    