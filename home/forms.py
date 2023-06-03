from django import forms


class AddToCartForm(forms.Form):
    quantity = forms.IntegerField(
        min_value=1, widget=forms.NumberInput(attrs={'class': 'form-control'}))


class CouponApplyForm(forms.Form):
    code = forms.CharField(max_length=100, widget=forms.TextInput(
        attrs={'class': 'form-control'}))
