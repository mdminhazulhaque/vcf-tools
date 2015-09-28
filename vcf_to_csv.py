#!/usr/bin/env python

"""
@author Md. Minhazul Haque
@link https://minhazulhaque.com
"""

import os

VCF_DIR='/home/minhaz/Contacts'
CSV_FILE='/home/minhaz/Contacts.csv'

# if there is no valid directory containing vcf files
if not os.path.isdir(VCF_DIR):
    print "%s not found" % (VCF_DIR)
    exit(1)
    
# move to the directory containing vcf files
os.chdir(VCF_DIR)

# calculate how many successful entries processed
entries = 0

# open a csv file for writing
try:
    csv = open(CSV_FILE, 'w')
except IOError:
    print "Could not open file!"
    exit(1)

# loop through all files in the directory
for _, _, files in os.walk(VCF_DIR):
    for vcf_file in files:
        vcard = open(vcf_file, 'r')
        
        name = None
        number = None
        
        for line in vcard.readlines():
            if line.startswith("N:"):
                name = line.replace("N:;", "")\
                    .replace("N:","")\
                    .replace(";;;;", "")\
                    .replace(";;;", "")\
                    .strip()
            elif "PREF:" in line:
                number = line.replace("TEL;VOICE;PREF:", "")\
                    .replace("TEL;CELL;PREF:", "")\
                    .replace("TEL;WORK;PREF:", "")\
                    .replace("TEL;HOME;PREF:", "")\
                    .replace("+88", "")\
                    .strip()
        # if name and number was successfully extracted from file
        if not name is None and not number is None:
            entries += 1
            row = '"%s","%s"\n' % (name, number)
            csv.write(row)
            print "Adding %s" % (name)
        # otherwise show which file has missing name or number
        else:
            print "No preferred name or number found in file", vcard.name
        
        vcard.close()
# close csv file
csv.close()
# show summary
print entries, "contacts added to", csv.name
