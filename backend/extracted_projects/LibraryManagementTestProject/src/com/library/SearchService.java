package com.library;
import java.util.ArrayList;
import java.util.List;
public class SearchService {
    private Library library;
    public SearchService(Library library) { this.library = library; }
    public List<Book> search(String keyword) {
        List<Book> result = new ArrayList<>();
        for (Book book : library.getBooks()) {
            if (book.getTitle().toLowerCase().contains(keyword.toLowerCase())
                    || book.getAuthor().toLowerCase().contains(keyword.toLowerCase())) result.add(book);
        }
        return result;
    }
}
