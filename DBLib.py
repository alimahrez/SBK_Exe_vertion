import sqlite3

def DB_connection():
    #create table for administrators
    DBConnection = sqlite3.connect('SBK.db')
    DBCursor = DBConnection.cursor()
    DBCursor.execute("""CREATE TABLE administrators (
        user_name text,
        pass_wd text)""")
    DBConnection.commit()
    DBConnection.close()
    
    #create table for Agents
    DBConnection = sqlite3.connect('SBK.db')
    DBCursor = DBConnection.cursor()
    DBCursor.execute("""CREATE TABLE agents (
        agent_id integer,
        agent_name text,
        agent_account text,
        agent_shift text,
        break_time integer,
        break_status text,
        break_out text,
        break_in text )""")
    DBConnection.commit()
    DBConnection.close()

def DB_Insert_Agent(id,name) :
    if DB_Agent_exist(id) :
        return False
    else :
        DBConnection = sqlite3.connect('SBK.db')
        DBCursor = DBConnection.cursor()
        DBCursor.execute("INSERT INTO agents VALUES (?,?,?,?,?,?,?,?)",(id,name,'x','x',0,'Red','00:00','00:00'))
        DBConnection.commit()
        DBConnection.close()
        return True

def DB_Push():
    DBConnection = sqlite3.connect('SBK.db')
    DBCursor = DBConnection.cursor()
    Volume_Agents = [
                        (2001,"Mohamed El-Saaed",'x','x',0,'Red','00:00','00:00'),
                        (2003,"Ali Sabry",'x','x',0,'Red','00:00','00:00'),
                        (2005,"Ezeis Hassan Mousa",'x','x',0,'Red','00:00','00:00'),
                        (2007,"Khloud Khaled",'x','x',0,'Red','00:00','00:00'),
                        (2008,"George Emad",'x','x',0,'Red','00:00','00:00'),
                        (2014,"Mohamed Ibrahim",'x','x',0,'Red','00:00','00:00'),
                        (2015,"Ali Osama",'x','x',0,'Red','00:00','00:00'),
                        (2016,"Mohamed Yasser",'x','x',0,'Red','00:00','00:00'),
                        (2018,"Mohamed Shaaban",'x','x',0,'Red','00:00','00:00'),
                        (2019,"Ali Ali",'x','x',0,'Red','00:00','00:00'),
                        (2020,"Ibrahim Mohamed",'x','x',0,'Red','00:00','00:00'),
                        (2021,"Karim Saber",'x','x',0,'Red','00:00','00:00'),
                        (2022,"Mostafa Mohamed",'x','x',0,'Red','00:00','00:00'),
                        (2024,"Nour Ramadan",'x','x',0,'Red','00:00','00:00'),
                        (2026,"Mohamed Reda",'x','x',0,'Red','00:00','00:00'),
                        (2028,"Walid Ahmed",'x','x',0,'Red','00:00','00:00'),
                        (2030,"Hesham Hussin",'x','x',0,'Red','00:00','00:00'),
                        (2034,"Mahmed Abdelftah",'x','x',0,'Red','00:00','00:00'),
                        (2039,"Donia Shreif",'x','x',0,'Red','00:00','00:00'),
                        (2040,"Hussin Tarek",'x','x',0,'Red','00:00','00:00'),
                        (2041,"Mostafa Samah",'x','x',0,'Red','00:00','00:00'),
                        (2042,"Abd El Rahman  Sayed",'x','x',0,'Red','00:00','00:00'),
                    ]
    DBCursor.executemany("INSERT INTO agents VALUES (?,?,?,?,?,?,?,?)",Volume_Agents)
    DBConnection.commit()
    DBConnection.close()

def DB_Add_Mastr_Record():
    DBConnection = sqlite3.connect('SBK.db')
    DBCursor = DBConnection.cursor()
    DBCursor.execute("INSERT INTO administrators VALUES ('ali','8090100')")
    DBConnection.commit()
    DBConnection.close()

def DB_Add_Admin_Record(username,passwd):
    DBConnection = sqlite3.connect('SBK.db')
    DBCursor = DBConnection.cursor()
    DBCursor.execute("INSERT INTO administrators VALUES (?,?)",(username,passwd))
    DBConnection.commit()
    DBConnection.close()

def DB_Read_Record_administrators():
    DBConnection = sqlite3.connect('SBK.db')
    DBCursor = DBConnection.cursor()
    DBCursor.execute("SELECT * FROM administrators")
    print(DBCursor.fetchall())
    DBConnection.commit()
    DBConnection.close()

def DB_Read_Record_agents():
    DBConnection = sqlite3.connect('SBK.db')
    DBCursor = DBConnection.cursor()
    DBCursor.execute("SELECT * FROM agents")
    print(DBCursor.fetchall())
    DBConnection.commit()
    DBConnection.close()

def DB_Read_All_DB():#------------------
    Dict = {}
    DBConnection = sqlite3.connect('SBK.db')
    DBCursor = DBConnection.cursor()
    DBCursor.execute("SELECT * FROM agents")
    for user in DBCursor.fetchall() :
        Dict[user[0]] = [user[1],user[2],user[3],user[4],user[5],user[6],user[7]]
    DBConnection.commit()
    DBConnection.close()
    return Dict

def DB_User_Passwd_Chick(username,passwd):
    ChickmyTuple = (username,passwd)
    DBConnection = sqlite3.connect('SBK.db')
    DBCursor = DBConnection.cursor()
    DBCursor.execute("SELECT * FROM administrators")
    for user in DBCursor.fetchall() :
        if ChickmyTuple == user :
            DBConnection.commit()
            DBConnection.close()
            return True
    DBConnection.commit()
    DBConnection.close()
    return False

def DB_Agent_exist(id):
    DBConnection = sqlite3.connect('SBK.db')
    DBCursor = DBConnection.cursor()
    DBCursor.execute("SELECT * FROM agents")
    for user in DBCursor.fetchall() :
        if id in user :
            DBConnection.commit()
            DBConnection.close()
            return True
    DBConnection.commit()
    DBConnection.close()
    return False

def DB_Delete_Agent(ext) :
    DBConnection = sqlite3.connect('SBK.db')
    DBCursor = DBConnection.cursor()
    DBCursor.execute("DELETE from agents WHERE agent_id=?",(ext,))
    DBConnection.commit()
    DBConnection.close()

def DB_Update_Break_Time(Id,Value) :
    DBConnection = sqlite3.connect('SBK.db')
    DBCursor = DBConnection.cursor()
    DBCursor.execute("UPDATE agents SET break_time=? WHERE agent_id=?",(Value,Id,))
    DBConnection.commit()
    DBConnection.close()