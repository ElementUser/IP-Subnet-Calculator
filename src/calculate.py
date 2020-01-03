###################################################
# William Lam's IPv4 Subnet Calculator
# Student Number: 040871728
# Professor: Risvan Coskun
# Course: CST8108
# Language: Python 3
###################################################

# Imports
import re, sys
import ipSubnetLogic as calculator

#=================================================
# Inputs; user can change these to valid inputs 
# The output may not give expected results if inputs are invalid
#=================================================
givenSubnetMask = "/17" # This can be given in a bit notation, e.g. "/24", or as a regular IPv4 address
hostIP = "10.0.0.0"



#=================================================
# Main logic & Input Validation / Error Checking
#=================================================

# Regex match expression check (first error checking layer)
accepted_Regex = re.compile('^([0-9]{1,3}\\.){3}[0-9]{1,3}$') # Regex: match any number from 0-999 with a decimal afterwards 3 times, then a number from 0-999 one time

# Optional command line arguments
if ((len(sys.argv) == 2) or (len(sys.argv) > 3)):
    sys.exit("If running from the command line, please input either 0 extra arguments or 2 extra arguments.\nProper format is python calculate.py <givenSubnetMask> <hostIP>")

if (len(sys.argv) >= 3):
    givenSubnetMask = sys.argv[1]
    hostIP = sys.argv[2]

# If the Subnet Mask is given in the bits notation, convert from bit notation to an actual Subnet Mask IP Address format if it passes the regex checks
if givenSubnetMask[0] == "/":
    subnetBitCount = str(givenSubnetMask.lstrip("/"))
    try:
        subnetBitCountCheck = int(subnetBitCount)
        if (subnetBitCountCheck < 1 or subnetBitCountCheck > 32):
            sys.exit("Given Subnet Mask value must be between 1 and 32 (inclusively) when given in prefix format. Correct it & run the program again.")
    except ValueError:
        sys.exit("Correct your Given Subnet Mask input (it is not an integer in prefix format) & run the program again.")

    givenSubnetMask = calculator.convertBitCountToIP(int(subnetBitCount))
else: # Check regular IP Format
    if (re.match(accepted_Regex, givenSubnetMask)):
        # Check if each segment of the IP Address has a valid octet value (this is based on how an octet is filled from left-to-right)
        validOctetValues = [255,254,252,248,240,224,192,128,0]
        givenSubnetMaskSegments = givenSubnetMask.split(".", 3)

        for segment in givenSubnetMaskSegments:
            intSegment = int(segment)
            if intSegment not in validOctetValues:
                sys.exit("Given Subnet Mask value is invalid. Its octets contain only these numeric values: 255,254,252,248,240,224,192,128,0.\nCorrect it & run the program again.")
    else:        
        sys.exit("Given Subnet Mask formatting is invalid. Correct your Given Subnet Mask input & run the program again.")

# Check if givenSubnetMask is valid ; this check is to see if it's a consecutive string of 1s and 0s. If it fails, then terminate the program.
givenSubnetMaskCheckString = givenSubnetMask.strip(".")
previousChar = 1
charSwitch = False
for char in givenSubnetMaskCheckString:
    if (char == 0):
        charSwitch = True
    if (char == 1 and charSwitch == True):
        sys.exit("The given subnet mask is of an invalid format.")

# Host IP regex check
if (re.match(accepted_Regex, hostIP)):
    hostIPSegments = hostIP.split(".", 3)
    for segment in hostIPSegments:
        intSegment = int(segment)
        if intSegment < 0 or intSegment > 255:
            sys.exit("Host IP Address is invalid. Its octets must contain a value between 0 and 255 (inclusively).\nCorrect it & run the program again.")
else:
    sys.exit("Host IP Address formatting is invalid. Correct your Host IP input & run the program again.")



# This is the function for printing out the IP Subnet info regarding the Subnet Index the Host IP corresponds to (without generating a table)
calculator.printBasicResults(givenSubnetMask, hostIP)

# Construct the table of output results as .csv
print("\nPrinting tabulated results to ipSubnetCalculator_Results.csv ...")
calculator.constructIPSubnetTableCSV(givenSubnetMask, hostIP)

