package com.library;
public class LibraryService {
    private Library library;
    public LibraryService(Library library) { this.library = library; }
    public void borrowBook(String memberId, String bookId) {
        Member member = library.findMember(memberId);
        Book book = library.findBook(bookId);
        if (member == null) { System.out.println("Member not found"); return; }
        if (book == null) { System.out.println("Book not found"); return; }
        if (!book.isAvailable()) { System.out.println("Book unavailable"); return; }
        book.setAvailable(false);
        member.borrow(bookId);
        System.out.println(member.getName() + " borrowed " + book.getTitle());
    }
    public void returnBook(String memberId, String bookId) {
        Member member = library.findMember(memberId);
        Book book = library.findBook(bookId);
        if (member != null && book != null) {
            book.setAvailable(true);
            member.returnBook(bookId);
        }
    }
    public void printMemberHistory(String memberId) {
        Member member = library.findMember(memberId);
        if (member != null) {
            System.out.println("History for " + member.getName());
            for (String bookId : member.getBorrowedBooks()) System.out.println(bookId);
        }
    }
}
