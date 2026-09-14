package com.library;
public class MemberReport {
    public String build(Member member) {
        StringBuilder report = new StringBuilder();
        report.append("Member ID: ").append(member.getId()).append("\n");
        report.append("Name: ").append(member.getName()).append("\n");
        report.append("Borrowed: ").append(member.getBorrowedBooks().size()).append("\n");
        for (String id : member.getBorrowedBooks()) report.append("- ").append(id).append("\n");
        return report.toString();
    }
}
