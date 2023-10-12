from django import forms
from .models import LotteryPrize


class LotteryForm(forms.ModelForm):
    file_upload = forms.FileField(required=False)

    class Meta:
        model = LotteryPrize

        fields = ('name', 'percentage')
        labels = {
            'name': "奖品",
            '比例': "percentage",
        }
