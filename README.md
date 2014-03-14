Introduction
============
RadioPi is a music and internet radio player for Linux. RadioPi uses MPD for
media play back, but other players can be added. The user interface is an
HD44870 LCD and a rotary encoder using lcdproc as the middleware.
 
Goals
=====

Internals
----------
 * Communicate with MPD

LCD interface
-------------
 * Controlled by a rotary encoder with a push switch
 * Connect to a WIFI
 * Use MPD with djmount to browse UPNP shares
 * Use MPD to play netradio
 * Use MPD to play music off usb memorysticks
 * Use MPD to play music of MTP devices
 
Web interface
-------------
 * Adding and editing playlist files for MPD, for net radio links
 
 
 Dependencies
 ============
 
  * lcdproc
  * mpd
  * python-mpd
 
 Misc
 ====
 Sorry about using both " and ' all over the place, I'm trying to use ' 
 consistently, but I have an old habit from my C days.
 
 Tips
 ====
 
 Use djmount to mount UPNP shares in MPD's music library directory and have MPD
 support UPNP/DLNA.
 
 Use usbmount to mount usb mass storage devices in MPD's music library directory and have MPD
 play music from them.