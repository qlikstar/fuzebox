from os.path import isfile



class filereader():
    
    def __init__(self,filenm):
        self.filenm = filenm
    
    def checkFileExists(self,filenm):
        self.filenm = filenm
        if not isfile(self.filenm):
            print "File not found !!"
            return False
        else:
            return True
        
        
    def readFile(self,filenm):
        self.filenm = filenm
        with open(self.filenm,'rb') as f:
            while True:
                line=f.readline()
                if not line: 
                    break
                else : 
                    return line.replace('\n','').split(',')
                
