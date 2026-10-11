from django.db import models


class Project(models.Model):
    name = models.CharField(max_length=160)
    slug = models.SlugField(unique=True)
    build_reference = models.CharField(max_length=120, default="local-preview")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Feature(models.Model):
    class Category(models.TextChoices):
        AUTHENTICATION = "authentication", "Authentication"
        PAYMENTS = "payments", "Payments"
        SEARCH = "search", "Search"
        ACCOUNT = "account", "Account"
        GENERAL = "general", "General"

    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="features")
    name = models.CharField(max_length=160)
    slug = models.SlugField()
    category = models.CharField(max_length=32, choices=Category.choices, default=Category.GENERAL)
    summary = models.TextField()
    expected_outcome = models.TextField()
    compliance_controls = models.JSONField(default=list)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order", "id"]
        constraints = [models.UniqueConstraint(fields=["project", "slug"], name="unique_feature_slug_per_project")]


class Scenario(models.Model):
    feature = models.ForeignKey(Feature, on_delete=models.CASCADE, related_name="scenarios")
    title = models.CharField(max_length=180)
    kind = models.CharField(max_length=40, default="happy-path")
    steps = models.JSONField(default=list)
    expected = models.TextField()
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order", "id"]


class TestResult(models.Model):
    class Status(models.TextChoices):
        PASS = "pass", "Pass"
        FAIL = "fail", "Fail"
        BLOCKED = "blocked", "Blocked"
        NOT_APPLICABLE = "not_applicable", "Not applicable"

    scenario = models.ForeignKey(Scenario, on_delete=models.CASCADE, related_name="results")
    build_reference = models.CharField(max_length=120)
    status = models.CharField(max_length=24, choices=Status.choices)
    actual = models.TextField(blank=True)
    evidence_url = models.URLField(blank=True)
    tester = models.CharField(max_length=120, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
