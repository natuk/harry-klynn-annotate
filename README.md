*README incomplete*

## Harry Klynn Annotate

This is a website which presents audio tracks with a running set of annotations. It hosts tracks from albums created by the Greek comedian Harry Klynn, but the system is independent of content.

[Live website here](https://natuk.github.io/harry-klynn-annotate).

### How it works

Data about the albums and tracks are downloaded from [MusicBrainz](https://musicbrainz.org/) as CSV (for the list of albums) and JSON (for the individual tracks).
Annotations for the tracks are produced manually using [ELAN](https://archive.mpi.nl/tla/elan).
ELAN saves data as XML files with own schema. A python script (`scripts/elanxml2json.py`) is used to transform these XML files to JSON. This can run on the command line like this:

`python3 elanxml2json.py -o <output.json> <elan-xml-file.json>`

These data files is stored in the `_data` folder.
The website is built on [Jekyll](https://jekyllrb.com/) and hosted on GitHub over [here](https://natuk.github.io/harry-klynn-annotate).
The magic for the scrolling annotations is provided by the fantastic [able](https://github.com/ableplayer/ableplayer) library.

### Harry Klynn

[Harry Klynn](https://en.wikipedia.org/wiki/Vasilis_Triantafillidis) was a Greek comedian who produced a series of record albums from 1978 until 2002.

## Authority files

People: [VIAF](https://viaf.org/)
Tracks: [MusicBrainz](https://musicbrainz.org/)

## ELAN annotation conventions

For the able viewer to work neatly we need the ELAN annotation timeslot to match broadly across all tiers. In ELAN it it not possible to create multiple annotations on the same tier and for the same timeslot. This is useful for multiple references in this project. To go around this problem we separate each reference using `|`. Links are produced using markdown's convention of `[link name](link url)`.
