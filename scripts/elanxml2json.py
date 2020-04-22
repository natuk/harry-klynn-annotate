import xml.etree.ElementTree as et
import json
from operator import itemgetter
import optparse
import sys

p = optparse.OptionParser(
    description='Converts ELAN XML to JSON.  Reads from standard input by default, or from file if given.',
    prog='elanxml2json',
    usage='%prog -o file.json [file]'
)
p.add_option('--out', '-o', help="Write to OUT instead of stdout")

options, arguments = p.parse_args()

if len(arguments) == 1:
    try:
        inputstream = open(arguments[0])
    except:
        sys.stderr.write("Problem reading '{0}'\n".format(arguments[0]))
        p.print_help()
        sys.exit(-1)

xmldoc = et.parse(inputstream)

tsr1 = ""
tsr2 = ""
ptl = []
paa = []
npaa = []

# get all timeslots
for xtl in xmldoc.findall('//TIME_SLOT'):
    ptl.append( [xtl.get('TIME_SLOT_ID'), int(xtl.get('TIME_VALUE')) / 1000 ] ) # divide with 1000 to turn miliseconds to seconds

# for every tier
for xtr in xmldoc.findall('//TIER'):
    # get all annotations
    for xaa in xtr.findall('ANNOTATION/ALIGNABLE_ANNOTATION'):
        # get the start in sec
        for item in ptl:
            if item[0] == xaa.get('TIME_SLOT_REF1'):
                tsr1 = item[1]
                break
        # get the end in sec
        for item in ptl:
            if item[0] == xaa.get('TIME_SLOT_REF2'):
                tsr2 = item[1]
                break
        # get the text and the tier name
        paa.append( [ tsr1, tsr2, xaa.get('ANNOTATION_ID'), xaa.find('ANNOTATION_VALUE').text, xtr.get('TIER_ID') ] )

# merge annotations with the same start and end
# first sort by time slot
paa.sort(key=itemgetter(0,1))
i = 0
# paa is the current array with annotations, npaa is the new one with the merged annotations per given time period
for item in paa: # loop through every annotation
    try:
        if item[0] == npaa[i - 1]['start'] and item[1] == npaa[i - 1]['end']: # if the start time of the current paa annotation is the same as the last annotation from npaa
            temprow = []
            for itemtwo in npaa[i - 1]['annotation']: # create a temporary array of the annotations in npaa
                temprow.append({"id": itemtwo['id'], "text": itemtwo['text'], "tier": itemtwo['tier']})
            # temprow.append([item[2], item[3], item[4]]) # and add the current annotation from paa in it
            temprow.append({"id": item[2], "text": item[3], "tier": item[4]})
            npaa[i-1]['annotation'] = temprow # then replace what is there already with the new term row
        else:
            #npaa.append([ item[0], item[1], [[item[2], item[3], item[4]]] ])
            npaa.append({"start": item[0], "end": item[1], "annotation": [{"id": item[2], "text": item[3], "tier": item[4]}]})
            i = i + 1
    except:
        npaa.append({"start": item[0], "end": item[1], "annotation": [{"id": item[2], "text": item[3], "tier": item[4]}]})
        i = i + 1

json_string = json.dumps(npaa, ensure_ascii=False, indent=4)

if (options.out):
    file = open(options.out, 'w')
    file.write(json_string)
    file.close()
else:
    print(json_string)