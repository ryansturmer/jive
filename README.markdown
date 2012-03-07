Jive - Web frontend for MPD (The Music Player Daemon)
-----------------------------------

### Summary

Jive is a web-based frontend for MPD, written in python.  It provides
a simple interface to your music library, and basic play controls.

### Features

- Playlist editor
- Support for MPD stored playlists
- Simple play controls
- Music library search
- Responsive design that also looks good on tablet devices (kindle, xoom, etc)

### Coming Soon

- More advanced play controls (shuffle, repeat, etc)
- Improved search
- More flexible playlist editing
- Better keyboard navigation
- Filesystem browser
- Settings
- Alarm clock!

### Install and Run

The only dependency (besides python) is flask, which you can install from 
the cheese shop or here: <http://flask.pocoo.org/>  To run jive, just
run main.py.

### Configuration

jive.cfg is the configuration file for jive, which will be created on first run, 
if it doesn't already exist.  You can change the host/port of the MPD server, and 
the port on which Jive hosts itself for development.  It's pretty self explanatory.