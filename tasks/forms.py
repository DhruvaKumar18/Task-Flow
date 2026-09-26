from django import forms
from .models import Task, Category


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = [
            'title',
            'description',
            'category',
            'priority',
            'status',
            'due_date',
        ]
        widgets = {
            'category': forms.Select(
                attrs={
                    'class': 'form-select',
                    'id': 'taskCategorySelect',
                }
            ),

            'title': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'e.g. Implement payment gateway',
                    'autocomplete': 'off',
                    'id': 'taskTitleInput',
                }
            ),
            'description': forms.Textarea(
                attrs={
                    'class': 'form-control',
                    'rows': 4,
                    'placeholder': 'Add task details, checklist, or helpful links...',
                    'id': 'taskDescriptionInput',
                }
            ),
            'priority': forms.Select(
                attrs={
                    'class': 'form-select',
                    'id': 'taskPrioritySelect',
                }
            ),
            'status': forms.Select(
                attrs={
                    'class': 'form-select',
                    'id': 'taskStatusSelect',
                }
            ),
            'due_date': forms.DateInput(
                attrs={
                    'type': 'date',
                    'class': 'form-control',
                    'id': 'taskDueDateInput',
                }
            ),
        }

    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['category'].required = False
        self.fields['category'].empty_label = "-- No Category (Optional) --"
        if user:
            self.fields['category'].queryset = Category.objects.filter(user=user)