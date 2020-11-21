##################################################
# Exports IoCs from STIX 2.0 files and writes
# these into a text file.
# Parsing is optimized for STIX 2.0 files from
# https://exchange.xforce.ibmcloud.com
##################################################
  
__author__ = "Fabian Voith"
__version__ = "1.0.2"
__email__ = "admin@fabian-voith.de"
  
import json
import sys
  
# By using sets, we avoid having duplicate
# IoCs in our output file
fileNames = set()
iocData = set()
outputFile = "iocs.txt"
  
# If no files were indicated or if we are running in Jupyter Notebook
# (i.e. first parameter = "-f"), 
# then we use a default filename "stix.json"
if len(sys.argv)<=1 or sys.argv[1]=="-f":
    fileNames.add("stix.json")
else:
    for x in sys.argv[1:]:
        fileNames.add(x)
          
try:
    for fileName in fileNames:
        with open(fileName) as json_data:
            data = json.load(json_data)
            print(str(len(data["objects"])) + " IoCs found in " + fileName)
 
            skipped=0
            for ioc in data["objects"]:
                if ioc["type"]=="indicator":
                    item = ioc["pattern"]
                    iocData.add(item.split(" ")[3].replace("'", ""))
                else:
                    #print('not an indicator, but '+ioc['type'])
                    skipped+=1
 
    with open(outputFile, "w") as f:
        for ioc in iocData:
            f.write("%s\n" % ioc)
except Exception as e:
    print("An error occured: " + str(e))
  
print(f"{str(len(iocData))} unique IoCs written to {outputFile}")
print(f"Skipped {str(skipped)} items, which were not IoCs (but reports, vulnerabilities, etc.).")
