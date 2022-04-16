from Database import *

db =  Database()

#print faces table
#face = db.get_AllFaces()
#print(face)

#db.register_Timestamp(111,'222000','tst')

db2 = Database()
getAllts = db2.get_AllTimestamp(111)
#print(getAllts)

print('\n')

db3 = Database()
getLastts = db3.get_LastTimestamp(111)
#print(getLastts)

employees = db.get_AllEmployees()

print(employees)
