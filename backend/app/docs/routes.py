"""Swagger UI and the localized OpenAPI spec.

    /api/v1/docs                 Swagger UI, Uzbek first; ?lang= picks another
    /api/v1/openapi.json?lang=   the spec in en (default), uz or ru
    /docs                        redirect, for the address people guess first

Served under the API prefix because the reverse proxy forwards only /api/ and
/health to this process -- a reference at /docs would be unreachable.
"""

from __future__ import annotations

import json

from fastapi import FastAPI, Query
from fastapi.responses import HTMLResponse, JSONResponse, RedirectResponse

from app.core.config import settings
from app.docs.i18n.base import LABELS, LANGS
from app.docs.openapi import localized_spec

# Same major version FastAPI's own docs page pins.
SWAGGER_UI = "https://cdn.jsdelivr.net/npm/swagger-ui-dist@5"
DOCS_DEFAULT_LANG = "uz"
SPEC_DEFAULT_LANG = "en"


def install_docs(app: FastAPI) -> None:
    prefix = settings.API_V1_PREFIX
    spec_path = f"{prefix}/openapi.json"
    docs_path = f"{prefix}/docs"

    @app.get(spec_path, include_in_schema=False)
    async def openapi_spec(lang: str = Query(SPEC_DEFAULT_LANG)) -> JSONResponse:
        return JSONResponse(localized_spec(app, lang if lang in LANGS else SPEC_DEFAULT_LANG))

    @app.get(docs_path, include_in_schema=False)
    async def swagger_ui(lang: str = Query(DOCS_DEFAULT_LANG)) -> HTMLResponse:
        return HTMLResponse(_swagger_html(spec_path, lang if lang in LANGS else DOCS_DEFAULT_LANG))

    @app.get("/docs", include_in_schema=False)
    async def docs_redirect() -> RedirectResponse:
        return RedirectResponse(docs_path)


def _swagger_html(spec_path: str, lang: str) -> str:
    # The standalone layout's "Select a definition" menu is the language
    # switch: one definition per language, the chosen one first.
    order = [lang, *(code for code in ("uz", "ru", "en") if code != lang)]
    config = {
        "urls": [{"url": f"{spec_path}?lang={code}", "name": LABELS[code]} for code in order],
        "urls.primaryName": LABELS[lang],
        "dom_id": "#swagger-ui",
        "layout": "StandaloneLayout",
        "deepLinking": True,
        # Keeps the pasted token across reloads and language switches.
        "persistAuthorization": True,
        "displayRequestDuration": True,
        "docExpansion": "none",
        "filter": True,
        "defaultModelsExpandDepth": 0,
    }
    return f"""<!doctype html>
<html lang="{lang}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>JoinPay POS API</title>
<link rel="stylesheet" href="{SWAGGER_UI}/swagger-ui.css">
</head>
<body>
<div id="swagger-ui"></div>
<script src="{SWAGGER_UI}/swagger-ui-bundle.js"></script>
<script src="{SWAGGER_UI}/swagger-ui-standalone-preset.js"></script>
<script>
window.ui = SwaggerUIBundle(Object.assign({json.dumps(config, ensure_ascii=False)}, {{
  presets: [SwaggerUIBundle.presets.apis, SwaggerUIStandalonePreset],
  plugins: [SwaggerUIBundle.plugins.DownloadUrl],
}}));
</script>
</body>
</html>"""
