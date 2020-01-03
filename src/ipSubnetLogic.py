###################################################
# William Lam's IPv4 Subnet Calculator
# Student Number: 040871728
# Professor: Risvan Coskun
# Course: CST8108
# Language: Python 3
###################################################

# Imports
import math, re, csv, sys

#=================================================
# Static Parameters
classABits = 8
classBBits = 16
classCBits = 24

#=================================================

#=================================================
# Helper functions
#=================================================

def binaryToDecimal(binaryValue): # Input needs to be in string format
    return int(binaryValue, 2)

def decimalToBinary(decimalValue): # Input needs to be in integer format
    # https://docs.python.org/3/library/string.html
	# {:b}.format() reads the value as a binary and returns it in String form, without the leading 0
	return "{:b}".format(decimalValue)

# Converts a decimal to binary in an 8-bit form
def decimalToBinary_8Bit(decimalValue): # Input needs to be in string format
    binaryModified = decimalToBinary(decimalValue)

    # Ensure that the output will always be 8-bit by adding 0s at the beginning of the result
    while len(binaryModified) < 8:
        binaryModified = "0" + binaryModified

    return binaryModified

# Adds a "." after every 8th character in a raw IP address string as binary
def convertRawIPString(inputString, n=8):
	# range(a, b, c); a = start value, b = end value, c = step size
    return '.'.join(inputString[i:i+n] for i in range(0, len(inputString), n))


#=================================================
# IP-specific calculation functions
#=================================================

# Function takes in an IP Address, looks at the first 3 decimal values (first octet) of the IP address
# Returns the number of bits to calculate the Default Subnet Mask
def determineClassBits(ipAddress):
    ipAddressSegments = ipAddress.split(".", 3) # Split 3 times since an IPv4 address only has 4 different segments
    classBits = int(ipAddressSegments[0]) # First segment of the IP Address is used to determine the number of class bits
    
    if classBits <= 126 and classBits >= 0: # Class A
        return classABits
    elif classBits == 127: # 127 bits is invalid, as it is a reserved value
        sys.exit("127 is a reserved bit value & the calculation won't work.\nPlease run the program again with a valid IP address.")
    elif classBits <= 191: # Class B
        return classBBits
    elif classBits <= 223: # Class C
        return classCBits
    else:
        sys.exit("IP addresses that belong to Class D and Class E cannot be handled by this program.\nPlease run the program again with a valid IP address.")

def determineClassType(ipAddress):
    ipAddressSegments = ipAddress.split(".", 3) # Split 3 times since an IPv4 address only has 4 different segments
    classBits = int(ipAddressSegments[0]) # First segment of the IP Address is used to determine the number of class bits
    
    if classBits <= 126 and classBits >= 0: # Class A
        return "A"
    elif classBits == 127: # 127 bits is invalid, as it is a reserved value
        sys.exit("127 is a reserved bit value & the calculation won't work.")
    elif classBits <= 191: # Class B
        return "B"
    elif classBits <= 223: # Class C
        return "C"
    else:
        sys.exit("IP addresses that belong to Class D and Class E cannot be handled by this program.\nPlease run the program again with a valid IP address.")

# Function takes in the number of bits the Default Subnet Mask is supposed to have
# Returns the formatted Default Subnet Mask
def convertBitCountToIP(bitCount):
    defaultSubnetMask = ""

    # Fill each bit with a 1 up to the bitCount
    for iii in range(0, bitCount):
        defaultSubnetMask = defaultSubnetMask + "1"
    
    # Fill the remaining bits in the 32-bit Subnet Mask with 0s
    for iii in range (bitCount, 32):
        defaultSubnetMask = defaultSubnetMask + "0"
    
    # Add a "." character after every 8 bits in the subnet mask for proper formatting, except for the last 8 bits
    defaultSubnetMask = convertRawIPString(defaultSubnetMask)

    # Split the string & convert each section into decimal
    defaultSubnetMaskSegments = defaultSubnetMask.split(".", 3)
    defaultSubnetMask = "" # Reset defaultSubnetMask here
    for iii in range (0, 4): # Loop only 4 times since both subnet masks have 4 address segments
        defaultSubnetMask = defaultSubnetMask + str(binaryToDecimal(defaultSubnetMaskSegments[iii]))
        if iii < 3: # Don't add the "." character at the end of the IP address string
            defaultSubnetMask = defaultSubnetMask + "."

    return defaultSubnetMask

# Function takes in a Default Subnet Mask & a Given Subnet Mask
# Returns the number of Borrowed Bits
def determineBorrowedBits(defaultSubnetMask, givenSubnetMask):

    # Lexographical comparison
    if (givenSubnetMask < defaultSubnetMask):
        sys.exit("Given Subnet Mask is less than the Default Subnet Mask. This will result in an invalid operation.\nPlease correct the inputs & run the program again.")

    defaultSubnetMaskSegments = defaultSubnetMask.split(".", 3)
    givenSubnetMaskSegments = givenSubnetMask.split(".", 3)
    bitwiseXOR_Segments = []
    bitComparedString = ""
    borrowedBitsCount = 0

    for iii in range (0, 4): # Loop only 4 times since both subnet masks have 4 address segments
        # Perform the bitwise comparison between each character of the subnet masks
        bitwiseXOR_Segments.append(int(defaultSubnetMaskSegments[iii]) ^ int(givenSubnetMaskSegments[iii]))

        # Afterwards, count the number of ones in the bitwiseXOR_Segments after converting to binary form
        bitCountString = decimalToBinary(bitwiseXOR_Segments[iii])
        for eachChar in bitCountString:
            if eachChar == "1":
                borrowedBitsCount += 1

        # This code is merely for verification purposes by printing out the XOR-compared Subnet Mask result
        bitComparedString = bitComparedString + str(bitwiseXOR_Segments[iii])
        if iii < 3: # Don't add the "." character at the end of the IP address string
            bitComparedString = bitComparedString + "."
        
        #print(bitComparedString)

    return borrowedBitsCount

# Function performs a bitwise AND between the subnetMask and the ipAddress
# Returns the formatted result of the operation
def outputBitwiseAnd_IP_Decimal(subnetMask, ipAddress):
    subnetMaskSegments = subnetMask.split(".", 3)
    ipAddressSegments = ipAddress.split(".", 3)
    bitwiseAnd_Segments = []
    bitComparedString = ""

    for iii in range (0, 4): # Loop only 4 times since both subnet masks have 4 address segments
        # Perform the bitwise comparison between each character of the subnet masks
        bitwiseAnd_Segments.append(int(subnetMaskSegments[iii]) & int(ipAddressSegments[iii]))

        bitComparedString = bitComparedString + str(bitwiseAnd_Segments[iii])
        if iii < 3: # Don't add the "." character at the end of the IP address string
            bitComparedString = bitComparedString + "."

    return bitComparedString

# Function takes in the number of Borrowed Bits
# Returns the total number of Subnet indexes
def calculateNumSubnets(s):
    return int(math.pow(2,s))

# Function takes in the Default Subnet Mask and number of borrowed bits, and adds the number of borrowed bits
# Returns the first & last index of which the borrowed bits occupy as a list
def getBorrowedBitIndexes(defaultSubnetMask, borrowedBits):
    borrowedBitIndexes_FirstAndLast = []
    defaultSubnetMaskSegments = defaultSubnetMask.split(".", 3)
    defaultSubnetMaskBits = 0
    
    # Convert to binary
    for iii in range(0, 4):
        defaultSubnetMaskSegments[iii] = decimalToBinary(int(defaultSubnetMaskSegments[iii]))
        defaultSubnetMaskSegments[iii] = re.sub("0", "", defaultSubnetMaskSegments[iii]) # Remove any 0s from the expression
        defaultSubnetMaskBits = defaultSubnetMaskBits + len(defaultSubnetMaskSegments[iii]) # Count number of bits in each segment

    firstIndex = defaultSubnetMaskBits # Do not have to add +1 here, since array/list indexes start at 0
    lastIndex = defaultSubnetMaskBits + borrowedBits
    
    borrowedBitIndexes_FirstAndLast.append(firstIndex)
    borrowedBitIndexes_FirstAndLast.append(lastIndex)

    return borrowedBitIndexes_FirstAndLast

# Function takes in the subnet ID and borrowed bit indexes as a list
# Returns the specific subnet index of the subnet ID
def determineSubnetIndex(subnetID, borrowedBitIndexes):
    subnetIDSegments = subnetID.split(".", 3)
    subnetIDTemp = ""
    subnetIndexString = ""

    # Convert to binary
    for iii in range(0, 4):
        subnetIDSegments[iii] = decimalToBinary_8Bit(int(subnetIDSegments[iii]))
        subnetIDTemp = subnetIDTemp + subnetIDSegments[iii]

    # Edge case: if Given Subnet Mask is equal to the Default Subnet Mask prefix, then the borrowedBitIndexes will be the same and subnetIndexString will still be null.
    # If this is the case, set this to 0 by default, as there will only be one subnet at index 0.
    if (borrowedBitIndexes[0] == borrowedBitIndexes[1]):
        return 0
    else:
        for iii in range(borrowedBitIndexes[0], borrowedBitIndexes[1]):
            subnetIndexString = subnetIndexString + subnetIDTemp[iii]
        
            # Convert the result back to decimal
            subnetIndex = binaryToDecimal(subnetIndexString)
            return int(subnetIndex)


# Function takes in a Subnet ID, and the first & last Borrowed Bits indexes as a list, and changes all the bits after the last Borrowed Bits index from 0 to 1
# Returns the Broadcast Address
def calculateBroadcastAddress(subnetID, borrowedBitIndexes):
    broadcastAddressSegments = subnetID.split(".", 3)
    broadcastAddress = ""

    # Convert to binary
    for iii in range(0, 4):
        broadcastAddressSegments[iii] = decimalToBinary_8Bit(int(broadcastAddressSegments[iii]))
        broadcastAddress = broadcastAddress + str(broadcastAddressSegments[iii])

    for iii in range (borrowedBitIndexes[1], 32): # Replace each character after the last borrowed bit index with a "1" in the 32-bit IP address
        broadcastAddress = broadcastAddress[:iii] + "1" + broadcastAddress[iii+1:]  # Strings are immutable in Python, so use the string slicing method and assign to a new copy of the variable when overwriting the old one

    broadcastAddress = convertRawIPString(broadcastAddress)
    # Convert back to decimal
    broadcastAddressSegments = broadcastAddress.split(".", 3)
    broadcastAddress = ""

    for iii in range (0, 4):
        broadcastAddressSegments[iii] = str(binaryToDecimal(broadcastAddressSegments[iii]))
        broadcastAddress = broadcastAddress + broadcastAddressSegments[iii]
        if iii < 3: # Don't add the "." character at the end of the IP address string
            broadcastAddress = broadcastAddress + "."

    return broadcastAddress

# Function takes in a givenSubnetMask and counts the number of empty host bits in it
# Returns the number of host bits
def calculateHostBits(givenSubnetMask):
    subnetMaskSegments = givenSubnetMask.split(".", 3)
    subnetMaskBinary = ""
    hostBits = 0

    for iii in range(0, 4):
        subnetMaskSegments[iii] = decimalToBinary_8Bit(int(subnetMaskSegments[iii]))
        subnetMaskBinary = subnetMaskBinary + str(subnetMaskSegments[iii])
    
    for iii in range(len(subnetMaskBinary) - 1, 0, -1):
        if subnetMaskBinary[iii] == "0":
            hostBits = hostBits + 1
        else:
            break
    return hostBits

# Function takes in number of host bits
# Returns the host count
def calculateHostCount(h):
    return int(math.pow(2,h) - 2)

# Function takes in a subnet ID and calculates the First Host IP Address
# Returns the First Host IP address
def calculateFirstHost(subnetID):
    # FirstHost = SID Address + 1
    subnetIDSegments = subnetID.split(".", 3)
    firstHostAddress = ""

    # Addition in the decimal level, since it's much easier to work with than binary
    for iii in range (3, 0, -1): # Start from the last octet and progress towards the first octet
        if int(subnetIDSegments[iii]) + 1 > 255: # If the last octet overflows past 255, then set it to 0 and proceed to the next one
            subnetIDSegments[iii] = 0
            continue
        else:
            subnetIDSegments[iii] = int(subnetIDSegments[iii]) + 1
            break

    # Reconcatenate string
    for iii in range (0, 4):
        firstHostAddress = firstHostAddress + str(subnetIDSegments[iii])
        if iii < 3: # Don't add the "." character at the end of the IP address string
            firstHostAddress = firstHostAddress + "."
        
    return firstHostAddress

# Function takes in a broadcast address and calculates the Last Host IP Address
# Returns the Last Host IP address
def calculateLastHost(broadcastAddress):
    # Last Host = Broadcast Address - 1
    broadcastAddressSegments = broadcastAddress.split(".", 3)
    lastHostAddress = ""

    # Subtraction in the decimal level, since it's much easier to work with than binary
    for iii in range (3, 0, -1):
        if int(broadcastAddressSegments[iii]) - 1 < 0:
            continue
        else:
            broadcastAddressSegments[iii] = int(broadcastAddressSegments[iii]) - 1
            break

    # Reconcatenate string
    for iii in range (0, 4):
        lastHostAddress = lastHostAddress + str(broadcastAddressSegments[iii])
        if iii < 3: # Don't add the "." character at the end of the IP address string
            lastHostAddress = lastHostAddress + "."
        
    return lastHostAddress


# Function that prints out the basic results of the calculations
def printBasicResults(givenSubnetMask, hostIP):
    print("\n=================================================")
    print("Welcome to William Lam's IP Subnet Calculator")
    print("=================================================")
    print("")

    print("Inputs")
    print("_________________________________________________")
    print("")
    print("The Given Subnet Mask (GSM) is:", givenSubnetMask)
    print("The Host IP (or Given IP) Address is:", hostIP)
    print("")

    print("Outputs:")
    print("_________________________________________________")
    print("")

    classType = determineClassType(hostIP)
    print("The Class Type is:", classType)
    classBits = determineClassBits(hostIP)
    print("The number of bits in this Class' subnet is:", classBits)

    defaultSubnetMask = convertBitCountToIP(classBits)
    print("The Default Subnet Mask (DSM) is:", defaultSubnetMask)
    print("")

    s = determineBorrowedBits(defaultSubnetMask, givenSubnetMask)
    print("The number of Borrowed Bits (s) is:", s)
    S = calculateNumSubnets(s)
    print("The total number of Subnet Indexes (S) is:", S)
    h = calculateHostBits(givenSubnetMask)
    print("The total number of Host Bits (h) is:", h)
    H = calculateHostCount(h)
    print("The total number of available Hosts (H) is:", H)
    print("")

    borrowedBitIndexes = getBorrowedBitIndexes(defaultSubnetMask, s)
    subnetID = outputBitwiseAnd_IP_Decimal(givenSubnetMask, hostIP)
    print("The Subnet ID (SID) calculated by (Subnet Mask Given & Host IP) is:", subnetID)
    subnetIndex = determineSubnetIndex(subnetID, borrowedBitIndexes)
    print("The Subnet Index is:", subnetIndex)
    print("")

    broadcastAddress = calculateBroadcastAddress(subnetID, borrowedBitIndexes)
    print("The Broadcast Address (BA) is:", broadcastAddress)
    firstHostAddress = calculateFirstHost(subnetID)
    print("The First Host's (FH) Address is:", firstHostAddress)
    lastHostAddress = calculateLastHost(broadcastAddress)
    print("The Last Host's (LH) Address is:", lastHostAddress)

    print("\n=================================================")

    # Individual Test functions, commented out. These can be run on their own if desired.
    """ print(binaryToDecimal("0000111"))
    print(decimalToBinary_8Bit(10))
    splitIP(defaultSubnetMask)
    print(determineClassBits(hostIP)) 
    print(determineBorrowedBits(defaultSubnetMask, givenSubnetMask)) 
    print(outputBitwiseAnd_IP_Decimal(givenSubnetMask, hostIP))
    print(calculateNumSubnets(9))
    print(calculateLastHost("0.0.255.0"))
    print(calculateFirstHost("0.0.0.255"))
    print(convertBitCountToIP(classABits)) 
    print(hostIP)
    print(calculateBroadcastAddress(hostIP, getBorrowedBitIndexes(defaultSubnetMask, 3)))
    """


def constructIPSubnetTableCSV(givenSubnetMask, hostIP):
    # These variables will remain the same regardless of the Subnet ID
    classType = determineClassType(hostIP)
    classBits = determineClassBits(hostIP)
    defaultSubnetMask = convertBitCountToIP(classBits)
    s = determineBorrowedBits(defaultSubnetMask, givenSubnetMask)
    S = calculateNumSubnets(s)
    h = calculateHostBits(givenSubnetMask)
    H = calculateHostCount(h)
    borrowedBitIndexes = getBorrowedBitIndexes(defaultSubnetMask, s)
    
    # Write to a new .csv file with starting parameters
    csvRow = ["Given Subnet Mask", "Host IP Address"]    
    with open('ipSubnetCalculator_Results.csv', 'w', newline='') as csvFile:
        writer = csv.writer(csvFile)
        writer.writerow(csvRow)
    csvRow = [givenSubnetMask, hostIP]    
    with open('ipSubnetCalculator_Results.csv', 'a') as csvFile:
        writer = csv.writer(csvFile)
        writer.writerow(csvRow)
    
    # Calculated parameters that do not change with the subnet index
    csvRow = ["Class Type", "Class Bits", 
        "Default Subnet Mask", "Number of Borrowed Bits (s)", "Number of Subnets (S)", "Number of Host Bits (h)", "Number of Available Hosts (H)"]
    with open('ipSubnetCalculator_Results.csv', 'a', newline='') as csvFile:
        writer = csv.writer(csvFile)
        writer.writerow(csvRow)
    csvRow = [classType, classBits, defaultSubnetMask, s, S, h, H]
    with open('ipSubnetCalculator_Results.csv', 'a') as csvFile:
        writer = csv.writer(csvFile)
        writer.writerow(csvRow)

    # Header row for parameters that do vary with the subnet index
    csvRow = ["Subnet Index (n)", "Subnet ID (SID)", "First Host IP Address (FH)", "Last Host IP Address (LH)", "Broadcast Address (BA)"]
    with open('ipSubnetCalculator_Results.csv', 'a', newline='') as csvFile:
        writer = csv.writer(csvFile)
        writer.writerow(csvRow)

    # Calculate subnet ID for the specific host IP address and save it to be used later when outputting a table of all possible SIDs
    subnetIDSample = outputBitwiseAnd_IP_Decimal(givenSubnetMask, hostIP)

    # Prompt user to enter a range between 0 and S
    print("\nChoose a range of subnet indexes between 0 and %s (inclusively) to output to the .csv file" %(S - 1))

    minIndex = 0
    maxIndex = 1

    # Loop to ensure that maxIndex is less than minIndex
    minIndexCheckBool = False
    while (not minIndexCheckBool):
        minIndex = int(input("Enter the starting subnet index: "))
        if (minIndex >= 0 and minIndex <= S - 1):
            minIndexCheckBool = True
        else:
            print("The starting subnet index must be between 0 and %s, inclusively.\n" %(S-1))

    # Loop to ensure that maxIndex is less than minIndex
    maxIndexCheckBool = False
    while (not maxIndexCheckBool):
        maxIndex = int(input("Enter the end subnet index (must be equal or greater than %s): " %minIndex))
        
        if (maxIndex >= minIndex and maxIndex >= 0 and maxIndex <= S - 1):
            maxIndexCheckBool = True
        else:
            print("The end subnet index must be between 0 and %s & equal or greater than %s.\n" %(S - 1, minIndex))

    # Loop through each Subnet Index and calculate BA, FH & LH for each SID
    for iii in range (minIndex, maxIndex + 1):
        # Convert borrowed bits section to binary format for this loop's iteration
        borrowedBitBinary = decimalToBinary(iii)
        while len(borrowedBitBinary) < (borrowedBitIndexes[1] - borrowedBitIndexes[0]): # Extend the length of the bit string by adding leading 0s
            borrowedBitBinary = "0" + borrowedBitBinary
            
        # Split the subnetID_iteration into a list, then convert to 8-bit binary and then re-append it into a 32-bit string
        subnetIDSegments = subnetIDSample.split(".", 3)
        subnetID_iteration = ""
        for jjj in range (0, 4):
            subnetIDSegments[jjj] = decimalToBinary_8Bit(int(subnetIDSegments[jjj]))
            subnetID_iteration = subnetID_iteration + subnetIDSegments[jjj]
        
        # Separate the part of subnetID_iteration before the starting borrowed bit index with string slicing
        subnetID_iteration = subnetID_iteration[:borrowedBitIndexes[0]]

        # Append the current loop iteration of borrowedBitBinary string to subnetID_iteration
        subnetID_iteration = subnetID_iteration + borrowedBitBinary

        # Fill rest of the string to 0
        while (len(subnetID_iteration) < 32): # Convert to a 32-bit IP address
            subnetID_iteration = subnetID_iteration + "0"

        subnetID_iteration = convertRawIPString(subnetID_iteration)

        # Convert SID back to decimal
        subnetID_iterationSegments = subnetID_iteration.split(".", 3)
        subnetID_iteration = ""
        for jjj in range (0, 4):
            subnetID_iterationSegments[jjj] = str(binaryToDecimal(subnetID_iterationSegments[jjj]))
            subnetID_iteration = subnetID_iteration + subnetID_iterationSegments[jjj]
            if jjj < 3: # Don't add the "." character at the end of the IP address string
                subnetID_iteration = subnetID_iteration + "."            

        broadcastAddress = calculateBroadcastAddress(subnetID_iteration, borrowedBitIndexes)
        firstHostAddress = calculateFirstHost(subnetID_iteration)
        lastHostAddress = calculateLastHost(broadcastAddress)

        # Append this row of data to the existing .csv file
        csvRow = [iii, subnetID_iteration, firstHostAddress, lastHostAddress, broadcastAddress]
        with open('ipSubnetCalculator_Results.csv', 'a', newline='') as csvFile:
            writer = csv.writer(csvFile)
            writer.writerow(csvRow)
        
    #Print success message
    print("Table of results successfully constructed in ipSubnetCalculator_Results.csv")