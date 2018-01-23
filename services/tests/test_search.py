from django.test import TestCase
from django.core.exceptions import SuspiciousOperation
from rest_framework import test as rest_test
from rest_framework import status
from services.tests.helpers import ServiceBuilder
from organizations.tests.helpers import OrganizationBuilder
from taxonomies.tests.helpers import TaxonomyTermBuilder
from services.viewsets import SearchParameters

class SearchParametersTests(TestCase):
    def test_can_build_with_taxonomy_id(self):
        parameters = SearchParameters({'taxonomy_term' : 'foo:bar'})
        self.assertEqual(parameters.taxonomy_id, 'foo')

    def test_can_build_with_taxonomy_term(self):
        parameters = SearchParameters({'taxonomy_term' : 'foo:bar'})
        self.assertEqual(parameters.taxonomy_term, 'bar')

    def test_throws_on_too_many_field_separators(self):
        with self.assertRaises(SuspiciousOperation):
            SearchParameters({'taxonomy_term' : 'foo:bar:baz'})

    def test_throws_on_missing_field_separators(self):
        with self.assertRaises(SuspiciousOperation):
            SearchParameters({'taxonomy_term' : 'foobar'})

    def test_throws_on_missing_taxonomy_id(self):
        with self.assertRaises(SuspiciousOperation):
            SearchParameters({'taxonomy_term' : ':bar'})

    def test_throws_on_missing_taxonomy_term(self):
        with self.assertRaises(SuspiciousOperation):
            SearchParameters({'taxonomy_term' : 'foo:'})

class ServicesTaxonomicSearchTests(rest_test.APITestCase):
    def setUp(self):
        self.organization = OrganizationBuilder().build()
        self.organization.save()

    def test_search_with_taxonomic_argument_returns_service(self):
        taxonomy_term = TaxonomyTermBuilder().build()
        taxonomy_term.save()
        service = ServiceBuilder(self.organization).with_taxonomy_terms([taxonomy_term]).build()
        service.save()

        url = '/v1/services/?taxonomy_term={0}:{1}'.format(taxonomy_term.taxonomy_id,
                                                           taxonomy_term.name)
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()), 1)
        self.assertEqual(response.json()[0]['id'], service.id)

    def test_search_with_wrong_taxonomy_id_returns_404(self):
        taxonomy_term = TaxonomyTermBuilder().build()
        taxonomy_term.save()
        wrong_taxonomy_term = TaxonomyTermBuilder().build()
        wrong_taxonomy_term.save()
        ServiceBuilder(self.organization).with_taxonomy_terms([taxonomy_term]).create()

        url = '/v1/services/?taxonomy_term={0}:{1}'.format(wrong_taxonomy_term.taxonomy_id,
                                                           taxonomy_term.name)
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_search_with_wrong_taxonomy_term_returns_404(self):
        taxonomy_term = TaxonomyTermBuilder().build()
        taxonomy_term.save()
        wrong_taxonomy_term = TaxonomyTermBuilder().build()
        wrong_taxonomy_term.save()
        ServiceBuilder(self.organization).with_taxonomy_terms([taxonomy_term]).create()

        url = '/v1/services/?taxonomy_term={0}:{1}'.format(taxonomy_term.taxonomy_id,
                                                           wrong_taxonomy_term.name)
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)