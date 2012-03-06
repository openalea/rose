def tempPickleFile(filename):
    '''    returns a picklefile name in a temp dir according to the os 
    '''
    picklefile = None; 
    # write the node code here.
    if filename is None:
	    filename="tempfile.dat"
    import os
    tempDir=os.getenv("TEMP")
    if not tempDir:
	    tempDir="/tmp"
    picklefile=tempDir + os.sep + filename
    # return outputs
    return picklefile,
