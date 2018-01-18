from common.models import ValidateOnSaveMixin, RequiredCharField
from django.core import validators
from django.db import models
from django.db.models import Q
from organizations.models import Organization
from parler.models import TranslatableModel, TranslatedFields
from taxonomies.models import TaxonomyTerm

class Service(ValidateOnSaveMixin, TranslatableModel):
    id = RequiredCharField(primary_key=True,
                           max_length=200,
                           validators=[validators.validate_slug])

    organization = models.ForeignKey(Organization,
                                     on_delete=models.CASCADE,
                                     related_name='services')

    taxonomy_terms = models.ManyToManyField(TaxonomyTerm,
                                            db_table='services_service_taxonomy_terms')

    translations = TranslatedFields(name=models.CharField(max_length=200),
                                    description=models.TextField(blank=True, null=True))

    def __str__(self):
        return self.name

    @classmethod
    def get_queryset(cls, search_parameters):
        queryset = cls.objects.all()
        queryset = cls.add_taxonomy_filter_if_given(queryset, search_parameters)
        queryset = cls.add_full_text_search_filter_if_given(queryset, search_parameters)
        return queryset

    @staticmethod
    def add_taxonomy_filter_if_given(queryset, search_parameters):
        identifier = search_parameters.taxonomy_id
        term = search_parameters.taxonomy_term

        if identifier and term:
            queryset = queryset.filter(taxonomy_terms__taxonomy_id=identifier,
                                       taxonomy_terms__name=term)
        return queryset

    @staticmethod
    def add_full_text_search_filter_if_given(queryset, search_parameters):
        search_terms = search_parameters.full_text_search_terms

        if not search_terms:
            return queryset

        qs = None
        for term in search_terms:
            if not qs:
                qs = (Q(translations__name__contains=term) |
                      Q(translations__description__contains=term))
            else:
                qs = (qs |
                      Q(translations__name__contains=term) |
                      Q(translations__description__contains=term))

        return queryset.filter(qs)
