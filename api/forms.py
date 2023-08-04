import os

from django import forms


# 自定义文件类型验证
def validate_file_extension(value):
    allowed_extensions = ['.csv', '.yaml', 'yml']
    file_extension = os.path.splitext(value.name)[1].lower()
    if file_extension not in allowed_extensions:
        raise forms.ValidationError("Unsupported file extension. Only .csv and .xlsx files are allowed.")


class TestDataUploadForm(forms.Form):
    file = forms.FileField(
        label='Select a data-driven test case file',
        help_text='Allowed file types: .csv, .yaml, .yml',
        widget=forms.ClearableFileInput(attrs={'multiple': True}),
        # 自定义文件类型验证
        validators=[validate_file_extension]
    )
