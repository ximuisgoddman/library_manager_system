from django import forms
from .models import LotteryPrize


class LotteryForm(forms.ModelForm):
    class Meta:
        model = LotteryPrize

        fields = ('image', 'name', 'percentage')
        labels = {
            'image': '奖品图片',
            'name': "奖品",
            '比例': "percentage",
        }
