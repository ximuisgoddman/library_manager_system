# 引入表单类
from django import forms
# 引入文章模型
from .models import ArticlePost
from django import forms
from mdeditor.fields import MDTextFormField


# 写文章的表单类
class ArticlePostForm(forms.ModelForm):
    # name = forms.CharField()

    class Meta:
        # 指明数据模型来源
        model = ArticlePost
        # 定义表单包含的字段
        fields = ('title', 'tags', 'avatar', 'content')


class MDEditorForm(forms.Form):
    name = forms.CharField()
    content = MDTextFormField()
