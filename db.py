import psycopg2
import psycopg2.extras

con = psycopg2.connect(dbname="accountserver", user="accountserveruser", password="accountserveruserpasswordMulberry1!")
cursorfactory = psycopg2.extras.RealDictCursor


def checkusernameexistence(username, email ):
    cur = con.cursor()
    query = "SELECT id FROM users WHERE username = %s"
    cur.execute(query, (username,))
    usernameexistence = cur.fetchone()
    if usernameexistence:
        usernameexistence = True
    else:
        usernameexistence = False
        
    if email:
        cur = con.cursor()
        query = "SELECT id FROM users WHERE email = %s"
        cur.execute(query, (email,))
        emailexistence = cur.fetchone()
        if emailexistence:
            emailexistence = True
        else:
            emailexistence = False
    else:
        emailexistence = False
    
    return (usernameexistence, emailexistence, )

def checklogin(username, password):
    cur = con.cursor()
    cur = con.cursor(cursor_factory=cursorfactory)
    query = "SELECT * FROM users WHERE username = %s AND password = crypt(%s, password);"
    cur.execute(query, (username,password,))
    return cur.fetchone()

def getuserinfo(id):
    cur = con.cursor()
    cur = con.cursor(cursor_factory=cursorfactory)
    query = "SELECT * FROM users WHERE id = %s;"
    cur.execute(query, (id,))
    return cur.fetchone()

def createaccount(username, password, email = None, ip = None):
    cur = con.cursor()  
    if email:
        createquery = "INSERT INTO users (username, email, ip_address_creation, password) VALUES (%s,%s,%s,crypt(%s, gen_salt('bf')));"
        cur.execute(createquery, (username,email,ip,password,))
    else:
        createquery = "INSERT INTO users (username, ip_address_creation, password) VALUES (%s,%s,crypt(%s, gen_salt('bf')));"
        cur.execute(createquery, (username,ip,password,))
    con.commit()
    print('commit!')