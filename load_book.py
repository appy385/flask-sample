LOAD DATA LOCAL INFILE '/Users/apoorva/Documents/ACMS/flask-sample/scifi.csv'
INTO TABLE book
FIELDS TERMINATED BY ',' ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 LINES
(book_id, goodreads_book_id, authors, isbn, title, average_rating, image_url, genre);

LOAD DATA LOCAL INFILE "/home/soumya/Desktop/books_test.csv"
INTO TABLE books7 FIELDS TERMINATED BY ','   LINES TERMINATED BY '\n' IGNORE 1 LINES  (x,goodreads_book_id,authors,isbn,original_title,avaerage_rating,image_url,genre);
