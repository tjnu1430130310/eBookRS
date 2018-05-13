# -*- coding: UTF-8 -*-
from django import forms

class ContactForm(forms.Form):
    subject = forms.CharField(max_length=100)
    email = forms.EmailField(required=False)
    message = forms.CharField(widget=forms.Textarea)

    def clean_message(self):
        # Django 的 form 系统自动寻找匹配的函数方法，该方法名称以 clean_ 开头，并以字段名称结束。 如果有这样的方法，它将在校验时被调用
        message = self.cleaned_data['message']
        num_words = len(message.split())
        if num_words < 4:
            #  如果用户输入字数不足，我们抛出一个 forms.ValidationError 型异常。这个异常的描述会被作为错误列表中的一项显示给用户。
            raise forms.ValidationError("Not enough words!")
        return message