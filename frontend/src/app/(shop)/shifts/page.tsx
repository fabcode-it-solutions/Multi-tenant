"use client";

import { useQuery } from "@tanstack/react-query";
import { Wallet } from "lucide-react";
import { useState } from "react";

import { PageHeader } from "@/components/layout/page-header";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Card } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
import { Skeleton } from "@/components/ui/skeleton";
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table";
import type { ShiftListItem } from "@/lib/api/admin-types";
import { branchesApi, employeesApi, shiftsApi } from "@/lib/api/endpoints";
import { formatDateTime, formatMoney } from "@/lib/format";
import { readDrawer } from "@/lib/pos/reconcile";
import { useAuthStore } from "@/lib/stores/auth-store";

const PAGE_SIZE = 25;
const ANY = "any";

export default function ShiftsPage() {
  const currency = useAuthStore((s) => s.currency) ?? "USD";

  const [branchId, setBranchId] = useState(ANY);
  const [userId, setUserId] = useState(ANY);
  const [status, setStatus] = useState(ANY);
  const [dateFrom, setDateFrom] = useState("");
  const [dateTo, setDateTo] = useState("");
  const [page, setPage] = useState(1);

  const filters = {
    branch_id: branchId === ANY ? undefined : branchId,
    user_id: userId === ANY ? undefined : userId,
    status: status === ANY ? undefined : status,
    date_from: dateFrom || undefined,
    date_to: dateTo || undefined,
  };

  const shifts = useQuery({
    queryKey: ["shifts", filters, page],
    queryFn: () => shiftsApi.list({ ...filters, page, size: PAGE_SIZE }),
  });

  const branches = useQuery({
    queryKey: ["branches"],
    queryFn: () => branchesApi.list(),
  });
  const staff = useQuery({
    queryKey: ["employees", false],
    queryFn: () => employeesApi.list({ include_inactive: false }),
  });

  const items = shifts.data?.items ?? [];
  const total = shifts.data?.total ?? 0;
  const pages = Math.max(1, Math.ceil(total / PAGE_SIZE));

  // Only counted drawers belong in a discrepancy total. An open till has not
  // been counted yet, and folding its null in as a zero would report a shop
  // as balanced when nobody has looked.
  const counted = items.filter((row) => row.cash_difference !== null);
  const outByCents = counted.reduce(
    (sum, row) => sum + readDrawer(row.cash_difference).amountCents,
    0,
  );

  const onFilterChange =
    <T,>(setter: (value: T) => void) =>
    (value: T) => {
      setter(value);
      // Page 3 of the old filter is rarely page 3 of the new one.
      setPage(1);
    };

  return (
    <div className="space-y-6">
      <PageHeader
        title="Shifts"
        description="Every till, and how its drawer reconciled."
      />

      <div className="flex flex-wrap items-end gap-3">
        <Select value={status} onValueChange={onFilterChange(setStatus)}>
          <SelectTrigger className="w-36">
            <SelectValue placeholder="Status" />
          </SelectTrigger>
          <SelectContent>
            <SelectItem value={ANY}>Any status</SelectItem>
            <SelectItem value="open">Open</SelectItem>
            <SelectItem value="closed">Closed</SelectItem>
          </SelectContent>
        </Select>

        <Select value={userId} onValueChange={onFilterChange(setUserId)}>
          <SelectTrigger className="w-48">
            <SelectValue placeholder="Cashier" />
          </SelectTrigger>
          <SelectContent>
            <SelectItem value={ANY}>Everyone</SelectItem>
            {(staff.data?.items ?? []).map((person) => (
              <SelectItem key={person.id} value={person.id}>
                {person.full_name}
              </SelectItem>
            ))}
          </SelectContent>
        </Select>

        {(branches.data?.length ?? 0) > 1 && (
          <Select value={branchId} onValueChange={onFilterChange(setBranchId)}>
            <SelectTrigger className="w-44">
              <SelectValue placeholder="Branch" />
            </SelectTrigger>
            <SelectContent>
              <SelectItem value={ANY}>All branches</SelectItem>
              {(branches.data ?? []).map((branch) => (
                <SelectItem key={branch.id} value={branch.id}>
                  {branch.name}
                </SelectItem>
              ))}
            </SelectContent>
          </Select>
        )}

        <Input
          type="date"
          aria-label="From"
          value={dateFrom}
          onChange={(event) => onFilterChange(setDateFrom)(event.target.value)}
          className="w-40"
        />
        <Input
          type="date"
          aria-label="To"
          value={dateTo}
          onChange={(event) => onFilterChange(setDateTo)(event.target.value)}
          className="w-40"
        />

        {outByCents > 0 && (
          <p className="text-muted-foreground ml-auto text-sm">
            <span className="text-destructive font-medium">
              {formatMoney(outByCents / 100, currency)}
            </span>{" "}
            out across {counted.length} counted{" "}
            {counted.length === 1 ? "till" : "tills"} on this page
          </p>
        )}
      </div>

      <Card className="overflow-hidden p-0">
        <div className="overflow-x-auto">
          <Table>
            <TableHeader>
              <TableRow>
                <TableHead>Cashier</TableHead>
                <TableHead>Opened</TableHead>
                <TableHead>Closed</TableHead>
                <TableHead className="text-right">Sales</TableHead>
                <TableHead className="text-right">Taken</TableHead>
                <TableHead className="text-right">Expected</TableHead>
                <TableHead className="text-right">Counted</TableHead>
                <TableHead className="text-right">Difference</TableHead>
              </TableRow>
            </TableHeader>
            <TableBody>
              {shifts.isPending &&
                Array.from({ length: 5 }).map((_, index) => (
                  <TableRow key={index}>
                    <TableCell colSpan={8}>
                      <Skeleton className="h-8 w-full" />
                    </TableCell>
                  </TableRow>
                ))}

              {!shifts.isPending && items.length === 0 && (
                <TableRow>
                  <TableCell colSpan={8} className="py-14 text-center">
                    <Wallet className="text-muted-foreground mx-auto mb-2 size-7" />
                    <p className="text-muted-foreground text-sm">
                      No shifts match. Tills appear here once a cashier opens one.
                    </p>
                  </TableCell>
                </TableRow>
              )}

              {items.map((shift) => (
                <ShiftRow key={shift.id} shift={shift} currency={currency} />
              ))}
            </TableBody>
          </Table>
        </div>

        {pages > 1 && (
          <div className="text-muted-foreground flex items-center justify-between border-t p-3 text-sm">
            <span>
              Page {page} of {pages} · {total} shifts
            </span>
            <div className="flex gap-2">
              <Button
                variant="outline"
                size="sm"
                disabled={page <= 1}
                onClick={() => setPage((current) => current - 1)}
              >
                Previous
              </Button>
              <Button
                variant="outline"
                size="sm"
                disabled={page >= pages}
                onClick={() => setPage((current) => current + 1)}
              >
                Next
              </Button>
            </div>
          </div>
        )}
      </Card>
    </div>
  );
}

function ShiftRow({ shift, currency }: { shift: ShiftListItem; currency: string }) {
  const { state, amountCents } = readDrawer(shift.cash_difference);
  const uncounted = shift.cash_difference === null;

  return (
    <TableRow>
      <TableCell>
        <span className="block font-medium">{shift.cashier_name}</span>
        <span className="text-muted-foreground block text-xs">
          {shift.branch_name}
        </span>
      </TableCell>
      <TableCell className="text-muted-foreground text-sm">
        {formatDateTime(shift.opened_at)}
      </TableCell>
      <TableCell className="text-muted-foreground text-sm">
        {shift.closed_at ? (
          formatDateTime(shift.closed_at)
        ) : (
          <Badge variant="outline">Still open</Badge>
        )}
      </TableCell>
      <TableCell className="numeric text-muted-foreground text-right">
        {shift.order_count}
      </TableCell>
      <TableCell className="numeric text-right">
        {formatMoney(shift.gross_sales, currency)}
      </TableCell>
      <TableCell className="numeric text-muted-foreground text-right">
        {formatMoney(shift.expected_cash, currency)}
      </TableCell>
      <TableCell className="numeric text-right">
        {/* An open till has not been counted. Printing 0.00 here would read as
            "counted, and empty", which is a different and alarming fact. */}
        {shift.counted_cash === null
          ? "—"
          : formatMoney(shift.counted_cash, currency)}
      </TableCell>
      <TableCell className="numeric text-right">
        {uncounted ? (
          <span className="text-muted-foreground">—</span>
        ) : state === "balanced" ? (
          <span className="text-muted-foreground">Balanced</span>
        ) : (
          <span
            className="text-destructive font-medium"
            title={shift.note ?? undefined}
          >
            {state === "over" ? "+" : "−"}
            {formatMoney(amountCents / 100, currency)}
          </span>
        )}
      </TableCell>
    </TableRow>
  );
}
