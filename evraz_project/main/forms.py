from .models import Plan, WorkShift, Fact
from django.forms import *


class PlanForm(ModelForm):
    class Meta:
        model = Plan
        fields = ['hour', 'action_type', 'profile', 'time', 'volume']

    def __init__(self, *args, **kwargs):
        super(PlanForm, self).__init__(*args, **kwargs)
        self.fields["action_type"].choices = [("", "Действие"), ] + list(self.fields["action_type"].choices)[1:]
        self.fields["profile"].choices = [("", "Профиль"), ] + list(self.fields["profile"].choices)[1:]



class WorkShiftForm(ModelForm):
    class Meta:
        model = WorkShift
        fields = ['type', 'date']
        widgets = {
            'type': Select(attrs={
            }),

            'date': DateInput(attrs={
                'placeholder': 'Дата смены',
                'type': 'date'
            })
        }

    def __init__(self, *args, **kwargs):
        super(WorkShiftForm, self).__init__(*args, **kwargs)
        self.fields["type"].choices = [("", "Тип смены"), ] + list(self.fields["type"].choices)[1:]


class FactForm(ModelForm):
    class Meta:
        model = Fact
        fields = ['production_plan', 'time', 'volume']


PlanFormSet_with_extra = modelformset_factory(
    model=Plan,
    fields=('hour', 'action_type', 'profile', 'time', 'volume'),
    extra=1,
    widgets={},
    form=PlanForm
)

PlanFormSet_without_extra = modelformset_factory(
    model=Plan,
    fields=('hour', 'action_type', 'profile', 'time', 'volume'),
    extra=0,
    widgets={},
    form=PlanForm
)

