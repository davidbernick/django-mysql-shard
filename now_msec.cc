#include <my_global.h>
#include <my_sys.h>
#include <mysql.h>

#include <stdio.h>
#include <string.h>
#include <sys/time.h>
#include <time.h>
#include <unistd.h>
/* Modified heavily by Bernz (David Bernick) - github.com/davidbernick */

/* Taken from: */

/* Copyright (c) 2006 Wadimoff <wadimoff@yahoo.com>                            */
/* Created:  27 April 2006                                                            */

/* NOW_MSEC() returns a character string representing the current date and time       */
/* with milliseconds in format YYYY-MM-DD HH:MM:SS.mmm  e.g.: 2006-04-27 17:10:52.129 */

/* How to install:                                                                    */
/* #1  gcc -shared -fPIC -o now_msec.so now_msec.cc -I /usr/include/mysql             */
/* #2  cp now_msec.so /usr/lib/mysql/plugin/                                                        */
/*     Comment : you can copy this wherever you want in the LD path                   */
/* #3  Run this query :                                                               */
/*     CREATE FUNCTION now_msec RETURNS STRING SONAME "now_msec.so";                  */
/* #4  Run this query to test it:                                                     */
/*     SELECT NOW_MSEC();                                                             */
/*     It should return something like that                                           */
/*                                                                                    */
/* mysql> select NOW_MSEC();                                                          */
/* +-------------------------+                                                        */
/* | NOW_MSEC()              |                                                        */
/* +-------------------------+                                                        */
/* | 2006-04-28 09:46:13.906 |                                                        */
/* +-------------------------+                                                        */
/* 1 row in set (0.01 sec)                                                            */

extern "C" {
   my_bool now_msec_init(UDF_INIT *initid, UDF_ARGS *args, char *message);
   char *now_msec(
               UDF_INIT *initid,
               UDF_ARGS *args,
               char *result,
               unsigned long *length, char *is_null, char *error);
}

my_bool now_msec_init(UDF_INIT *initid, UDF_ARGS *args, char *message) {
   return 0;
}


char *now_msec(UDF_INIT *initid, UDF_ARGS *args, char *result,
               unsigned long *length, char *is_null, char *error) {

  struct timeval tv;
  struct tm* ptm;
  char *msec_time_string = result;
  time_t t;


  /* Obtain the time of day, and convert it to a tm struct. */
  gettimeofday (&tv, NULL);

  t = (time_t)tv.tv_sec;
  long long millis = (tv.tv_sec * 1000) + (tv.tv_usec / 1000);
  sprintf(msec_time_string, "%lld", millis);

  *length = strnlen (msec_time_string, 32);

  return(msec_time_string);
}

