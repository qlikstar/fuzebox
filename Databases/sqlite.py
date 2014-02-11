#############################################################################################
###################    DATABSE MODULE FOR FUZEBOX PROJECT    ################################    
#############################################################################################

'''
    Database Module for SQLite3.
    Instead of creating a physical database, virtual database has been created to speed up the 
    process of insertion and fetching.
'''
import sqlite3

class sqlite():

    def __init__(self,db):
        self.db = db #':memory:'
    
    def SqliteConnect(self,db):
        self.db = db
        try:
            self.conn = sqlite3.connect(self.db) #":memory:"
            #print "Connection Successful"
        except:
            print "Error opening database"
            return False
       
    def ExecQuery(self,query):
        self.query = query
        self.cur = self.conn.cursor()
        #print self.cur
        self.cur.execute(self.query)
        return self.cur.fetchall()
    
    

