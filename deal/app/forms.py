from django.contrib.auth import get_user_model
#from .models import Interest,User,Device
from entangled.forms import EntangledModelForm
from multiselectfield import MultiSelectFormField,MultiSelectField
from prettyjson import PrettyJSONWidget
from django import forms
from django.forms import fields, models

'''class UserInterestForm(forms.ModelForm):
    class Meta:
        model = User
        fields='__all__'
    choice=Interest.objects.all()#.values('category_id')
    ch_list=[]
    for ch in choice:
        ch_list.append([ch.category_name,ch.category_name])
    #interest = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple(), choices=ch_list)
    interest = MultiSelectFormField(choices=ch_list)'''

'''class MyModelChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return obj.category_name


class UserInterestForm(forms.ModelForm):
    pos_code = MyModelChoiceField(queryset=Interest.objects.all(), widget=forms.Select(attrs={'class': 'select2_single form-control', 'blank': 'True'}))
  '''  

'''class DeviceModelForm(forms.ModelForm):
    class Meta:
        model=Device
        fields='__all__'
        widgets = {
            'devie': PrettyJSONWidget(),
        }'''


'''class DeviceForm(EntangledModelForm):
    token=forms.CharField()
    #token = fields.RegexField(
        #regex=r'^#[0-9a-f]{256}$',
    #)
    id=forms.CharField()
    #id = fields.RegexField(
        #regex=r'^#[0-9a-f]{20}$',
    #)

    type = fields.ChoiceField(
        choices=[('iOS', "iOS"), ('Android', "Android")],
    )

    #tenant = models.ModelChoiceField(
        #queryset=get_user_model().objects.filter(is_staff=True),
    #)

    class Meta:
        model = Device
        entangled_fields = {'device': ['id', 'token', 'type']}  # fields provided by this form
        untangled_fields = ['userCD']  # these fields are provided by the Product model 
    '''
