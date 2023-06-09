#!/usr/bin/env python3

# import
import sys, re, os, getopt, os.path, mimetypes
from datetime import datetime 
from pathlib import Path

# script usage
def usage():
    '''script usage
    
    display script usage when the -h or --help option is used
    '''
    usage = """
-h --help display help
-i gimp curve file

curve2ffmpeg -i <gimpe curve>
    """
    print(usage)

def checkfile(infile):
    ''' check first argument passed to script
    
    check if first argument passed to script, is a file 
    '''
    if os.path.isfile(infile):
        return infile
    
# argv
argv = sys.argv[1:]

# store result of checkfile function
result = []

# main function
def main(argv):
    ''' main function
    
    check number of arguments passed to script
    '''
    if len(argv) == 0: # no arguments passed to script
        print("No arguments passed to script")
        usage()    # display script usage
        sys.exit() # exit
    elif len(argv) > 2: # too many arguments passed to script
        print("Too many arguments passed to script")
        usage()    # display script usage
        sys.exit() # exit
        
    try:
        opts, args = getopt.getopt(argv, "hi:", ["help", "infile"])
    except getopt.GetoptError as err: 
        print(err)  # will print something like "option -x not recognized"
        usage()     # display script usage
        sys.exit(2) # exit

    for opt, arg in opts:
        if opt in ("-h", "--help"):
            # -h or --help = display help
            usage()
            sys.exit()
        elif opt == ("-i") and len(argv) == 2:
            # -i and url or text file
            result.append(checkfile(argv[1]))
            return result

        else:
            assert False, "unhandled option"


#=================================================#
# slice off script name from arguments
#=================================================#

def entry():
    main(sys.argv[1:])

    # infile: set the variable infile to equal the contents of the file
    with open(result[0], 'r') as file:
        infile = file.read()
        file.close()          
    
    #make generator
    lower=0
    upper=1
    length=256
    zerotoonestepped256gen = [lower + x*(upper-lower)/length for x in range(length)]

    # format gimp curve for ffmpeg
    def formatForFFMPEG(values):
        serializedValues = values.split(' ')
        list = []
        for i in range (len(serializedValues)):
            if not list or zerotoonestepped256gen[i] - float(re.match(r"^[^////]*",list[-1]).group(0)) > 0.01:
                list.append('%s/%s' % (zerotoonestepped256gen[i], serializedValues[i]))
        return list
    
    # outfile destination
    name=(Path(argv[1]).resolve().stem)
    ext = 'txt'
    #outfile = os.path.join(home, desktop, '{}-{}.{}'.format(name, time, ext))
    outfile = os.path.join(os.path.dirname(os.path.realpath(__file__)), '{}-{}.{}'.format(name, 'ffmpeg', ext))
    
    # regex to find code in gimp curve
    foundValues = re.findall(r'(?<=samples 256) [\d. ]*',infile)
    
    # values
    masterValues = formatForFFMPEG(foundValues[0][1:])
    redValues = formatForFFMPEG(foundValues[1][1:])
    greenValues = formatForFFMPEG(foundValues[2][1:])
    blueValues = formatForFFMPEG(foundValues[3][1:])
    alphaValues = formatForFFMPEG(foundValues[4][1:])
    
    # ffmpeg prefix for code
    commandPrelim = 'curves=master=\''
    
    # command
    command = commandPrelim + ' '.join(masterValues) + '\':red=\'' + ' '.join(redValues) +'\':green=\'' + ' '.join(greenValues) + '\':blue=\'' + ' '.join(blueValues) + '\''
    
    # save file
    try:
        with open(outfile, 'w') as out:
            out.write(command + '\n')
    except KeyboardInterrupt:
        print("stopped by user")
    except IOError:
        print("input outpur error")

if __name__ == "__main__":
    entry()