from django import forms

class ImageUploadForm(forms.Form):
    image = forms.ImageField(
        label='Select an image', 
        widget=forms.ClearableFileInput(attrs={'class': 'form-control'})
    )
    quality = forms.IntegerField(
        min_value=10, max_value=100, 
        label='Select Compression Quality (10-100)',
        widget=forms.NumberInput(attrs={'class': 'form-range'})
    )
