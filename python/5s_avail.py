#!/usr/bin/python
# Hello world python program

import json, urllib2, sys, getopt, smtplib

def main(argv):

   models = {"ME341LL/A":"16G Black iPhone 5S", "ME342LL/A":"16G White iPhone 5S"}
   
   url = "http://store.apple.com/us/retail/availabilitySearch?parts.0=ME341LL%2FA&parts.1=ME342LL%2FA&store=R035"
   sender = 'jsippel@cheekybadger.com'
   receivers = ['jeff.sippel@edointeractive.com']

   help_text= """
   Usage: test.py [OPTIONS]

   Options
   
   -h: help
   -u, --url: the requested URL
   """

   try:
      opts, args = getopt.getopt(argv,"hu",["url"])
   except getopt.GetoptError:
      print help_text

      sys.exit(2)
   for opt, arg in opts:
      if opt == '-h':
         print help_text
         sys.exit()
      elif opt in ("-u", "--url"):
         url = arg
      
   apple_json = urllib2.urlopen(url)
   json_object = json.load(apple_json)
   stores = json_object.get("body",{}).get("stores",{})
   for item in stores:
      city = item.get("city",{})
      state = item.get("state",{})
      display = item.get("storeDisplayName",{})
      city_summary = display + " in " + city + ", " + state
      
      
      for results in item.get("partsAvailability",{}):
         text = item.get("partsAvailability",{}).get(results,{}).get("pickupDisplay",{})
         model = models.get(results)
         if text == 'available':
            print city_summary + " " + model + " is " + text
            message = """From: CheekyBadger <jsippel@cheekybadger.com>
To: Jeff <jsippel@gmail.com>
Subject: iPhone Availability


"""
            message = message + city_summary + " " + model + " is " + text      
            try:
               smtpObj = smtplib.SMTP('mail.cheekybadger.com',25)
               username = 'jsippel@cheekybadger.com'
               password = 'falshack'
               smtpObj.login(username,password)
               smtpObj.sendmail(sender, receivers, message)         
               print "Successfully sent email"
            except smtplib.SMTPException:
               print "Error: unable to send email"

      
if __name__ == "__main__":
   main(sys.argv[1:])
