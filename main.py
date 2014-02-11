#############################################################################################
###################    MAIN PROGRAM FOR FUZEBOX PROJECT    ##################################    
#############################################################################################


''' This main program will do the following 
        1. Read the CSV Data file supplied
        2. Create a database in SQLite in the "memory"
        3. Insert records into the table as per the pre defined table structure
        4. Fire an analytics query to bring out some meaningful data
        5. Fetch the records from database and create a JSON file 
'''

''' IMPORTING ALL THE REQUIRED MODULES '''
from Databases.sqlite import *
from os.path import isfile
import json
from datetime import datetime
import config


# Function to check if file exists
def isFilePresent (filename):
    if isfile (filename):
        return True
    else:
        print "File not found !!"
        return False


# Read and Process the file read
def readFile (filename , dbobj):    
    ''' 1. If the file is present then read the contents line by line
        2. Call the function processFile to create resultset
        3. Insert the records in the table
    '''
    gameid      = 0
    count       = 0
    
    with open(filename,'rb') as f:
        while True:
            line=f.readline()
            if not line: 
                break
            else : 
                output = line.replace('\n','').split(',')
                gameid +=1 
                resultset = processFile (output , gameid)
                count = count + 1    

            for statement in createInsertstatement (resultset).split(';'):
                dbobj.ExecQuery(statement+ ';')
    f.close()
    return count



# Function to process the data file
def processFile( input, gameid):
    ''' This function takes the input file and creates meaningful data from it. '''    
    
    pos = 0
    indrow = ()
    resultset = []
    
    for playername in input[:-1]:
        if pos/5+1 == int(input[-1]):
            result = 1
        else:
            result = 0
        pos+=1
        indrow = (gameid, (pos/6)+1 , pos%5+1, playername, result)
        resultset.append(indrow)
    return resultset
 


''' This Function creates insert statements to be processed in the database '''   
def createInsertstatement (input):
    statement = ''
    for record in input:
        statement += config.insertquery + str(record) +'; '
    return statement
         


def processAnalyticsQuery( dbobj , analytics_query ):
    '''1. This part executes the analytics query to find some meaningful data from the datafile
       2. Once this data is fetched, it is packed into a JSON file for the next
    '''
    jsonobj     = []
    reader =  dbobj.ExecQuery ( config.analytics_query)
    for record in reader:
        dict = {}
        for value in range(len(record)):
            if isinstance(record[value], unicode):
                dict[config.header[value]] = str(record[value])
            else:
                dict[config.header[value]] = record[value]
                   
        jsonobj.append(dict)
    
    json_output =  str(jsonobj).replace('\'' , '"' )
    return json_output



# Function to write a JSON file  
def jsonWrite( filename , contents) :
    
    f = open( filename , 'w')
    f.write( contents )    
    f.close()
    return



#-------------------------------------------------------------------------------------------------------------
''' This main program will do the following 
        1. Read the CSV Data file supplied
        2. Create a database in SQLite in the "memory"
        3. Insert records into the table as per the pre defined table structure
        4. Fire an analytics query to bring out some meaningful data
        5. Fetch the records from database and create a JSON file 
'''
#-------------------------------------------------------------------------------------------------------------
def main():      

    # Execution Begins ...
    print "Execution Starts : " + str(datetime.now()) 
    print "Job is Executing... Please wait ....."
     
    ''' Database Objects to connect execute and retrieve the records '''  
    obj = sqlite(config.database)
    obj.SqliteConnect(config.database)
    obj.ExecQuery(config.createtable)
    rows = obj.ExecQuery(config.query) 

    '''To check if the datafile exists at the specified location '''
    if isFilePresent(config.filename):
        count = readFile (config.filename , obj)
 
    json_output = processAnalyticsQuery( obj , config.analytics_query )
     
    # The JSON output writer
    jsonWrite(config.jsonoutput , json_output )
    print "Execution Completes successfully at : " + str(datetime.now()) 
    print str(count) + " records have been processed !!" 


''' Calling the main() ''' 
if __name__ == '__main__':
    main()