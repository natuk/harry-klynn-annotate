## Harry Klynn Annotate

This is a website which presents audio tracks with a running set of annotations about the track. It hosts tracks from albums created by the Greek comedian Harry Klynn, but the same setup can be used for any track annotation.

### How it works

Data about the albums and tracks are downloaded from MusicBrainz as CSV (for the list of albums) and JSON (for the individual tracks).
Annotations for the tracks are produced manually using ELAN.
ELAN saves data as XML files with own schema. A python scipt is used to transform these XML files to JSON.
These data files is stored in the _data folder.
The website is build on Jekyll and hosted on GitHub over here.
The magic for the scrolling annotations is provided by the able library.

### Harry Klynn

[Harry Klynn](https://en.wikipedia.org/wiki/Vasilis_Triantafillidis) was a Greek comedian who produced a series of record albums from 1978 until 2002 with

## Authority files

VIAF
MusicBrainz

## ELAN annotation conventions

For the able viewer to work neatly we need the ELAN annotation timeslot to match broadly across all tiers. In ELAN it it not possible to create multiple annotations on the same tier and for the same timeslot. This is useful for multiple references in this project. To go around this problem we separate each reference using `|`. Links are produced using markdown's convention of `[link name](link url)`. For links to authority files
