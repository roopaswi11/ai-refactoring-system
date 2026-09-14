package com.library;
public class FineCalculator {
    public double calculateFine(int overdueDays) {
        if (overdueDays <= 0) return 0;
        if (overdueDays <= 5) return overdueDays * 2.0;
        if (overdueDays <= 15) return 10.0 + (overdueDays - 5) * 3.0;
        return 40.0 + (overdueDays - 15) * 5.0;
    }
}
