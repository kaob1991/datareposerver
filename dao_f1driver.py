 
# Database access object
# using python to control database
# 

# dev.mysql.com/doc/connector-python/en/connector-python-api-mysqlcursor.html
# This gets imported into Flask!!!

import mysql.connector
import dbconfig as cfg

class driverDAO:

# Setting up the database and access points

    host = "",
    user = ""
    password = "" 
    database = ""
    connection = ""
    cursor = ""


    def __init__(self):
        # reading these in from a config file for ease of portability
        self.host= cfg.mysql['host']
        self.user= cfg.mysql['user']
        self.password = cfg.mysql['password']
        self.database = cfg.mysql['database']
    

    def getCursor(self):
        self.connection = mysql.connector.connect(
            host = self.host,
            user= self.user,
            password=self.password,
            database = self.database,
        )
        self.cursor = self.connection.cursor()
        return self.cursor


    def closeAll(self):
        self.connection.close()
        self.cursor.close()


## ~~~~~~~~~~~~~~~~~~~~~~~~~USER CLASSSES ~~~~~~~~~~~~~~~~~~~~~~~
    # working- this will create a new driver from user input from the webpage
    # data is written from the static page, returned from the server application and written to the database
    def create(self, data):
        cursor = self.getCursor()
        sql =  "insert into f1drivers (DriverNo, LastName,FirstName,Nationality,CurrentTeam) values (%s,%s,%s,%s,%s)"
        values= [
            data["DriverNo"],
            data["LastName"],
            data["FirstName"],
            data["Nationality"],
            data["CurrentTeam"]
        ]
        cursor.execute(sql,values)
        
        self.connection.commit()
        self.closeAll
        return cursor.lastrowid
        
        
    ## function to return all of the database rows- the array returned is send to the server for writing to the webpage
    def getAll(self):
        cursor = self.getCursor()
        sql = "select * from f1drivers"
        cursor.execute(sql)
        results= cursor.fetchall()
        returnArray = []
        for result in results:
            resultAsDict= self.convertToDict(result)
            returnArray.append(resultAsDict)
        self.closeAll()
        return returnArray

 # function to find a specific row- uses the immutable id to search the database for the full record
    def findById(self,id):
        cursor = self.getCursor()
        sql = "select * from f1drivers where id = %s"
        values = (id,)
        cursor.execute(sql,values)
        result= cursor.fetchone()
        self.closeAll()
        return self.convertToDict(result)

 # function to update an existing object- uses id as the constant object and takes data in from the webpage       

    def update(self,data):
        cursor= self.getCursor()
        sql= "update f1drivers set DriverNo = %s, LastName = %s, FirstName = %s, Nationality = %s, CurrentTeam = %s where id = %s;"
        values= [
            data["DriverNo"],
            data["LastName"],
            data["FirstName"],
            data["Nationality"],
            data["CurrentTeam"],
            data["id"]
        ]
        cursor.execute(sql,values)
        self.connection.commit()
        self.closeAll()
        return data

    # function to delete a row of data
    def delete(self,id):
        cursor = self.getCursor()
        sql = "delete from f1drivers where id = %s"
        values = (id,)

        cursor.execute(sql,values)

        self.connection.commit()
        print("Deletion complete")
        self.closeAll
        return {}


    # function to convert records from the database to a dict so they can be written on the webpage
    def convertToDict(self,result):
        colnames= ["id","DriverNo","LastName","FirstName","Nationality","CurrentTeam"]
        driver = {}
        if result:
            for i, colName in enumerate(colnames):
                value = result[i]
                driver[colName]= value
            return driver


    # Function to create the table - only used once for python anywhere
    def createtable(self):
            cursor = self.getcursor()
            sql="create table f1drivers (id int AUTO_INCREMENT NOT NULL PRIMARY KEY, DriverNo int, LastName varchar(250), FirstName varchar(250), Nationality varchar (250), CurrentTeam(250))"
            cursor.execute(sql)

            self.connection.commit()
            self.closeAll()
    # Function to create a database- only ran once for initialising the database 
    def createdatabase(self):
        self.connection = mysql.connector.connect(
            host=       self.host,
            user=       self.user,
            password=   self.password   
        )
        self.cursor = self.connection.cursor()
        sql="create database "+ self.database
        self.cursor.execute(sql)

        self.connection.commit()
        self.closeAll()


# creates a new class each time the class is run
DriverDAO= driverDAO()    

if __name__== "__main__":

    #MyDAO.createdatabase()
    #MyDAO.createtable()
    print("sanity")


