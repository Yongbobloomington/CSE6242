########################### DO NOT MODIFY THIS SECTION ##########################
#################################################################################
import sqlite3
from sqlite3 import Error
import csv
#################################################################################

## Change to False to disable Sample
SHOW = False

############### SAMPLE CLASS AND SQL QUERY ###########################
######################################################################
class Sample():
    def sample(self):
        try:
            connection = sqlite3.connect("sample")
            connection.text_factory = str
        except Error as e:
            print("Error occurred: " + str(e))
        print('\033[32m' + "Sample: " + '\033[m')
        
        # Sample Drop table
        connection.execute("DROP TABLE IF EXISTS sample;")
        # Sample Create
        connection.execute("CREATE TABLE sample(id integer, name text);")
        # Sample Insert
        connection.execute("INSERT INTO sample VALUES (?,?)",("1","test_name"))
        connection.commit()
        # Sample Select
        cursor = connection.execute("SELECT * FROM sample;")
        print(cursor.fetchall())

######################################################################

class HW2_sql():
    ############### DO NOT MODIFY THIS SECTION ###########################
    ######################################################################
    def create_connection(self, path):
        connection = None
        try:
            connection = sqlite3.connect(path)
            connection.text_factory = str
        except Error as e:
            print("Error occurred: " + str(e))
    
        return connection

    def execute_query(self, connection, query):
        cursor = connection.cursor()
        try:
            if query == "":
                return "Query Blank"
            else:
                cursor.execute(query)
                connection.commit()
                return "Query executed successfully"
        except Error as e:
            return "Error occurred: " + str(e)
    ######################################################################
    ######################################################################

    # GTusername [0 points]
    def GTusername(self):
        gt_username = "rmutombo3"
        return gt_username
    
    # Part a.i Create Tables [2 points]
    def part_ai_1(self,connection):
        ############### EDIT SQL STATEMENT ###################################
        part_ai_1_sql = "CREATE TABLE movies(id INTEGER, title TEXT, score REAL);"
        ######################################################################
        
        return self.execute_query(connection, part_ai_1_sql)

    def part_ai_2(self,connection):
        ############### EDIT SQL STATEMENT ###################################
        part_ai_2_sql = """CREATE TABLE movie_cast(movie_id INTEGER, 
        cast_id INTEGER, cast_name TEXT, birthday TEXT, popularity REAL);"""
        ######################################################################
        
        return self.execute_query(connection, part_ai_2_sql)
    
    # Part a.ii Import Data [2 points]
    def part_aii_1(self,connection,path):
        ############### CREATE IMPORT CODE BELOW ############################
        with open('data/movies.csv') as f:
            rows = csv.reader(f, delimiter=',')
            for row in rows:
                 title = row[1]
                 title = title.replace(',', '')
                 title = str(title).encode(encoding='ascii',errors='ignore').decode()
                 title = title.replace("'", ' ')
                 sql ="INSERT INTO movies VALUES(" + row[0] + ", '" + title + "', " + row[2] + ");"
                 cursor = connection.execute(sql)

       ######################################################################
        
        sql = "SELECT COUNT(id) FROM movies;"
        cursor = connection.execute(sql)
        return cursor.fetchall()[0][0]
    
    def part_aii_2(self,connection, path):
        ############### CREATE IMPORT CODE BELOW ############################
        with open('data/movie_cast.csv') as f:
            rows = csv.reader(f, delimiter=',')
            for row in rows:
                 name = row[2]
                 name = name.replace(',', '')
                 name = str(name).encode(encoding='ascii',errors='ignore').decode()
                 name = name.replace("'", ' ')
                 sql ="INSERT INTO movie_cast VALUES(" + row[0] + ", " + row[1] + ", '" + name + "', '" +  row[3] + "', " + row[4] + ");"
                 cursor = connection.execute(sql)
        ######################################################################
        
        sql = "SELECT COUNT(cast_id) FROM movie_cast;"
        cursor = connection.execute(sql)
        return cursor.fetchall()[0][0]

    # Part a.iii Vertical Database Partitioning [5 points]
    def part_aiii(self,connection):
        ############### EDIT CREATE TABLE SQL STATEMENT ###################################
        part_aiii_sql = """CREATE TABLE cast_bio(cast_id INTEGER, 
                         cast_name TEXT, birthday TEXT, popularity REAL);"""
        ######################################################################
        
        self.execute_query(connection, part_aiii_sql)
        
        ############### CREATE IMPORT CODE BELOW ############################
        part_aiii_insert_sql = """INSERT INTO cast_bio SELECT DISTINCT cast_id, 
                                   cast_name, birthday, popularity FROM movie_cast;"""
        ######################################################################
        
        self.execute_query(connection, part_aiii_insert_sql)
        
        sql = "SELECT COUNT(cast_id) FROM cast_bio;"
        cursor = connection.execute(sql)
        return cursor.fetchall()[0][0]
       

    # Part b Create Indexes [1 points]
    def part_b_1(self, connection):
        ############### EDIT SQL STATEMENT ###################################
        part_b_1_sql = "CREATE UNIQUE INDEX movie_index ON movies(id);"
        ######################################################################
        return self.execute_query(connection, part_b_1_sql)
    
    def part_b_2(self,connection):
        ############### EDIT SQL STATEMENT ###################################
        part_b_2_sql = "CREATE INDEX cast_index ON movie_cast(cast_id);"
        ######################################################################
        return self.execute_query(connection, part_b_2_sql)
    
    def part_b_3(self,connection):
        ############### EDIT SQL STATEMENT ###################################
        part_b_3_sql = "CREATE UNIQUE INDEX cast_bio_index ON cast_bio(cast_id)"
        ######################################################################
        return self.execute_query(connection, part_b_3_sql)
    
    # Part c Calculate a Proportion [3 points]
    def part_c(self,connection):
        ############### EDIT SQL STATEMENT ###################################
        part_c_sql = """select printf('%.2f', (SELECT (select cast((count(id) * 100) as real) 
                        FROM movies WHERE LOWER(title) LIKE '%war%' 
                        AND score > CAST(50 as REAL))/cast(count(*) as real) from movies));"""
        ######################################################################
        cursor = connection.execute(part_c_sql)
        return cursor.fetchall()[0][0]

    # Part d Find the Most Prolific Actors [4 points]
    def part_d(self,connection):
        ############### EDIT SQL STATEMENT ###################################
        part_d_sql =  """SELECT cast_name, COUNT(movie_id) AS appearance_count 
                         FROM movie_cast 
                         WHERE popularity > CAST(10 as real)           
                         GROUP BY cast_id
                         ORDER BY appearance_count DESC , cast_name ASC 
                         LIMIT 5;"""
        ######################################################################
        cursor = connection.execute(part_d_sql)
        return cursor.fetchall()

    # Part e Find the Highest Scoring Movies With the Least Amount of Cast [4 points]
    def part_e(self,connection):
        ############### EDIT SQL STATEMENT ###################################
        part_e_sql = """SELECT movies.title, printf('%.2f', movies.score), 
                     COUNT(movie_cast.cast_id) AS cast_count FROM movies
                     INNER JOIN movie_cast 
                     ON movies.id = movie_cast.movie_id
                     GROUP BY movies.id
                     ORDER BY movies.score DESC, cast_count ASC, movies.title ASC
                     LIMIT 5;"""
        ######################################################################
        cursor = connection.execute(part_e_sql)
        return cursor.fetchall()
    
    # Part f Get High Scoring Actors [4 points]
    def part_f(self,connection):
        ############### EDIT SQL STATEMENT ###################################
        part_f_sql = """SELECT movie_cast.cast_id, movie_cast.cast_name, 
                     printf('%.2f', avg(movies.score)) AS average_score
                     FROM movies INNER JOIN movie_cast 
                     ON movies.id = movie_cast.movie_id 
                     WHERE movies.score >= CAST(25 as real)
                     GROUP BY movie_cast.cast_id
                     HAVING COUNT(movie_cast.movie_id) > 2
                     ORDER BY AVG(movies.score) DESC, movie_cast.cast_name ASC
                     LIMIT 10;"""


        ######################################################################
        cursor = connection.execute(part_f_sql)
        return cursor.fetchall()

    # Part g Creating Views [6 points]
    def part_g(self,connection):
        ############### EDIT SQL STATEMENT ###################################

        part_g_sql = """create view good_collaboration(
                 cast_member_id1, cast_member_id2, movie_count, average_movie_score)
                 as
                 select t1.cast_id as cast_member_id1,
                      t2.cast_id as cast_member_id2, 
                      count(t1.movie_id) as movie_count,
                      avg(t3.score) as average_movie_score
                      from movie_cast as t1 
                      inner join movie_cast as t2 on t1.movie_id = t2.movie_id
                      inner join movies as t3 on t1.movie_id = t3.id 
                      where t1.cast_id < t2.cast_id
                      group by t1.cast_id, t2.cast_id
                      having movie_count > 2 and average_movie_score >= cast(40 as real);"""

        ######################################################################
        return self.execute_query(connection, part_g_sql)
    
    def part_gi(self,connection):
        ############### EDIT SQL STATEMENT ###################################

        part_g_i_sql = """select cast_member_id1, cast_bio.cast_name, 
                             printf('%.2f', avg(average_movie_score)) as collaboration_score
                          from good_collaboration 
                             inner join cast_bio
                                 on cast_bio.cast_id = cast_member_id1
                          group by cast_member_id1
                order by collaboration_score desc, cast_bio.cast_name asc
                limit 5;"""
 
        ######################################################################
        cursor = connection.execute(part_g_i_sql)
        return cursor.fetchall()
    
    # Part h FTS [4 points]
    def part_h(self,connection,path):
        ############### EDIT SQL STATEMENT ###################################
        part_h_sql = """CREATE VIRTUAL TABLE movie_overview 
               USING FTS4 (id INTEGER, overview TEXT);"""
        ######################################################################
        connection.execute(part_h_sql)
        ############### CREATE IMPORT CODE BELOW ############################
        with open('data/movie_overview.csv') as f:
            rows = csv.reader(f, delimiter=',')
            for row in rows:
                 id = row[0]
                 id = str(row[0]).encode(encoding='ascii',errors='ignore').decode()
                 overview = row[1].replace(',', '')
                 overview = str(overview).encode(encoding='ascii',errors='ignore').decode()
                 overview = overview.replace("'", ' ')
                 sql ="INSERT INTO movie_overview VALUES(" + id + ", '" + overview + "');"
                 cursor = connection.execute(sql)  
                 
        ######################################################################
        sql = "SELECT COUNT(id) FROM movie_overview;"
        cursor = connection.execute(sql)
        return cursor.fetchall()[0][0]
        
    def part_hi(self,connection):
        ############### EDIT SQL STATEMENT ###################################

        part_hi_sql = """SELECT COUNT(overview) FROM movie_overview WHERE 
                 overview MATCH 'fight';"""
        ######################################################################
        cursor = connection.execute(part_hi_sql)
        return cursor.fetchall()[0][0]
    
    def part_hii(self,connection):
        ############### EDIT SQL STATEMENT ###################################
        part_hii_sql = """SELECT COUNT(overview) FROM movie_overview WHERE 
                 overview MATCH 'space NEAR/5 program';"""
        ######################################################################
        cursor = connection.execute(part_hii_sql)
        return cursor.fetchall()[0][0]


if __name__ == "__main__":
    
    ########################### DO NOT MODIFY THIS SECTION ##########################
    #################################################################################
    if SHOW == True:
        sample = Sample()
        sample.sample()

    print('\033[32m' + "Q2 Output: " + '\033[m')
    db = HW2_sql()
    try:
        conn = db.create_connection("Q2")
    except:
        print("Database Creation Error")

    try:
        conn.execute("DROP TABLE IF EXISTS movies;")
        conn.execute("DROP TABLE IF EXISTS movie_cast;")
        conn.execute("DROP TABLE IF EXISTS cast_bio;")
        conn.execute("DROP VIEW IF EXISTS good_collaboration;")
        conn.execute("DROP TABLE IF EXISTS movie_overview;")
    except:
        print("Error in Table Drops")

    try:
        print('\033[32m' + "part ai 1: " + '\033[m' + str(db.part_ai_1(conn)))
        print('\033[32m' + "part ai 2: " + '\033[m' + str(db.part_ai_2(conn)))
    except:
         print("Error in Part a.i")

    try:
        print('\033[32m' + "Row count for Movies Table: " + '\033[m' + str(db.part_aii_1(conn,"data/movies.csv")))
        print('\033[32m' + "Row count for Movie Cast Table: " + '\033[m' + str(db.part_aii_2(conn,"data/movie_cast.csv")))
    except:
        print("Error in part a.ii")

    try:
        print('\033[32m' + "Row count for Cast Bio Table: " + '\033[m' + str(db.part_aiii(conn)))
    except:
        print("Error in part a.iii")

    try:
        print('\033[32m' + "part b 1: " + '\033[m' + db.part_b_1(conn))
        print('\033[32m' + "part b 2: " + '\033[m' + db.part_b_2(conn))
        print('\033[32m' + "part b 3: " + '\033[m' + db.part_b_3(conn))
    except:
        print("Error in part b")

    try:
        print('\033[32m' + "part c: " + '\033[m' + str(db.part_c(conn)))
    except:
        print("Error in part c")

    try:
        print('\033[32m' + "part d: " + '\033[m')
        for line in db.part_d(conn):
            print(line[0],line[1])
    except:
        print("Error in part d")

    try:
        print('\033[32m' + "part e: " + '\033[m')
        for line in db.part_e(conn):
            print(line[0],line[1],line[2])
    except:
        print("Error in part e")

    try:
        print('\033[32m' + "part f: " + '\033[m')
        for line in db.part_f(conn):
            print(line[0],line[1],line[2])
    except:
        print("Error in part f")
    
    try:
        print('\033[32m' + "part g: " + '\033[m' + str(db.part_g(conn)))
        print('\033[32m' + "part g.i: " + '\033[m')
        for line in db.part_gi(conn):
            print(line[0],line[1],line[2])
    except:
        print("Error in part g")

    try:   
        print('\033[32m' + "part h.i: " + '\033[m'+ str(db.part_h(conn,"data/movie_overview.csv")))
        print('\033[32m' + "Count h.ii: " + '\033[m' + str(db.part_hi(conn)))
        print('\033[32m' + "Count h.iii: " + '\033[m' + str(db.part_hii(conn)))
    except:
        print("Error in part h")

    conn.close()
    #################################################################################
    #################################################################################
  
