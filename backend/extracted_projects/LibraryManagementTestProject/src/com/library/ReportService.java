package com.library;
public class ReportService {
    public void printReport(Library library) {
        System.out.println("=== LIBRARY REPORT ===");
        System.out.println("Books: " + library.getBooks().size());
        System.out.println("Members: " + library.getMembers().size());
        for (Book book : library.getBooks()) {
            String status = book.isAvailable() ? "AVAILABLE" : "BORROWED";
            System.out.println(book.getId() + " | " + book.getTitle() + " | " + status);
        }
    }
}
