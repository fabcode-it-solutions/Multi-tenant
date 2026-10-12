"""The published API reference: complete, truthful, and in three languages."""

from __future__ import annotations

import re
from pathlib import Path

from httpx import AsyncClient

from app import main
from app.docs.i18n.general import ERROR_CODES
from app.docs.i18n.operations import OPERATIONS
from app.docs.openapi import build_base_spec, localize, missing_translations

APP_ROOT = Path(__file__).resolve().parents[1] / "app"
# Where error codes are raised. Seeds and the docs catalog are left out: they
# hold plan and branch codes, not error codes.
ERROR_SOURCES = ("api", "core", "services", "middleware")


def _ops(spec: dict) -> list[dict]:
    return [op for item in spec["paths"].values() for op in item.values()]


def _op(spec: dict, operation_id: str) -> dict:
    return next(op for op in _ops(spec) if op["operationId"] == operation_id)


def _raised_codes() -> set[str]:
    patterns = (re.compile(r'code="([a-z_]+)"'), re.compile(r'^\s+code = "([a-z_]+)"', re.M))
    codes: set[str] = set()
    for folder in ERROR_SOURCES:
        for path in (APP_ROOT / folder).rglob("*.py"):
            text = path.read_text()
            for pattern in patterns:
                codes |= set(pattern.findall(text))
    return codes


async def test_everything_the_api_exposes_is_described_in_all_three_languages():
    """The guarantee that keeps the reference from drifting back to
    half-written: a new endpoint, field or parameter without English, Uzbek
    and Russian text fails here, and so does a translation left behind after
    a rename."""
    problems = missing_translations(build_base_spec(main.app))
    assert problems == [], "\n".join(problems)


async def test_every_error_code_the_api_can_raise_is_explained():
    unexplained = _raised_codes() - ERROR_CODES.keys()
    assert unexplained == set(), f"codes with no explanation: {sorted(unexplained)}"


async def test_endpoints_only_list_error_codes_that_really_exist():
    raised = _raised_codes()
    for op_id, entry in OPERATIONS.items():
        for codes in (entry.errors or {}).values():
            assert (
                set(codes) <= raised
            ), f"{op_id} lists codes nothing raises: {set(codes) - raised}"


async def test_operation_ids_are_unique_and_readable():
    ids = [op["operationId"] for op in _ops(build_base_spec(main.app))]
    assert len(ids) == len(set(ids))
    assert not [i for i in ids if "api_v1" in i], "FastAPI's generated ids leaked through"


async def test_validation_errors_are_documented_in_the_envelope_the_api_really_sends():
    """FastAPI documents 422 as `{"detail": [...]}`; this API answers with its
    own envelope. The reference used to describe a body nobody ever receives."""
    base = build_base_spec(main.app)
    assert "HTTPValidationError" not in base["components"]["schemas"]
    for op in _ops(base):
        for status, response in op["responses"].items():
            if status >= "400":
                ref = response["content"]["application/json"]["schema"]["$ref"]
                assert ref.endswith("/ErrorResponse"), (op["operationId"], status)


async def test_access_is_read_off_the_route_guards():
    base = build_base_spec(main.app)

    login = _op(base, "auth_login")
    assert login["x-access"] == "public"
    assert "security" not in login
    assert "401" in login["responses"]  # bad password, from its own codes

    me = _op(base, "auth_me")
    assert me["x-access"] == "authenticated"
    assert "x-permissions" not in me

    assert _op(base, "shop_update_shop")["x-permissions"] == ["tenant.update"]
    assert _op(base, "platform_metrics")["x-access"] == "platform"


async def test_the_roles_named_on_an_endpoint_match_the_permission_sets():
    en = localize(build_base_spec(main.app), "en")

    owner_only = _op(en, "shop_delete_branch")["description"].split("Held by default by:")[1]
    assert "owner" in owner_only
    assert "manager" not in owner_only
    assert "cashier" not in owner_only

    everyone = _op(en, "orders_create_order")["description"].split("Held by default by:")[1]
    assert "cashier" in everyone and "manager" in everyone and "owner" in everyone


async def test_business_error_codes_appear_on_their_endpoint():
    ru = localize(build_base_spec(main.app), "ru")
    conflict = _op(ru, "catalog_create_product")["responses"]["409"]["description"]
    assert "`sku_taken`" in conflict and "`barcode_taken`" in conflict
    assert "артикул" in conflict


async def test_the_spec_is_served_in_each_language(client: AsyncClient):
    specs = {}
    for lang in ("en", "uz", "ru"):
        resp = await client.get("/api/v1/openapi.json", params={"lang": lang})
        assert resp.status_code == 200
        specs[lang] = resp.json()

    login = {lang: specs[lang]["paths"]["/api/v1/auth/login"]["post"] for lang in specs}
    assert login["en"]["summary"] == "Sign in"
    assert login["uz"]["summary"] == "Tizimga kirish"
    assert login["ru"]["summary"] == "Вход"
    assert specs["ru"]["tags"][0]["name"] == "Аутентификация"

    unknown = await client.get("/api/v1/openapi.json", params={"lang": "xx"})
    assert unknown.json()["paths"]["/api/v1/auth/login"]["post"]["summary"] == "Sign in"


async def test_swagger_ui_offers_all_three_languages(client: AsyncClient):
    resp = await client.get("/api/v1/docs")
    assert resp.status_code == 200
    for lang in ("uz", "ru", "en"):
        assert f"/api/v1/openapi.json?lang={lang}" in resp.text
    assert '"urls.primaryName": "O\'zbekcha"' in resp.text
    assert "StandaloneLayout" in resp.text

    russian = await client.get("/api/v1/docs", params={"lang": "ru"})
    assert '"urls.primaryName": "Русский"' in russian.text

    guessed = await client.get("/docs", follow_redirects=False)
    assert guessed.status_code in (301, 302, 307)
    assert guessed.headers["location"].endswith("/api/v1/docs")


async def test_the_reference_can_be_switched_off(monkeypatch):
    monkeypatch.setattr(main.settings, "API_DOCS_ENABLED", False)
    paths = {getattr(route, "path", "") for route in main.create_app().routes}
    assert "/api/v1/docs" not in paths
    assert "/api/v1/openapi.json" not in paths
