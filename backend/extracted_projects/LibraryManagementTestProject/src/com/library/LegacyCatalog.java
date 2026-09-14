package com.library;
import java.util.ArrayList;
import java.util.List;
public class LegacyCatalog {
    private List<String> records = new ArrayList<>();
    public void add(String record) { records.add(record); }
    public void processEverything(String input, int mode, boolean flag) {
        if (input == null) return;
        if (mode == 1) {
            if (flag) records.add(input.toUpperCase());
            else records.add(input.toLowerCase());
        } else if (mode == 2) {
            if (input.length() > 10) records.add(input.substring(0, 10));
            else records.add(input);
        } else if (mode == 3) records.add(input.replace(" ", "_"));
        else records.add(input);
    }
    public List<String> getRecords() { return records; }
}
