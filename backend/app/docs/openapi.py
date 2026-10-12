"""The published API reference, in English, Uzbek and Russian.

FastAPI derives the *structure* of the spec from the routes and schemas. This
module layers the prose on top -- summaries, descriptions, parameter and field
explanations, the permission each endpoint checks, the error codes it can
return -- in three languages kept side by side in `app.docs.i18n`.

A test walks the finished spec and fails on anything the API exposes without a
description in all three languages, so the reference cannot drift back to
half-written as endpoints are added.
"""

from __future__ import annotations

import copy
from collections.abc import Iterator
from typing import Any

from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi
from fastapi.routing import APIRoute

from app.api.deps import get_current_user, get_platform_admin
from app.core.permissions import ROLE_PERMISSIONS
from app.docs.i18n.base import LANGS, T
from app.docs.i18n.fields import FIELD_OVERRIDES, FIELDS, PAGE_FIELDS
from app.docs.i18n.general import (
    ACCESS,
    ERROR_CODES,
    INFO_DESCRIPTION,
    INFO_TITLE,
    PAGE_SCHEMA,
    PARAMS,
    ROLE_NAMES,
    SECURITY,
    STATUS,
    TAGS,
)
from app.docs.i18n.operations import OPERATIONS
from app.docs.i18n.schemas import SCHEMAS
from app.models.enums import UserRole
from app.schemas.common import ErrorResponse

API_VERSION = "1.0.0"

_ERROR_BODY = {"application/json": {"schema": {"$ref": "#/components/schemas/ErrorResponse"}}}
# FastAPI's validation-error models describe `{"detail": [...]}`, a body this
# API never sends: its handler answers 422 with the standard error envelope.
_FASTAPI_ERROR_SCHEMAS = ("HTTPValidationError", "ValidationError")
# The roles a shop can grant, in the order the reference names them.
_SHOP_ROLES = (UserRole.CASHIER, UserRole.MANAGER, UserRole.OWNER)
_BLANK = T("", "", "")


def operation_id(route: APIRoute) -> str:
    """`auth_login`, `employees_reset_password`.

    Prefixed with the tag because function names repeat across routers --
    `reset_password` exists in both auth and employees -- and FastAPI's own
    ids (`reset_password_api_v1_auth_reset_password_post`) make unreadable
    method names in any generated client.
    """
    return f"{route.tags[0]}_{route.name}" if route.tags else route.name


def _operations(spec: dict[str, Any]) -> Iterator[dict[str, Any]]:
    for item in spec.get("paths", {}).values():
        yield from item.values()


def _dependency_calls(route: APIRoute) -> list[Any]:
    calls: list[Any] = []
    stack = [route.dependant]
    while stack:
        dependant = stack.pop()
        if dependant.call is not None:
            calls.append(dependant.call)
        stack.extend(dependant.dependencies)
    return calls


def _access(route: APIRoute) -> tuple[str, list[str]]:
    """Who may call a route, read off its dependencies rather than restated by
    hand -- so the reference cannot claim one permission while the code checks
    another."""
    calls = _dependency_calls(route)
    permissions = sorted({p for call in calls for p in getattr(call, "required_permissions", ())})
    if get_platform_admin in calls:
        return "platform", permissions
    if get_current_user in calls:
        return "authenticated", permissions
    return "public", permissions


def build_base_spec(app: FastAPI) -> dict[str, Any]:
    """The language-neutral spec: structure, access, and error responses."""
    routes = [r for r in app.routes if isinstance(r, APIRoute) and r.include_in_schema]
    spec = get_openapi(title=INFO_TITLE.en, version=API_VERSION, routes=routes)
    by_key = {(r.path_format, m.lower()): r for r in routes for m in r.methods}

    schemas = spec.setdefault("components", {}).setdefault("schemas", {})
    for name in _FASTAPI_ERROR_SCHEMAS:
        schemas.pop(name, None)
    schemas["ErrorResponse"] = ErrorResponse.model_json_schema()

    for path, item in spec["paths"].items():
        for method, op in item.items():
            route = by_key[(path, method)]
            op["operationId"] = operation_id(route)
            access, permissions = _access(route)
            op["x-access"] = access
            if permissions:
                op["x-permissions"] = permissions
            _attach_errors(op, access)

    bearer = spec["components"].get("securitySchemes", {}).get("HTTPBearer")
    if bearer is not None:
        bearer["bearerFormat"] = "JWT"
    return spec


def _attach_errors(op: dict[str, Any], access: str) -> None:
    """Every error an operation can answer with, in the envelope it really
    uses. Statuses any endpoint of that kind can return are inferred; the
    specific business codes come from the operation's catalog entry."""
    responses = op.setdefault("responses", {})
    statuses: dict[str, list[str]] = {}
    if access != "public":
        statuses["401"] = []
        statuses["403"] = []
    if any(p.get("in") == "path" for p in op.get("parameters", [])):
        statuses["404"] = []
    if "422" in responses or op.get("parameters") or op.get("requestBody"):
        statuses["422"] = []

    entry = OPERATIONS.get(op["operationId"])
    for status, codes in ((entry.errors or {}) if entry else {}).items():
        statuses.setdefault(str(status), []).extend(codes)

    for status, codes in statuses.items():
        responses[status] = {"description": status, "content": copy.deepcopy(_ERROR_BODY)}
        if codes:
            op.setdefault("x-error-codes", {})[status] = codes
    op["responses"] = dict(sorted(responses.items()))


def localize(base: dict[str, Any], lang: str) -> dict[str, Any]:
    """The base spec with every piece of prose in one language."""
    spec = copy.deepcopy(base)
    spec["info"]["title"] = INFO_TITLE.of(lang)
    spec["info"]["description"] = INFO_DESCRIPTION.of(lang)

    tag_names = {key: name.of(lang) for key, (name, _desc) in TAGS.items()}
    spec["tags"] = [
        {"name": name.of(lang), "description": desc.of(lang)} for name, desc in TAGS.values()
    ]

    for op in _operations(spec):
        entry = OPERATIONS.get(op["operationId"])
        codes = op.get("x-error-codes", {})
        op["summary"] = entry.summary.of(lang) if entry else op["operationId"]
        op["description"] = "\n\n".join(
            part
            for part in ((entry.description.of(lang) if entry else ""), _access_line(op, lang))
            if part
        )
        op["tags"] = [tag_names.get(tag, tag) for tag in op.get("tags", [])]
        for param in op.get("parameters", []):
            param["description"] = PARAMS.get(f"{param['in']}:{param['name']}", _BLANK).of(lang)
        for status, response in op["responses"].items():
            response["description"] = _status_text(status, codes.get(status, []), lang)

    for name, schema in spec["components"]["schemas"].items():
        schema["description"] = (_schema_text(name) or _BLANK).of(lang)
        for field, prop in schema.get("properties", {}).items():
            prop["description"] = (_field_text(name, field) or _BLANK).of(lang)

    bearer = spec["components"].get("securitySchemes", {}).get("HTTPBearer")
    if bearer is not None:
        bearer["description"] = SECURITY.of(lang)
    return spec


def _status_text(status: str, codes: list[str], lang: str) -> str:
    text = STATUS[status].of(lang) if status in STATUS else status
    if codes:
        text += "\n\n" + "\n".join(
            f"- `{code}` — {ERROR_CODES[code].of(lang) if code in ERROR_CODES else ''}"
            for code in codes
        )
    return text


def _access_line(op: dict[str, Any], lang: str) -> str:
    access = op.get("x-access", "public")
    if access != "authenticated":
        return ACCESS[access].of(lang)
    permissions = op.get("x-permissions", [])
    if not permissions:
        return ACCESS["authenticated"].of(lang)
    roles = [
        ROLE_NAMES[role.value].of(lang)
        for role in _SHOP_ROLES
        if set(permissions) <= ROLE_PERMISSIONS[role]
    ]
    return (
        ACCESS["permission"]
        .of(lang)
        .format(
            permissions=", ".join(f"`{p}`" for p in permissions),
            roles=", ".join(roles) if roles else ACCESS["no_role"].of(lang),
        )
    )


def _schema_text(name: str) -> T | None:
    if name.startswith("Page_") and name.endswith("_"):
        item = name[len("Page_") : -1]
        return T(*(PAGE_SCHEMA.of(lang).format(item=item) for lang in LANGS))
    return SCHEMAS.get(name)


def _field_text(schema: str, field: str) -> T | None:
    # Every paginated list shares one envelope; its `total` is a count, not
    # the money `total` an order carries.
    if schema.startswith("Page_"):
        return PAGE_FIELDS.get(field)
    return FIELD_OVERRIDES.get(f"{schema}.{field}") or FIELDS.get(field)


def missing_translations(base: dict[str, Any]) -> list[str]:
    """Everything the spec exposes without text in all three languages, plus
    catalog entries that no longer match anything (a renamed field leaves its
    old translation behind otherwise)."""
    problems: list[str] = []

    def check(label: str, text: T | None) -> None:
        if text is None:
            problems.append(f"no text: {label}")
            return
        problems.extend(f"empty {lang}: {label}" for lang in LANGS if not text.of(lang).strip())

    check("info.title", INFO_TITLE)
    check("info.description", INFO_DESCRIPTION)
    check("security", SECURITY)

    seen_ops: set[str] = set()
    seen_params: set[str] = set()
    seen_fields: set[str] = set()
    seen_overrides: set[str] = set()
    seen_tags: set[str] = set()

    for op in _operations(base):
        oid = op["operationId"]
        seen_ops.add(oid)
        entry = OPERATIONS.get(oid)
        if entry is None:
            problems.append(f"no text: operation {oid}")
        else:
            check(f"{oid}.summary", entry.summary)
            check(f"{oid}.description", entry.description)
        for tag in op.get("tags", []):
            seen_tags.add(tag)
            if tag not in TAGS:
                problems.append(f"no text: tag {tag}")
        for param in op.get("parameters", []):
            key = f"{param['in']}:{param['name']}"
            seen_params.add(key)
            check(f"{oid} parameter {key}", PARAMS.get(key))
        for status in op.get("responses", {}):
            if status not in STATUS:
                problems.append(f"no text: status {status} ({oid})")
        for codes in op.get("x-error-codes", {}).values():
            for code in codes:
                check(f"{oid} error code {code}", ERROR_CODES.get(code))

    for name, schema in base["components"]["schemas"].items():
        check(f"schema {name}", _schema_text(name))
        for field in schema.get("properties", {}):
            key = f"{name}.{field}"
            if name.startswith("Page_"):
                pass
            elif key in FIELD_OVERRIDES:
                seen_overrides.add(key)
            else:
                seen_fields.add(field)
            check(f"field {key}", _field_text(name, field))

    for name, t in TAGS.items():
        check(f"tag {name}.name", t[0])
        check(f"tag {name}.description", t[1])

    problems += [f"stale operation: {k}" for k in sorted(OPERATIONS.keys() - seen_ops)]
    problems += [f"stale parameter: {k}" for k in sorted(PARAMS.keys() - seen_params)]
    problems += [f"stale field: {k}" for k in sorted(FIELDS.keys() - seen_fields)]
    problems += [f"stale override: {k}" for k in sorted(FIELD_OVERRIDES.keys() - seen_overrides)]
    problems += [
        f"stale schema: {k}" for k in sorted(SCHEMAS.keys() - base["components"]["schemas"].keys())
    ]
    problems += [f"stale tag: {k}" for k in sorted(TAGS.keys() - seen_tags)]
    return problems


def localized_spec(app: FastAPI, lang: str) -> dict[str, Any]:
    """Built once per process and language, then served from memory."""
    cache: dict[str, dict[str, Any]] | None = getattr(app.state, "api_docs", None)
    if cache is None:
        cache = {"_base": build_base_spec(app)}
        app.state.api_docs = cache
    if lang not in cache:
        cache[lang] = localize(cache["_base"], lang)
    return cache[lang]
