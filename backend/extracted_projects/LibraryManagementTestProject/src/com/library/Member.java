package com.library;
import java.util.ArrayList;
import java.util.List;
public class Member {
    private String id, name;
    private List<String> borrowedBooks = new ArrayList<>();
    public Member(String id, String name) { this.id = id; this.name = name; }
    public String getId() { return id; }
    public String getName() { return name; }
    public void borrow(String bookId) { borrowedBooks.add(bookId); }
    public void returnBook(String bookId) { borrowedBooks.remove(bookId); }
    public List<String> getBorrowedBooks() { return borrowedBooks; }
}
