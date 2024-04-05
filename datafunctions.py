import psycopg2;
import os

dbpass = os.environ.get('dbpass')
def opencon():
    connection = psycopg2.connect(host="localhost",dbname="discordbot",user = "postgres",password=dbpass,port=5432)
    return connection

def closecon(cn):
    cn.close()


def getallvalues():
    opencon()

    cur = connection.cursor()

    cur.execute("""
                SELECT *
                FROM discordusers
            """)


    connection.commit()
    cur.close()
    connection.close()



def updatecoins(amt,user_id):

    conn = opencon()
    cur = conn.cursor()
    cur.execute("""
                UPDATE discordusers
                SET coins = %s
                WHERE id = %s;
                """,(amt,user_id))
    conn.commit()
    cur.close()
    conn.close()

def workadjust(amt,user_id):
    conn = opencon()
    cur = conn.cursor()
    cur.execute("""
                UPDATE discordusers
                SET totalshifts = %s
                WHERE id = %s;
                """,(amt,user_id))
    conn.commit()
    cur.close()
    conn.close()


def checkcoins(user_id):
    cc = opencon()
    cr = cc.cursor()
    cr.execute("""SELECT coins FROM discordusers WHERE id = %s""", (user_id,))
    data = cr.fetchone()  # Fetch the result
    cr.close()
    closecon(cc)
    balance = data[0]
    return balance

def checktotalshifts(user_id):
    cc = opencon()
    cr = cc.cursor()
    cr.execute("""SELECT totalshifts FROM discordusers WHERE id = %s""", (user_id,))
    data = cr.fetchone()  # Fetch the result
    cr.close()
    closecon(cc)
    totalshifts = data[0]
    return totalshifts

def userdbcheck(user_id):
    if not userexists(user_id):
        adduser(user_id)



def adduser(user_id):
    conn = opencon()
    cur = conn.cursor()
    # Assuming a very simple table structure; adjust as necessary.
    cur.execute("INSERT INTO discordusers (id, coins) VALUES (%s, %s);", (user_id, 0))
    conn.commit()
    cur.close()
    conn.close()



def userexists(user_id):
    conn = opencon()
    cur = conn.cursor()
    cur.execute("SELECT EXISTS(SELECT 1 FROM discordusers WHERE id = %s);", (user_id,))
    exists = cur.fetchone()[0]
    cur.close()
    conn.close()
    return exists