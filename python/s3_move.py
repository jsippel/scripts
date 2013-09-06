#!/usr/bin/python
# Hello world python program

import boto, sys, getopt

def main(argv):
   src_bucket = ''
   src_prefix = ''
   dest_bucket = ''
   dest_folder = ''
   delete_original = False

   help_text= """
   Usage: test.py [OPTIONS]

   Options
   
   -h: help
   -s, --src-bucket: source bucket
   -sp, --src-prefix: source file prefix
   -d, --dest-bucket: destination bucket
   -df, --destination-folder: destination folder
   --delete-original
   """

   try:
      opts, args = getopt.getopt(argv,"hs:pd:f",["src-bucket=","dest-bucket=","src-prefix","dest-folder","delete-original"])
   except getopt.GetoptError:
      print help_text

      sys.exit(2)
   for opt, arg in opts:
      if opt == '-h':
         print help_text
         sys.exit()
      elif opt in ("-s", "--src-bucket"):
         src_bucket = arg
      elif opt in ("-p", "--src-prefix"):
         src_bucket = arg
      elif opt in ("-d", "--dest-bucket"):
         dest_bucket = arg
      elif opt in ("-f", "--dest-folder"):
         dest_folder = arg
      elif opt in ("--delete-original"):
         delete_original=True

   print "Moving files from " + src_bucket + " to " + dest_bucket + "\\" +dest_folder;

   s3 = boto.connect_s3()
   bucket = s3.get_bucket(src_bucket)
   rs = bucket.list(src_prefix)
   for key in rs:
      print key.name + " moved"
      key.copy(dest_bucket, dest_folder + key.name)
      if delete_original:
         bucket.delete_key(key)

if __name__ == "__main__":
   main(sys.argv[1:])
