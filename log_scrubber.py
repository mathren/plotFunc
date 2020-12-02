# NAME: log_scrubber
# AUTHOR: William Wolf, modified by Mathieu renzo to turn it into a function
# LAST EDITED: March 25, 2019
# PURPOSE: Removes superfluous entries in MESA history files that are
#          artifacts of backups, restarts, etc. Essentially the entries
#          are pruned so that they are MESA-time-ordered with preference
#          going to most recently written model numbers of the same value.
#
# Depending on the version of MESA and how your history columns are set up,
# these first few variables may need to be reset. Otherwise, just put this
# script in your LOGS directory and execute it via 'python log_scrubber.py'
# to ensure your history is well-ordered. Only the most recently written
# timesteps are accepted for your new history (meaning that if a backup is
# done, the final version of the timestep is accepted).
# edited by Mathieu Renzo to adapt to other custom output files
########################################################
# CHECK TO SEE THAT THESE ARE APPROPRIATE FOR YOUR USE #
########################################################
import sys
import shlex


def log_scubber(logName):
    # dirty fix for PPI ejecta files
    if 'ejecta.data' in sys.argv[1]:
        dataStart = 1
    else:
        dataStart = 6

    ###################################################################
    # THIS SHOULDN'T NEED TO BE TOUCHED UNLESS YOU ARE SPEEDING IT UP #
    ###################################################################
    # Pull original data from history file
    f = open(logName, 'r')
    fileLines = f.readlines()
    f.close()
    headerLines = fileLines[:dataStart]
    dataLines = fileLines[dataStart:]

    # Determine which column is the model_number column
    headers = shlex.split(headerLines[dataStart-1])
    modelNumberCol = headers.index('model_number')

    # Get list of model numbers
    modelNumbers = [-1]*len(dataLines)
    for i in range(len(dataLines)):
        data = shlex.split(dataLines[i])
        modelNumbers[i] = int(data[modelNumberCol])

    # Pick "good" data points from the end to the beginning
    modelNumbers.reverse()
    dataLines.reverse()
    dataOut = []

    for i in range(len(modelNumbers)):
        if len(dataOut) == 0:
            dataOut.append(dataLines[i])
            lastGoodModelNumber = modelNumbers[i]
            #        print 'model_number = ', modelNumbers[i], ': Accepted!'
        elif modelNumbers[i] < lastGoodModelNumber:
            dataOut.append(dataLines[i])
            lastGoodModelNumber = modelNumbers[i]
            #        print 'model_number = ', modelNumbers[i], '<', lastGoodModelNumber, ': Accepted!'
            # else:
            #        print 'model_number = ', modelNumbers[i], '>=', lastGoodModelNumber, ': REJECTED!'

    # Properly reorder data and make combined output list of lines
    dataOut.reverse()
    fileLinesOut = headerLines + dataOut

    # Output ordered data back into history file
    f = open(logName, 'w')
    for line in fileLinesOut:
        f.write(line)
    f.close()

    print ('Data in', logName, 'has been scrubbed.')
