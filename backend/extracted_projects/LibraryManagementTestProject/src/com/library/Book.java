package com.library;
public class Book {
    private String id, title, author;
    private boolean available = true;
    public Book(String id, String title, String author) {
        this.id = id; this.title = title; this.author = author;
    }
    public String getId() { return id; }
    public String getTitle() { return title; }
    public String getAuthor() { return author; }
    public boolean isAvailable() { return available; }
    public void setAvailable(boolean available) { this.available = available; }
}
