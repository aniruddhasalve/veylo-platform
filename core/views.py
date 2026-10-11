import json
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.http import require_http_methods
from .models import Feature, Project, Scenario, TestResult


def _feature_payload(feature):
    return {"id": feature.id, "name": feature.name, "slug": feature.slug, "category": feature.category, "summary": feature.summary, "expected_outcome": feature.expected_outcome, "compliance_controls": feature.compliance_controls, "scenarios": [{"id": s.id, "title": s.title, "kind": s.kind, "steps": s.steps, "expected": s.expected} for s in feature.scenarios.all()]}


def dashboard(request):
    project = Project.objects.first()
    return render(request, "dashboard.html", {"project": project})


def features_api(request):
    project = Project.objects.first()
    if not project:
        return JsonResponse({"features": []})
    return JsonResponse({"project": {"name": project.name, "build_reference": project.build_reference}, "features": [_feature_payload(feature) for feature in project.features.prefetch_related("scenarios")]})


def feature_api(request, feature_id):
    try:
        feature = Feature.objects.prefetch_related("scenarios").get(id=feature_id)
    except Feature.DoesNotExist:
        return JsonResponse({"detail": "Feature not found"}, status=404)
    return JsonResponse(_feature_payload(feature))


@require_http_methods(["POST"])
def results_api(request):
    try:
        data = json.loads(request.body)
        scenario = Scenario.objects.get(id=data["scenario_id"])
        status = data["status"]
        if status not in {choice[0] for choice in TestResult.Status.choices}:
            raise ValueError("invalid status")
        result = TestResult.objects.create(scenario=scenario, build_reference=data.get("build_reference", scenario.feature.project.build_reference), status=status, actual=data.get("actual", ""), evidence_url=data.get("evidence_url", ""), tester=data.get("tester", ""))
        return JsonResponse({"id": result.id, "status": result.status, "created_at": result.created_at.isoformat()})
    except (KeyError, ValueError, TypeError, json.JSONDecodeError, Scenario.DoesNotExist) as error:
        return JsonResponse({"detail": str(error)}, status=400)
