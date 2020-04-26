import xml.etree.ElementTree as et
import json
from operator import itemgetter
import optparse
import sys

def processannotation(item):
    # item should be a list like where:
    # item[0] is the annotation id,
    # item[1] is the annotation text whic may include multiple values separated by |,
    # item[2] is the annotation tier
    i = 0
    newitem = []
    item[1] = item[1].split("|")
    for annotation in item[1]:
        if annotation.find("viaf:") > 0:
            annotation = annotation.replace("viaf:", "https://viaf.org/viaf/")
        i = i + 1
        newitem.append([item[0] + "-" + str(i), annotation, item[2]])
    return newitem

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

#inputstream = "/home/thanasis/Documents/programming/harry-klynn-annotate/annotations/280b0e15-57f5-4f4e-a51c-982fdf54ea8e/b8cb44ba-81f2-456d-8b3d-660601aff3f2.eaf"
#xmldoc = et.parse(inputstream)

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
            newannotations = []
            for itemtwo in npaa[i - 1]['annotation']: # create a temporary array of the annotations in npaa call itemtwo
                temprow.append({"id": itemtwo['id'], "text": itemtwo['text'], "tier": itemtwo['tier']})
            # temprow.append([item[2], item[3], item[4]]) # and add the current annotation from paa in it
            newannotations = processannotation([item[2], item[3], item[4]]) # process the current annotation
            for newannotation in newannotations:
                temprow.append({"id": newannotation[0], "text": newannotation[1], "tier": newannotation[2]})
            npaa[i-1]['annotation'] = temprow # then replace what is there already with the new term row
        else:
            #npaa.append([ item[0], item[1], [[item[2], item[3], item[4]]] ])
            annotations = processannotation([item[2], item[3], item[4]])
            for annotation in annotations:
                npaa.append({"start": item[0], "end": item[1], "annotation": [{"id": annotation[0], "text": annotation[1], "tier": annotation[2]}]})
                i = i + 1
    except:
        annotations = processannotation([item[2], item[3], item[4]])
        for annotation in annotations:
            npaa.append({"start": item[0], "end": item[1], "annotation": [{"id": annotation[0], "text": annotation[1], "tier": annotation[2]}]})
            i = i + 1

json_string = json.dumps(npaa, ensure_ascii=False, indent=4)

if (options.out):
    file = open(options.out, 'w')
    file.write(json_string)
    file.close()
else:
    print(json_string)