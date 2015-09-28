#!/usr/bin/env python

"""
This script converts a multi-contact VCF file for Nokia 139 backup format
"""

backup_file = open("/home/minhaz/backup.dat", "w")
vcf = open('/home/minhaz/downloads/Contacts.vcf', 'r')

card_name = ""
card_nums = []

card_data = """BEGIN:VCARD
VERSION:2.1
N;ENCODING=QUOTED-PRINTABLE;CHARSET=UTF-8:;=
{};;;
TEL;VOICE;CELL:{}
END:VCARD
"""

for line in vcf.readlines():
    if line.startswith('END:VCARD'):
        card_nums = list(set(card_nums))
        if len(card_nums) == 1:
            backup_file.write(card_data.format(card_name, card_nums[0]))
        else:
            for num in card_nums:
                operator_name = ""
                
                if str(num).startswith("016"):
                    operator_name = "AT"
                elif str(num).startswith("017"):
                    operator_name = "GP"
                elif str(num).startswith("015"):
                    operator_name = "TT"
                elif str(num).startswith("019"):
                    operator_name = "BL"
                elif str(num).startswith("018"):
                    operator_name = "RB"
                elif str(num).startswith("011"):
                    operator_name = "CC"
                else:
                    operator_name = "NA"
                    
                backup_file.write(card_data.format(card_name + " " + operator_name, num))
                    
        card_nums = []
    else:
        if line.startswith("FN:"):
            card_name = line.strip().replace("FN:", "").replace(";;;", "")
        elif line.startswith("TEL;"):
            number = line\
                    .replace("TEL;VOICE;PREF:", "")\
                    .replace("TEL;CELL;PREF:", "")\
                    .replace("TEL;WORK;PREF:", "")\
                    .replace("TEL;HOME;PREF:", "")\
                    .replace("TEL;VOICE:", "")\
                    .replace("TEL;CELL:", "")\
                    .replace("TEL;WORK:", "")\
                    .replace("TEL;HOME:", "")\
                    .replace("+88", "")\
                    .strip()
            card_nums.append(number)
        
vcf.close()
backup_file.close()