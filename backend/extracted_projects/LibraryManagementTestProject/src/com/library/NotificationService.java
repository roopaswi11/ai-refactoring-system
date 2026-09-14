package com.library;
public class NotificationService {
    public void notifyBorrow(Member m, Book b) { System.out.println("Borrowed: " + m.getName() + " / " + b.getTitle()); }
    public void notifyReturn(Member m, Book b) { System.out.println("Returned: " + m.getName() + " / " + b.getTitle()); }
    public void notifyOverdue(Member m, int days) { System.out.println("Overdue: " + m.getName() + " / " + days); }
}
