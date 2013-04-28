"""
   Copyright 2013 DISQUS
   
   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at
   
       http://www.apache.org/licenses/LICENSE-2.0
   
   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.
"""

import time
from django.conf import settings

next_sharded_id = """delimiter //
drop table if exists shard_seq_tbl //
create table shard_seq_tbl ( nextval bigint not null primary key auto_increment ) engine = MyISAM //
alter table shard_seq_tbl AUTO_INCREMENT = 10000 //

drop function if exists shard_nextval //
create function shard_nextval()
returns bigint
begin
   insert into shard_seq_tbl values (NULL) ;
   set @R_ObjectId_val=LAST_INSERT_ID() ;
   delete from shard_seq_tbl ;
   return @R_ObjectId_val ;
end//

drop function if exists now_msec//
CREATE FUNCTION now_msec RETURNS STRING SONAME "now_msec.so"//

drop function if exists next_sharded_id //
CREATE function next_sharded_id ()
RETURNS bigint
 BEGIN
    DECLARE our_epoch bigint DEFAULT 1325419260000;
    DECLARE seq_id bigint;
    DECLARE now_millis bigint;
    DECLARE shard_id int DEFAULT 5;
    DECLARE result bigint UNSIGNED;

    SELECT MOD(shard_nextval(),1024) INTO seq_id;

    SELECT now_msec() INTO now_millis;
    set result := (now_millis - our_epoch) << 23;
    set result := result | (seq_id << 10);
    set result := result | (shard_id);
    RETURN result;
 END//
delimiter ;""".format(our_epoch=settings.SHARD_EPOCH)
