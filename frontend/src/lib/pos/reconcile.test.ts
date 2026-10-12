import { describe, expect, it } from "vitest";

import { readDrawer } from "@/lib/pos/reconcile";

describe("readDrawer", () => {
  it("calls an exact drawer balanced", () => {
    expect(readDrawer("0")).toEqual({ state: "balanced", amountCents: 0 });
    expect(readDrawer("0.00")).toEqual({ state: "balanced", amountCents: 0 });
    expect(readDrawer(null)).toEqual({ state: "balanced", amountCents: 0 });
  });

  it("reports a surplus as over and a shortfall as short", () => {
    expect(readDrawer("5000.00")).toEqual({ state: "over", amountCents: 500000 });
    expect(readDrawer("-5000.00")).toEqual({ state: "short", amountCents: 500000 });
  });

  it("does not round a one-cent gap away into 'balanced'", () => {
    // The whole reason this is integer arithmetic. A till that is a cent out
    // is a till someone should look at, and "balanced" is what stops them.
    expect(readDrawer("-0.01").state).toBe("short");
    expect(readDrawer("0.01").state).toBe("over");
  });

  it("survives the float that would otherwise not be exactly zero", () => {
    // 0.1 + 0.2 - 0.3 in IEEE-754 is 5.55e-17, not 0.
    expect(readDrawer(0.1 + 0.2 - 0.3).state).toBe("balanced");
  });

  it("shows the magnitude without a sign, so the label carries the meaning", () => {
    expect(readDrawer("-1234.56").amountCents).toBe(123456);
  });
});
