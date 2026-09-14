package com.library;
public class ValidationUtil {
    public static boolean validBookId(String id) { return id != null && id.matches("B[0-9]+"); }
    public static boolean validMemberId(String id) { return id != null && id.matches("M[0-9]+"); }
    public static boolean validName(String name) { return name != null && !name.trim().isEmpty(); }
}
