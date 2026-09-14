package com.library;
public class Main {
    public static void main(String[] args) {
        Library library = new Library();
        library.addBook(new Book("B101", "Clean Code", "Robert Martin"));
        library.addBook(new Book("B102", "Effective Java", "Joshua Bloch"));
        Member member = new Member("M101", "Ananya");
        library.registerMember(member);
        LibraryService service = new LibraryService(library);
        service.borrowBook("M101", "B101");
        service.printMemberHistory("M101");
    }
}
