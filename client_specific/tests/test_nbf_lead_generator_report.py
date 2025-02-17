from rest_framework.test import APITestCase, APIRequestFactory

from console.tests.test_user_behaviour import date_to_string
from client_specific.views.nbf_lead_generator_views import LeadGeneratorViewSet
from unittest import mock


def get_current_tenant_name():
    return "lebacpsix"


class TestLeadGeneratorViewSet(APITestCase):
    databases = {"analytics"}
    fixtures = [
        "tests/fixtures/stagelog.json",
    ]

    def setUp(self):
        self.factory = APIRequestFactory()
        self.request = self.factory.post("analytics-new/reports/")
        self.request.data = {
            "timestamp__range": ["2001-01-01T00:00:00Z", "2023-06-30T00:00:00Z"],
            "channel": ["webchat"],
        }
        self.leads = LeadGeneratorViewSet()
        self.pdf_content = "application/pdf"
        self.csv_content = "text/csv"

    @mock.patch(
        "client_specific.services.nbf_lead_generator_utils.get_current_tenant_name",
        side_effect=get_current_tenant_name,
    )
    def test_total_leads(self, mock_middleware):
        result = self.leads.total_leads(self.request)
        self.assertEqual(result.data, {"count": 1})

    @mock.patch(
        "client_specific.services.nbf_lead_generator_utils.get_current_tenant_name",
        side_effect=get_current_tenant_name,
    )
    def test_total_ntb_leads(self, mock_middleware):
        result = self.leads.total_ntb_leads(self.request)
        self.assertEqual(result.data, {"count": 1})

    @mock.patch(
        "client_specific.services.nbf_lead_generator_utils.get_current_tenant_name",
        side_effect=get_current_tenant_name,
    )
    def test_total_etb_leads(self, mock_middleware):
        result = self.leads.total_etb_leads(self.request)
        self.assertEqual(result.data, {"count": 1})

    @mock.patch(
        "client_specific.services.nbf_lead_generator_utils.get_current_tenant_name",
        side_effect=get_current_tenant_name,
    )
    def test_interested_for_call(self, mock_middleware):
        result = self.leads.interested_for_call(self.request)
        self.assertEqual(result.data, {"count": 2})

    @mock.patch(
        "client_specific.services.nbf_lead_generator_utils.get_current_tenant_name",
        side_effect=get_current_tenant_name,
    )
    def test_not_interested_for_call(self, mock_middleware):
        result = self.leads.not_interested_for_call(self.request)
        self.assertEqual(result.data, {"count": 0})

    @mock.patch(
        "client_specific.services.nbf_lead_generator_utils.get_current_tenant_name",
        side_effect=get_current_tenant_name,
    )
    def test_lead_by_products(self, mock_middleware):
        result = self.leads.lead_by_products(self.request)
        formatted_result = date_to_string(result.data, "timestamp")
        actual_output = {
            "count": 2,
            "next": None,
            "previous": None,
            "results": [
                {
                    "channel_id": "d27d56078a7a2f96d4586c3d735a150u",
                    "product": "Suggest Current Account",
                    "status": "NTB",
                    "timestamp": "2023-01-05 10:18:57+00:00",
                },
                {
                    "channel_id": "d27d56078a7a2f96d4586j3d735a150u",
                    "product": "Fixed Deposit",
                    "status": "ETB",
                    "timestamp": "2023-01-05 10:18:57+00:00",
                },
            ],
        }
        self.assertEqual(formatted_result, actual_output)

    @mock.patch(
        "client_specific.services.nbf_lead_generator_utils.get_current_tenant_name",
        side_effect=get_current_tenant_name,
    )
    def test_lead_by_products_export(self, mock_middleware):
        result = self.leads.lead_by_products_export(self.request)
        self.assertEqual(result.get("Content-Type"), self.csv_content)
        self.assertEqual(
            result.get("Content-Disposition"),
            "attachment; filename=lead_by_products.csv",
        )

    @mock.patch(
        "client_specific.services.nbf_lead_generator_utils.get_current_tenant_name",
        side_effect=get_current_tenant_name,
    )
    def test_lead_by_products_export_pdf(self, mock_middleware):
        result = self.leads.lead_by_products_export_pdf(self.request)
        self.assertEqual(result.get("Content-Type"), self.pdf_content)
        self.assertEqual(
            result.get("Content-Disposition"),
            "inline; filename=lead_by_products.pdf",
        )
