django-mysql-shard
==================

A Model for Django Models to inherit (and utilities) for abstracting horizontal sharding on MySQL. Follow the instructions and grow tables infinitely.

This is essentially a port of Instagram's methods:  
http://instagram-engineering.tumblr.com/post/10853187575/sharding-ids-at-instagram

Why not just do range based?
===============================
Because all new entries would just end up on one machine rather than balance. Range based is good for things that are read in a balanced way.

Why not just use a NoSQL database?
======================================
Relations in your code and/or in your database? I like having some relations in the database.

Building
=============
On each MySQL machine, build the hash generator thing:  

```
gcc -shared -fPIC -o now_msec.so now_msec.cc -I /usr/include/mysql

sudo cp -rfp now_msec.so /usr/lib/mysql/plugin/
```

Then, on each machine execute, change this line in create_shard_table.sql and replace 5 with each MySQL shard ID number. Just make sure each MySQL machine has a different number.  

```
    DECLARE shard_id int DEFAULT 5;
```

Then run the MySQL:
```
mysql -uroot -pasdfasdf dbname < create_shard_table.sql
```

Now if you run:
```
mysql> select simpleproc();
+--------------------+
| simpleproc()       |
+--------------------+
| 247562734190477317 |
+--------------------+
1 row in set (0.00 sec)
```

In the next section, we'll go over how that new string of numbers (your new ID) works with Django and how it auto-identifies which shard it lives on.
