import { toCents } from "@/lib/pos/money";

export type DrawerState = "balanced" | "over" | "short";

export interface DrawerVerdict {
  state: DrawerState;
  /** Always positive: the sign lives in `state`, not in the number shown. */
  amountCents: number;
}

/**
 * Turn a shift's cash_difference into what the cashier is told.
 *
 * Via integer minor units, because this is the one comparison in the till
 * that must not be done on a float: `0.1 + 0.2 !== 0.3` would let a drawer
 * that is a cent out report itself as balanced, and "balanced" is the word a
 * shop trusts when deciding not to investigate.
 */
export function readDrawer(difference: string | number | null): DrawerVerdict {
  const cents = toCents(difference ?? 0);
  if (cents === 0) return { state: "balanced", amountCents: 0 };
  return {
    state: cents > 0 ? "over" : "short",
    amountCents: Math.abs(cents),
  };
}
