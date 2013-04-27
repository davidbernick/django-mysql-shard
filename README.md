django-mysql-shard
==================

A Model for Django Models to inherit (and utilities) for abstracting horizontal sharding on MySQL. Follow the instructions and grow tables infinitely.

This is essentially a port of Instagram's methods:  
http://instagram-engineering.tumblr.com/post/10853187575/sharding-ids-at-instagram 

And uses lots of inspiration from Disqus: 
https://github.com/disqus/sharding-example

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
mysql> select next_sharded_id();
+--------------------+
| next_sharded_id()       |
+--------------------+
| 247562734190477317 |
+--------------------+
1 row in set (0.00 sec)
```

```
import bistring
a = bitstring.BitArray(bin(247562734190477317))
#print part where shard_id exists
print a[46:58].int
```
And there's your shard_id. I hope you can imagine what we're going to do with that! It means that any object we get will tell us where it lives without a lookup.  

What we'll go over next is how to integrate this all into django -- Inserts will put the file into its proper shard. Selects will map-reduce to get all of the matching queries in all of the shards.
