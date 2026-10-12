"""Text in the three languages the API reference is published in."""

from __future__ import annotations

from typing import NamedTuple

LANGS = ("en", "uz", "ru")
LABELS = {"uz": "O'zbekcha", "ru": "Русский", "en": "English"}


class T(NamedTuple):
    """One piece of reference text, in every published language at once.

    Keeping the three side by side is the point: a translation that lives in
    another file is a translation nobody updates when the English changes.
    """

    en: str
    uz: str
    ru: str

    def of(self, lang: str) -> str:
        return getattr(self, lang)
