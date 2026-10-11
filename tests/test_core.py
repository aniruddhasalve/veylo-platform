import json
from django.test import Client, TestCase
from core.models import Feature, Project, Scenario, TestResult


class VeyloWorkflowTests(TestCase):
    def setUp(self):
        project = Project.objects.create(name="Test project", slug="test-project", build_reference="build-1")
        feature = Feature.objects.create(project=project, name="Sign in", slug="sign-in", category="authentication", summary="Sign in safely.", expected_outcome="A valid user gets access.", compliance_controls=["ASVS-5.0-AUTH"])
        self.scenario = Scenario.objects.create(feature=feature, title="Valid sign in", steps=["Enter credentials"], expected="Dashboard opens.")
        self.client = Client()

    def test_features_api_returns_feature_and_scenario(self):
        response = self.client.get("/api/features")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["features"][0]["scenarios"][0]["title"], "Valid sign in")

    def test_result_api_persists_manual_result(self):
        response = self.client.post("/api/results", data=json.dumps({"scenario_id": self.scenario.id, "status": "pass", "actual": "Worked"}), content_type="application/json")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(TestResult.objects.get().status, "pass")

    def test_result_api_rejects_invalid_status(self):
        response = self.client.post("/api/results", data=json.dumps({"scenario_id": self.scenario.id, "status": "unknown"}), content_type="application/json")
        self.assertEqual(response.status_code, 400)
