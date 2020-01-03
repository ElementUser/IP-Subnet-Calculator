# IP-Subnet-Calculator

# How to Use

The IPv4 subnet calculator will take a given subnet mask (GSM) and a host IP address (HIP) as inputs (both of these as additional arguments when ran through the command line, or will assume default values as specified in the code until the operator changes them), and will output the Class Type, Class Bits, Default Subnet Mask, number of borrowed bits, number of subnets, number of host bits, and the number of available hosts. For each subnet index in the total number of subnets, the calculator will also output the subnet ID, the broadcast address, the first host IP address, and the last host IP address.

# Prerequisites

On the Windows platform, ensure that Python 3 is installed and has its environment path set. The latest stable version of Python 3 can be obtained from the Python website, https://www.python.org/.

Afterwards, simply run either the Windows command prompt or Windows Powershell and navigate to the directory calculate.py and ipSubnetLogic.py are in.

Run calculate.py with either of the following command syntax (without the < or > brackets):

python calculate.py

python calculate.py <givenSubnetMask> <hostIPAddress>


The above commands can also be run in Mac or Linux by specifying calculate.py as the target file to run.
