from .models import Interest,User
from multiselectfield import MultiSelectFormField,MultiSelectField
from django import forms

class UserInterestForm(forms.ModelForm):
    class Meta:
        model = User
        fields='__all__'
    choice=Interest.objects.all()#.values('category_id')
    ch_list=[]
    for ch in choice:
        ch_list.append([ch.category_name,ch.category_name])
    #interest = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple(), choices=ch_list)
    interest = MultiSelectFormField(choices=ch_list)

'''class MyModelChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return obj.category_name


class UserInterestForm(forms.ModelForm):
    pos_code = MyModelChoiceField(queryset=Interest.objects.all(), widget=forms.Select(attrs={'class': 'select2_single form-control', 'blank': 'True'}))
  '''  


