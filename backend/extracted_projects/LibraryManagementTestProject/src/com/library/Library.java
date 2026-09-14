package com.library;
import java.util.ArrayList;
import java.util.List;
public class Library {
    private List<Book> books = new ArrayList<>();
    private List<Member> members = new ArrayList<>();
    public void addBook(Book book) { books.add(book); }
    public void registerMember(Member member) { members.add(member); }
    public Book findBook(String id) {
        for (Book book : books) if (book.getId().equals(id)) return book;
        return null;
    }
    public Member findMember(String id) {
        for (Member member : members) if (member.getId().equals(id)) return member;
        return null;
    }
    public List<Book> getBooks() { return books; }
    public List<Member> getMembers() { return members; }
}
