from __future__ import annotations

import uuid
from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, Field

from app.models.enums import ShiftStatus
from app.schemas.common import ORMModel


class ShiftOpenIn(BaseModel):
    branch_id: uuid.UUID | None = None
    opening_float: Decimal = Field(default=Decimal("0"), ge=0)


class ShiftCloseIn(BaseModel):
    counted_cash: Decimal = Field(ge=0)
    note: str | None = Field(default=None, max_length=500)


class ShiftOut(ORMModel):
    id: uuid.UUID
    branch_id: uuid.UUID
    user_id: uuid.UUID
    status: ShiftStatus
    opened_at: datetime
    closed_at: datetime | None
    opening_float: Decimal
    expected_cash: Decimal
    counted_cash: Decimal | None
    cash_difference: Decimal | None
    note: str | None


class ShiftSummaryOut(BaseModel):
    """What the cashier sees before committing to a count."""

    shift: ShiftOut
    order_count: int
    gross_sales: Decimal
    cash_sales: Decimal
    card_sales: Decimal
    refund_total: Decimal


class ShiftListItem(ORMModel):
    """A closed shift as the office reviews it.

    Carries the names and the takings the row is judged on, so the review
    screen is one request rather than one per shift.
    """

    id: uuid.UUID
    branch_id: uuid.UUID
    branch_name: str
    user_id: uuid.UUID
    cashier_name: str
    status: ShiftStatus
    opened_at: datetime
    closed_at: datetime | None
    opening_float: Decimal
    expected_cash: Decimal
    counted_cash: Decimal | None
    cash_difference: Decimal | None
    note: str | None
    order_count: int
    gross_sales: Decimal
