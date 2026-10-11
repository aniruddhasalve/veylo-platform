# Veylo Platform

Veylo helps testers understand how a feature should work, run scenarios, and record release evidence.

The MVP combines an HTML-first workspace with a Django backend and database. It is intentionally small and focused: the product behavior model is more important than a large dashboard.

## MVP features

- Demo project with real feature examples
- Feature catalog for authentication, payments, and search
- Expected outcomes for each feature
- Positive, negative, failure, and empty-state scenarios
- WCAG, OWASP, privacy, payment, and secure-development mappings
- Manual pass, fail, blocked, and not-applicable results
- Django ORM persistence
- JSON endpoints for features and results
- Native HTML, CSS, and JavaScript frontend

## Run locally

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py loaddata fixtures/demo.json
python manage.py runserver 127.0.0.1:8000
```

Open <http://127.0.0.1:8000>.

## Product model

```text
Project
  └── Feature
        └── Scenario
              └── TestResult
```

A project represents a product and build reference. A feature describes the user-facing behavior. A scenario explains how to exercise one state. A result records what happened against a known build.

## Production direction

Before public multi-user hosting, add Django authentication, organization and membership models, project ownership, CSRF-safe result forms, evidence storage, permissions, audit history, background browser execution, reports, and secure deployment settings. The demo data and development secret are not production credentials.

## License

MIT. See [LICENSE](LICENSE).
