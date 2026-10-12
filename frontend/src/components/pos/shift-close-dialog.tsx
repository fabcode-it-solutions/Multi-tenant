"use client";

import { useMutation, useQuery } from "@tanstack/react-query";
import { Loader2, Wallet } from "lucide-react";
import { useState } from "react";
import { toast } from "sonner";

import { Button } from "@/components/ui/button";
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
} from "@/components/ui/dialog";
import { Field, FieldDescription, FieldLabel } from "@/components/ui/field";
import { Input } from "@/components/ui/input";
import { Skeleton } from "@/components/ui/skeleton";
import { Textarea } from "@/components/ui/textarea";
import { shiftsApi } from "@/lib/api/endpoints";
import { isApiError } from "@/lib/api/errors";
import { formatDateTime, formatMoney } from "@/lib/format";
import { fromCents } from "@/lib/pos/money";
import { readDrawer } from "@/lib/pos/reconcile";

/**
 * Closing a shift is the other half of opening one.
 *
 * The opening float exists so that this screen has something to reconcile
 * against: expected = float + cash taken - cash refunded. The cashier counts
 * the drawer, and the gap between the count and the expectation is the number
 * a shop actually cares about -- it is how a wrong-change mistake, an unrung
 * sale, or a hand in the till shows up at all.
 *
 * The count is entered before the difference is revealed, deliberately. Show
 * the expected figure as a target to type and you have not measured the
 * drawer, you have measured whether someone can copy a number.
 */
export function ShiftCloseDialog({
  open,
  onOpenChange,
  currency,
  onClosed,
}: {
  open: boolean;
  onOpenChange: (open: boolean) => void;
  currency: string;
  onClosed: () => void;
}) {
  const [settled, setSettled] = useState<Settled | null>(null);

  // Once the till is closed the shift is gone whatever the cashier does with
  // this dialog, so every route out of it -- Done, Escape, the X -- has to
  // hand back to the terminal rather than just hiding the result.
  const dismiss = (next: boolean) => {
    if (next) {
      onOpenChange(true);
      return;
    }
    if (settled) {
      setSettled(null);
      onClosed();
      return;
    }
    onOpenChange(false);
  };

  return (
    <Dialog open={open} onOpenChange={dismiss}>
      <DialogContent className="sm:max-w-md">
        {settled ? (
          <ShiftSettled
            {...settled}
            currency={currency}
            onDone={() => dismiss(false)}
          />
        ) : (
          /* Keyed on `open` so a reopened dialog starts from a blank count
             rather than the previous attempt's. */
          <CloseShiftForm
            key={String(open)}
            currency={currency}
            onCancel={() => onOpenChange(false)}
            onSettled={setSettled}
          />
        )}
      </DialogContent>
    </Dialog>
  );
}

type Settled = { counted: string; difference: string };

function CloseShiftForm({
  currency,
  onCancel,
  onSettled,
}: {
  currency: string;
  onCancel: () => void;
  onSettled: (settled: Settled) => void;
}) {
  const [counted, setCounted] = useState("");
  const [note, setNote] = useState("");

  const summary = useQuery({
    queryKey: ["shift", "current", "summary"],
    queryFn: shiftsApi.summary,
  });

  const close = useMutation({
    mutationFn: () => shiftsApi.close(counted, note.trim() || undefined),
    // Deliberately does NOT refetch the shift here. Doing so makes the
    // terminal swap itself for the open-till gate, unmounting this dialog
    // before the cashier ever sees the difference -- which is the one number
    // the whole screen exists to show. The terminal refreshes on dismissal.
    onSuccess: (shift) =>
      onSettled({
        counted: shift.counted_cash ?? counted,
        difference: shift.cash_difference ?? "0",
      }),
    onError: (error) =>
      toast.error(isApiError(error) ? error.message : "Could not close the shift."),
  });

  if (summary.isPending || !summary.data) {
    return (
      <>
        <DialogHeader>
          <DialogTitle>Close your till</DialogTitle>
        </DialogHeader>
        <Skeleton className="h-56 w-full" />
      </>
    );
  }

  const { shift, order_count, gross_sales, cash_sales, refund_total } =
    summary.data;

  const countedIsValid = counted.trim() !== "" && Number(counted) >= 0;

  return (
    <>
      <DialogHeader>
        <DialogTitle>Close your till</DialogTitle>
        <DialogDescription>
          Open since {formatDateTime(shift.opened_at)}.
        </DialogDescription>
      </DialogHeader>

      <dl className="bg-muted/40 divide-border divide-y rounded-lg border text-sm">
        <Line label="Sales" value={`${order_count}`} />
        <Line
          label="Taken, all methods"
          value={formatMoney(gross_sales, currency)}
        />
        <Line label="Cash taken" value={formatMoney(cash_sales, currency)} />
        {Number(refund_total) > 0 && (
          <Line
            label="Refunded"
            value={`−${formatMoney(refund_total, currency)}`}
          />
        )}
        <Line
          label="Opening float"
          value={formatMoney(shift.opening_float, currency)}
        />
      </dl>

      <Field>
        <FieldLabel htmlFor="counted-cash">Cash counted in the drawer</FieldLabel>
        <Input
          id="counted-cash"
          inputMode="decimal"
          autoFocus
          autoComplete="off"
          placeholder="0.00"
          value={counted}
          onChange={(event) => setCounted(event.target.value)}
          className="numeric h-14 text-center text-2xl"
        />
        <FieldDescription>
          Count the drawer first. The difference is shown once you close.
        </FieldDescription>
      </Field>

      <Field>
        <FieldLabel htmlFor="shift-note">Note</FieldLabel>
        <Textarea
          id="shift-note"
          rows={2}
          value={note}
          onChange={(event) => setNote(event.target.value)}
          placeholder="Optional — anything that explains a difference."
        />
      </Field>

      <DialogFooter>
        <Button variant="outline" onClick={onCancel}>
          Keep selling
        </Button>
        <Button
          onClick={() => close.mutate()}
          disabled={!countedIsValid || close.isPending}
        >
          {close.isPending && <Loader2 className="size-4 animate-spin" />}
          Close shift
        </Button>
      </DialogFooter>
    </>
  );
}

function ShiftSettled({
  counted,
  difference,
  currency,
  onDone,
}: {
  counted: string;
  difference: string;
  currency: string;
  onDone: () => void;
}) {
  const { state, amountCents } = readDrawer(difference);
  const balanced = state === "balanced";
  const over = state === "over";

  return (
    <>
      <DialogHeader>
        <div
          className={
            "mx-auto flex size-12 items-center justify-center rounded-full " +
            (balanced
              ? "bg-primary/10 text-primary"
              : "bg-destructive/10 text-destructive")
          }
        >
          <Wallet className="size-6" />
        </div>
        <DialogTitle className="text-center">Shift closed</DialogTitle>
        <DialogDescription className="text-center">
          Counted {formatMoney(counted, currency)}.
        </DialogDescription>
      </DialogHeader>

      <p
        className={
          "text-center text-3xl font-semibold tabular-nums " +
          (balanced ? "" : "text-destructive")
        }
      >
        {balanced
          ? "Balanced"
          : `${over ? "+" : "−"}${formatMoney(fromCents(amountCents), currency)}`}
      </p>
      <p className="text-muted-foreground text-center text-sm">
        {balanced
          ? "The drawer matches what the till expected."
          : over
            ? "The drawer holds more than the till expected."
            : "The drawer holds less than the till expected."}
      </p>

      <DialogFooter>
        <Button onClick={onDone} className="w-full">
          Done
        </Button>
      </DialogFooter>
    </>
  );
}

function Line({ label, value }: { label: string; value: string }) {
  return (
    <div className="flex items-center justify-between px-3 py-2">
      <dt className="text-muted-foreground">{label}</dt>
      <dd className="numeric font-medium">{value}</dd>
    </div>
  );
}
