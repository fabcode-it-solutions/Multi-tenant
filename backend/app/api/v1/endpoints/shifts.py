from __future__ import annotations

import uuid
from datetime import UTC, date, datetime, time, timedelta, tzinfo
from decimal import Decimal
from typing import Annotated
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError

from fastapi import APIRouter, Depends, Query
from sqlalchemy import func, select

from app.api.deps import CurrentTenant, CurrentUser, DbSession, require, resolve_branch_id
from app.core.exceptions import NotFoundError, PermissionDeniedError
from app.core.permissions import Permission
from app.models.enums import OrderStatus, PaymentMethod, ShiftStatus
from app.models.sales import Order, Payment, Shift
from app.models.tenant import Branch
from app.models.user import User
from app.schemas.common import Page
from app.schemas.shifts import (
    ShiftCloseIn,
    ShiftListItem,
    ShiftOpenIn,
    ShiftOut,
    ShiftSummaryOut,
)
from app.services import order_service

router = APIRouter(prefix="/shifts", tags=["shifts"])


@router.get("/current", response_model=ShiftOut | None)
async def current_shift(
    db: DbSession,
    user: CurrentUser,
    _: Annotated[object, Depends(require(Permission.SHIFT_OPEN))],
) -> Shift | None:
    """What the terminal asks on load, to decide whether to show the till or
    the "open your drawer" screen."""
    branch_id = resolve_branch_id(user, None)
    if branch_id is None:
        return None
    return await order_service.get_open_shift(db, user_id=user.id, branch_id=branch_id)


@router.post("/open", response_model=ShiftOut)
async def open_shift(
    payload: ShiftOpenIn,
    db: DbSession,
    user: CurrentUser,
    tenant: CurrentTenant,
    _: Annotated[object, Depends(require(Permission.SHIFT_OPEN))],
) -> Shift:
    branch_id = resolve_branch_id(user, payload.branch_id)
    if branch_id is None:
        raise PermissionDeniedError("No branch assigned to this terminal.")
    return await order_service.open_shift(
        db,
        tenant_id=tenant.id,
        user=user,
        branch_id=branch_id,
        opening_float=payload.opening_float,
    )


@router.get("/current/summary", response_model=ShiftSummaryOut)
async def current_shift_summary(
    db: DbSession,
    user: CurrentUser,
    _: Annotated[object, Depends(require(Permission.SHIFT_CLOSE))],
) -> ShiftSummaryOut:
    """Takings so far, so the cashier counts against a real figure."""
    branch_id = resolve_branch_id(user, None)
    shift = (
        await order_service.get_open_shift(db, user_id=user.id, branch_id=branch_id)
        if branch_id
        else None
    )
    if shift is None:
        raise NotFoundError("No open shift.", code="no_open_shift")

    totals = (
        await db.execute(
            select(
                func.count(Order.id),
                func.coalesce(func.sum(Order.total), 0),
                func.coalesce(func.sum(Order.refunded_total), 0),
            ).where(Order.shift_id == shift.id, Order.status != OrderStatus.DRAFT)
        )
    ).one()

    by_method = dict(
        (
            await db.execute(
                select(Payment.method, func.coalesce(func.sum(Payment.amount), 0))
                .join(Order, Order.id == Payment.order_id)
                .where(Order.shift_id == shift.id)
                .group_by(Payment.method)
            )
        ).all()
    )

    return ShiftSummaryOut(
        shift=ShiftOut.model_validate(shift),
        order_count=totals[0],
        gross_sales=Decimal(totals[1]),
        cash_sales=Decimal(by_method.get(PaymentMethod.CASH, 0)),
        card_sales=Decimal(by_method.get(PaymentMethod.CARD, 0)),
        refund_total=Decimal(totals[2]),
    )


@router.post("/current/close", response_model=ShiftOut)
async def close_current_shift(
    payload: ShiftCloseIn,
    db: DbSession,
    user: CurrentUser,
    _: Annotated[object, Depends(require(Permission.SHIFT_CLOSE))],
) -> Shift:
    branch_id = resolve_branch_id(user, None)
    shift = (
        await order_service.get_open_shift(db, user_id=user.id, branch_id=branch_id)
        if branch_id
        else None
    )
    if shift is None:
        raise NotFoundError("No open shift.", code="no_open_shift")

    return await order_service.close_shift(
        db, shift=shift, counted_cash=payload.counted_cash, note=payload.note
    )


@router.get("", response_model=Page[ShiftListItem])
async def list_shifts(
    db: DbSession,
    user: CurrentUser,
    tenant: CurrentTenant,
    _: Annotated[object, Depends(require(Permission.SHIFT_READ_ALL))],
    branch_id: uuid.UUID | None = None,
    user_id: uuid.UUID | None = None,
    status: ShiftStatus | None = None,
    date_from: date | None = None,
    date_to: date | None = None,
    page: int = Query(1, ge=1),
    size: int = Query(25, ge=1, le=100),
) -> Page[ShiftListItem]:
    """Every shift and how its drawer reconciled.

    Closing a till writes a cash difference; without this it was written to a
    row nothing ever read, which makes the count a ritual rather than a
    control. A shortfall is only useful to a shop that can see it.
    """
    conditions = []
    if branch_id:
        conditions.append(Shift.branch_id == branch_id)
    if user_id:
        conditions.append(Shift.user_id == user_id)
    if status:
        conditions.append(Shift.status == status)
    # Days are the shop's days, as on its receipts and reports. Read as UTC, a
    # shift opened at 01:30 in Tashkent on the 12th -- 20:30 UTC on the 11th --
    # vanished from "shifts on the 12th".
    zone = _shop_zone(tenant.timezone)
    if date_from:
        conditions.append(Shift.opened_at >= datetime.combine(date_from, time.min, tzinfo=zone))
    if date_to:
        # Inclusive: "to the 8th" means through the end of the 8th, not up to
        # midnight at its start.
        conditions.append(
            Shift.opened_at < datetime.combine(date_to + timedelta(days=1), time.min, tzinfo=zone)
        )

    total = await db.scalar(select(func.count()).select_from(Shift).where(*conditions)) or 0

    rows = (
        await db.execute(
            select(Shift, Branch.name, User.full_name)
            .join(Branch, Branch.id == Shift.branch_id)
            .join(User, User.id == Shift.user_id)
            .where(*conditions)
            .order_by(Shift.opened_at.desc())
            .offset((page - 1) * size)
            .limit(size)
        )
    ).all()

    shift_ids = [row[0].id for row in rows]
    takings: dict[uuid.UUID, tuple[int, Decimal]] = {}
    if shift_ids:
        takings = {
            shift_id: (count, Decimal(gross))
            for shift_id, count, gross in (
                await db.execute(
                    select(
                        Order.shift_id,
                        func.count(Order.id),
                        func.coalesce(func.sum(Order.total), 0),
                    )
                    .where(Order.shift_id.in_(shift_ids), Order.status != OrderStatus.DRAFT)
                    .group_by(Order.shift_id)
                )
            ).all()
        }

    items = [
        ShiftListItem(
            **{
                field: getattr(shift, field)
                for field in ShiftListItem.model_fields
                if hasattr(shift, field)
            },
            branch_name=branch_name,
            cashier_name=cashier_name,
            order_count=takings.get(shift.id, (0, Decimal("0")))[0],
            gross_sales=takings.get(shift.id, (0, Decimal("0")))[1],
        )
        for shift, branch_name, cashier_name in rows
    ]

    return Page(items=items, total=total, page=page, size=size)


def _shop_zone(name: str | None) -> tzinfo:
    """The shop's time zone, falling back to UTC for a name the zone database
    does not know -- the same fallback receipt numbering uses."""
    try:
        return ZoneInfo(name or "UTC")
    except (ZoneInfoNotFoundError, ValueError):
        return UTC
