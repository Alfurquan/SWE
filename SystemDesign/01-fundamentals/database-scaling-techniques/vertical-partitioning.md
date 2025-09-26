# Vertical Partitioning

Imagine you’re running a busy online store with a massive customer database.

Each customer record contains dozens of columns—from basic information like name and email to rarely accessed details such as user preferences.

When your system has to retrieve data quickly for millions of users, it can struggle if every query has to sift through all this extra baggage. This is where vertical partitioning comes into play.

## What is Vertical Partitioning?

Vertical partitioning is a technique to split up a large tables into multiple smaller tables that contain a subset of columns from the original table.

Unlike horizontal partitioning, which divides data by rows (for example, splitting customers by region), vertical partitioning divides data by columns.