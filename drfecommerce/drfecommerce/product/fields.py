from django.db import models
from django.core import checks
from django.core.exceptions import ObjectDoesNotExist, ValidationError


class OrderField(models.PositiveIntegerField):

    description = 'Field for ordering within unique filed groups'

    def __init__(self, unique_for_field=None, *args, **kwargs):
        self.unique_for_field = unique_for_field
        super().__init__(*args, **kwargs)

    def check(self, **kwargs):
        return [*super().check(**kwargs),
                *self._check_for_unique_for_field_attr()]

    def _check_for_unique_for_field_attr(self):
        if self.unique_for_field is None:
            return [checks.Error('Insert unique_for_field attribute')]
        elif self.unique_for_field not in [field.name for field in self.model._meta.get_fields()]:
            return [checks.Error('Insert existent unique_for_field attribute')]
        else:
            return []

    def pre_save(self, model_instance, add):

        if getattr(model_instance, self.attname) is None:
            queryset = self.model.objects.all()
            try:
                qs_filter = {self.unique_for_field: getattr(model_instance, self.unique_for_field)}
                query = queryset.filter(**qs_filter)
                last_order = query.latest(self.attname)
                value = getattr(last_order, self.attname) + 1
            except ObjectDoesNotExist:
                value = 1
            return value
        else:
            return super().pre_save(model_instance, add)

    # def get_internal_type(self):
    #     return "OrderField"

    def formfield(self, **kwargs):
        return super().formfield(min_value=1, **kwargs)

    def validate(self, value, model_instance):
        super().validate(value, model_instance)
        # if value < 1:
        #     raise ValidationError('Value equeals 0', 'error1')
        queryset = self.model.objects.all()
        qs_filter = {self.unique_for_field: getattr(model_instance, self.unique_for_field)}
        query = queryset.filter(**qs_filter)
        for i in query:
            if model_instance.id != i.id and value == getattr(i, self.attname):
                raise ValidationError('Duplicate value', 'error2')
