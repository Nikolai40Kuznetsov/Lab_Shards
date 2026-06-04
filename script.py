import pymssql
import credits as cr

conn = pymssql.connect(cr.server, cr.user, cr.password, cr.db)
cursor = conn.cursor()

cursor.execute ("""
    USE test3 

    select Students_uutw66.FIO, Students_uutw66.BD, Students_uutw66.Grade, Teacher_uutw66.FIO from Students_uutw66    
        JOIN Classes_uutw66 ON Students_uutw66.Grade = Classes_uutw66.Grade
        JOIN Teacher_uutw66 ON Classes_uutw66.Grade = Teacher_uutw66.Grades 
        where Teacher_uutw66.FIO = 'Dick'                                      
"""
)


print(cursor.fetchall())
conn.commit()
conn.close()