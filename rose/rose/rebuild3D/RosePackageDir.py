def RosePackageDir():
    '''    get the actual directory name for the rose package, even in windows
    '''
    dirname = None; 
    # write the node code here.
    import rose
    # return outputs
    return rose.__path__[0],
