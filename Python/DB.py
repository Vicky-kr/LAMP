from sqlalchemy import Integer, String,Table,Column,MetaData, create_engine,desc
class DB :
    engine = None
    Employees = None
    connection = None
    id = None
    URL = "mysql+pymysql://root:root@localhost/test"

    def __init__(self) :
        self.engine = create_engine(self.URL)
        meta = MetaData()
        self.Employees = Table(
            'employees',meta,
            Column('id',Integer,autoincrement=True,primary_key=True),
            Column('fname',String),
            Column('lname',String),
            Column('role',String)
        )
        meta.create_all(self.engine)
        self.connection = self.engine.connect()
    
    def getAllEmployeesList(self,limit = -1):
        """
        any limit < 0 means it will give all the data
        """
        if limit < 0:
            select = self.Employees.select()
            result = self.connection.execute(select)
            self.engine.dispose()
            return result.fetchall()
        if limit > 0:
            select = self.Employees.select().limit(limit=limit)
            result = self.connection.execute(select)
            self.engine.dispose()
            return result.fetchall()
    
    def getEmployeeByID(self,ID):
        """
        ID argument is compulsory to send
        """
        select = self.Employees.select(whereclause=self.Employees.c.id == ID)
        result = self.connection.execute(select)
        self.engine.dispose()
        return result.fetchone()
    
    def getId(self):
        select = self.Employees.select(self.Employees.c.id).order_by(self.Employees.c.id.desc()).limit(limit=1)
        result  = self.connection.execute(select)
        self.id = result.fetchone()
        return self.id
    
    def addEmployee(self,data):
        """
        send the data in the form of dictionary for e.g {"fname":"Vicky","lname":"Kumar","role":"Emp"}
        """
        if len(data) == 3:
            insert = self.Employees.insert(data)
            self.connection.execute(insert)
            select = self.Employees.select(self.Employees.c.id).order_by(self.Employees.c.id.desc()).limit(limit=1)
            result  = self.connection.execute(select)
            self.id = result.fetchone()[0]
            message =  f"Employee Added to database with ID {self.id}"
        else:
            message = "Please Provide all the details ( i.e. fname, lname & role )"
        
        self.engine.dispose()
        return message
            
    def updateEmployeeDetails(self,ID,data):

        if len(data) > 0 and ID > 0 :
            update = self.Employees.update().where(self.Employees.c.id==ID).values(data)
            self.connection.execute(update)
            self.engine.dispose()
            return f"Updated the Employee details with id = {ID} successfully"
        else:
            return f"Employee with id = {ID} Does not exists"

    def deleteEmployeeById(self,ID):
        """
        ID is mandatory to avoid unintented deletion
        """
        check = self.Employees.select().where(self.Employees.c.id == ID)
        result = self.connection.execute(check)
        message = ""
        if result.fetchone() is None :
            message =  f"Employee with id = {ID} does not exists in database"
        else:
            delete = self.Employees.delete().where(self.Employees.c.id == ID)
            result = self.connection.execute(delete)
            message = f"Employee with id = {ID} was deleted from database successfully"
        self.engine.dispose()
        return message


