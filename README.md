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
The web interfaces has now been separated into RadioPiWeb

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


 External stuff
 ===========
 Sometimes there are some quirks in the software that RadioPi depend on, this is
 the place to write about them.
 
 LCDproc
 -------
 I have wrestled a lot with lcdproc, especially the menus. Debugging, and at
 least RadioPi would benefit from a "list_menus" command, that basically prints
 out the internal menu structure from lcdproc to the client.
 
 MPD
 ---
 For some reason MPD does not read extended info from M3U files placed in it's
 'playlist' directory. For now the internet radio play list are placed in the 
 'music' directory.
 
 I hope to someday go ahead and look into these things and contribute back.
 
 Tips
 ====
 
 Use djmount to mount UPNP shares in MPD's music library directory and have MPD
 support UPNP/DLNA.
 
 Use usbmount to mount usb mass storage devices in MPD's music library directory and have MPD
 play music from them.