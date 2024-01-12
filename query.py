import sqlite3
import bcrypt
from datetime import datetime

# Connect to the SQLite database
conn = sqlite3.connect("SmartRestaurant.db")
cursor = conn.cursor()


def print_all_from_pinaka(name):
    query = "SELECT * FROM " + name
    cursor.execute(query)
    rows = cursor.fetchall()
    for row in rows:
        print(row)


def tuple_to_list(list):
    return [item[0] for item in list]  # [(1,), (2,), (3,), ... -> [1, 2, 3, ...


def getdatetime():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def hash_password(password):
    # Hash a password using bcrypt
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    return hashed_password


# Function to check if a candidate password matches a hashed password
def check_password(candidate_password, hashed_password):
    return bcrypt.checkpw(candidate_password.encode('utf-8'), hashed_password)


# Function to check if the provided username and password are valid
def check_user(myusername, mypassword):
    query = "SELECT username, password FROM PELATIS WHERE username = ?"
    cursor.execute(query, (myusername,))
    result = cursor.fetchone()

    if result:
        stored_username = result[0]  # Assuming username is stored in the first column
        stored_password_hash = result[1]  # Assuming password is stored in the second column
        if stored_username == myusername and check_password(mypassword, stored_password_hash):
            return 1  # Username and password are correct
    return 0  # Username or password is incorrect


def check_if_user_exists(username, email):
    cursor.execute('''
        SELECT username, email FROM PELATIS
    ''')
    results = cursor.fetchall()
    for item in results:
        if item[0] == username:
            return "Username is already used! Please try another username, or sign up if you already have an account."
        elif item[1] == email:
            return "Email is already used! Please try another email, or sign up if you already have an account."


# insert new customer
def insert_user(name, lastname, phone, mail, username=None, password=None):
    query = "INSERT INTO PELATIS (onoma, eponimo, tilefono, email, username, password) VALUES(?,?,?,?,?,?)"
    cursor.execute(query, (name, lastname, phone, mail, username, hash_password(password)))
    conn.commit()


# insert_user("Nektaria", "Zevgoula", "6969696969", "nektaroazev@gmail.com", "nektar", "nektar12345")
# print(check_user("nektar", "nektar145"))
# inserts kritiki to database
def insert_kritiki(bathmologia, perigrafi, id_pelati):
    try:
        query = "INSERT INTO KRITIKI (id, bathmologia, perigrafi, imerominia, id_pelati) VALUES(NULL,?,?,?,?)"
        cursor.execute(query, (bathmologia, perigrafi, getdatetime(), id_pelati))
        conn.commit()
    except Exception as e:
        print("Error " + str(e))


def get_all_food():
    query = "SELECT onoma FROM FAGITO"
    cursor.execute(query)
    results = cursor.fetchall()
    return [t[0] for t in results]


def get_all_drinks():
    query = "SELECT onoma FROM POTO"
    cursor.execute(query)
    results = cursor.fetchall()
    return [t[0] for t in results]


def get_all_tables():
    return ['a1', 'a2', 'a3', 'a4', 'a5', 'b1', 'b2', 'b3', 'b4', 'b5', 'c1', 'c2', 'c3', 'c4', 'c5']


def get_id_from_fagito(name):
    query = "SELECT onoma, id_fagitoy FROM FAGITO"
    cursor.execute(query)
    results = cursor.fetchall()
    try:
        for row in results:
            if row[0] == name:
                return row[1]
    except Exception as e:
        print("Error " + str(e))


def get_id_from_poto(name):
    query = "SELECT onoma, id_potoy FROM POTO"
    cursor.execute(query)
    results = cursor.fetchall()
    try:
        for row in results:
            if row[0] == name:
                return row[1]
    except Exception as e:
        print("Error " + str(e))


def get_onoma_from_id_fagitoy(id_fagitoy):
    cursor.execute('''
        SELECT onoma FROM FAGITO WHERE id_fagitoy = ?
    ''', (id_fagitoy,))
    return cursor.fetchone()[0]


def get_onoma_from_id_potoy(id_potoy):
    cursor.execute('''
        SELECT onoma FROM POTO WHERE id_potoy = ?
    ''', (id_potoy,))
    return cursor.fetchone()[0]


def get_id_from_yliko(name):
    query = "SELECT onoma, id_ylikoy FROM YLIKA"
    cursor.execute(query)
    results = cursor.fetchall()
    for row in results:
        if row[0] == name:
            return row[1]


# enter date+ time, get tables that are free for that time
def free_tables(date, time):
    free_table_list = get_all_tables()
    date_time = date + " " + time
    cursor.execute(
        '''
        SELECT id_trapeziou, imera_ora FROM KRATISI
        '''
    )
    results = cursor.fetchall()

    for row in results:
        if date_time == (row[1])[8:]:
            if row[0] in free_table_list:
                try:
                    free_table_list.remove(row[0])
                except:
                    pass

    return free_table_list


def insert_kratisi(id_pelati, imera_ora, arithmos_atomon, id_trapeziou):
    cursor.execute('''
        INSERT INTO KRATISI(id_kratisis, imera_ora, arithmos_atomon, id_trapeziou)
        VALUES(NULL,?,?, ?)
    ''', (imera_ora, arithmos_atomon, id_trapeziou))
    conn.commit()

    cursor.execute('''
        SELECT id_kratisis
        FROM KRATISI
        ORDER BY id_kratisis DESC
        LIMIT 1;
    ''')
    result = cursor.fetchone()
    id_kratisis = result[0]
    cursor.execute('''
        INSERT INTO KANEI(id_pelati, id_kratisis)
        VALUES(?,?)
            ''', (id_pelati, id_kratisis))
    conn.commit()


# ta dedomena auta ta trexeis mia fora mono:)
'''insert_kratisi("1", "2024-01-01 20:00:00", "4", "a1")
insert_kratisi("2", "2024-01-01 20:00:00", "3", "a2")
insert_kratisi("3", "2024-01-01 21:00:00", "4", "a3")
insert_kratisi("4", "2024-01-01 21:00:00", "2", "a4")
insert_kratisi("7", "2024-01-02 20:00:00", "4", "a1")
insert_kratisi("8", "2024-01-02 20:00:00", "4", "b1")
insert_kratisi("10", "2024-01-02 20:00:00", "3", "b2")
insert_kratisi("12", "2024-01-02 21:00:00", "4", "b3")
insert_kratisi("1", "2024-02-01 20:00:00", "4", "a1")'''


# return kratisis for a given day
# Sto gui make sure days form 1-9 are given in 01-09 form
def kratisi_for_day(daytime):
    mylist = []
    query = "SELECT id_kratisis, imera_ora FROM KRATISI"
    cursor.execute(query)
    results = cursor.fetchall()
    for row in results:
        if daytime == (row[1])[8:10]:
            mylist.append(row)
    counter = len(mylist)

    return counter, mylist  # returns number of kratisis + the tuple imera+ora of kratisis for a given day


def get_kratisi_from_pelati(id_pelati):
    cursor.execute('''
            SELECT KANEI.id_pelati, KANEI.id_kratisis, KRATISI.imera_ora
            FROM KANEI
            INNER JOIN KRATISI ON KANEI.id_kratisis = KRATISI.id_kratisis
            WHERE KANEI.id_pelati = ?
        ''', (id_pelati,))

    results = cursor.fetchall()
    # mexri edw epistrefei oles tis kratisis  apo pelati

    for row in results:
        if row[2] < getdatetime():
            results.remove(row)

    return results  # returns tuple (id_pelati, id_kratisi, imerominia kratisis > currentdatetime)


def delete_kratisi(id_pelati, id_kratisis):
    try:
        cursor.execute("DELETE FROM KANEI WHERE id_pelati = ? AND id_kratisis = ?", (id_pelati, id_kratisis))
        cursor.execute("DELETE FROM KRATISI WHERE id_kratisis = ?", (id_kratisis))
        conn.commit()
        print("Row deleted successfully")
    except sqlite3.Error as e:
        print(f"Error deleting row: {e}")

    conn.commit()


def insert_proion_to_perilambanei(id_paraggelias, id_fagitoy=None, id_potoy=None):
    cursor.execute('''
            INSERT INTO PERILAMBANEI (id_paraggelias, id_fagitoy, id_potoy, id_perilambanei)
            VALUES (?, ?, ?, NULL)
        ''', (id_paraggelias, id_fagitoy, id_potoy))
    conn.commit()


def calculate_kostos(id_paraggelias):
    kostos = 0
    cursor.execute('''
        SELECT id_fagitoy from PERILAMBANEI WHERE id_paraggelias = ?
    ''', (id_paraggelias,))
    food = tuple_to_list(cursor.fetchall())
    food = [item for item in food if item is not None]
    cursor.execute('''
            SELECT id_potoy from PERILAMBANEI WHERE id_paraggelias = ?
        ''', (id_paraggelias,))
    drinks = tuple_to_list(cursor.fetchall())
    drinks = [item for item in drinks if item is not None]

    for item in food:
        item = get_onoma_from_id_fagitoy(item)
        cursor.execute('''
            SELECT kostos from FAGITO
            WHERE onoma = ?
        ''', (item,))
        result = cursor.fetchone()
        if result is not None and result[0] is not None:
            kostos += float(result[0])

    for item in drinks:
        item = get_onoma_from_id_potoy(item)
        cursor.execute('''
            SELECT kostos from POTO
            WHERE onoma = ?
        ''', (item,))
        result = cursor.fetchone()
        if result is not None and result[0] is not None:
            kostos += float(result[0])
    print("Value: " + str(kostos))
    return str(kostos)


def set_kostos_in_paraggelia(id_paraggelias):
    cursor.execute('''
        UPDATE PARAGGELIA SET kostos = ? WHERE id_paraggelias = ?
    ''', (calculate_kostos(id_paraggelias), id_paraggelias))
    conn.commit()


def insert_into_paraggelia(id_paraggelias, newfoods=None, newdrinks=None):
    if newfoods != None:
        for item in newfoods:
            insert_proion_to_perilambanei(id_paraggelias, get_id_from_fagito(item), None)
    if newdrinks != None:
        for item in newdrinks:
            insert_proion_to_perilambanei(id_paraggelias, None, get_id_from_poto(item))
    set_kostos_in_paraggelia(id_paraggelias)


def insert_paraggelia(id_trapeziou, food, drinks):
    imer_ora = getdatetime()
    cursor.execute('''
        INSERT INTO PARAGGELIA (id_paraggelias, imer_ora, kostos, id_trapeziou)
        VALUES (NULL, ?, ?, ?)
    ''', (imer_ora, None, id_trapeziou))
    conn.commit()
    id_paraggelias = cursor.lastrowid
    set_kostos_in_paraggelia(id_paraggelias)
    insert_into_paraggelia(id_paraggelias, food, drinks)


def get_id_paraggelias_from_trapezi(id_trapeziou):
    cursor.execute('''
        SELECT id_paraggelias from PARAGGELIA WHERE id_trapeziou = ?
    ''', (id_trapeziou,))
    return (cursor.fetchone())[0]


def delete_paraggelia(id_paraggelias):
    try:
        cursor.execute("DELETE FROM PARAGGELIA WHERE id_paraggelias = ? ", (id_paraggelias,))
        cursor.execute("DELETE FROM PERILAMBANEI WHERE id_paraggelias = ?", (id_paraggelias,))
        conn.commit()
        print("Row deleted successfully")
    except sqlite3.Error as e:
        print(f"Error deleting row: {e}")

    conn.commit()


def delete_proion_from_perilambanei(id_paraggelias, id_fagitoy=None, id_potoy=None):
    try:
        # Check and delete based on id_fagitoy
        if id_fagitoy is not None:
            cursor.execute('''
                SELECT id_perilambanei
                FROM PERILAMBANEI
                WHERE id_paraggelias = ? AND id_fagitoy = ?
                LIMIT 1
            ''', (id_paraggelias, id_fagitoy))
            row_to_delete = cursor.fetchone()

            if row_to_delete:
                cursor.execute('''
                    DELETE FROM PERILAMBANEI
                    WHERE id_perilambanei = ?
                ''', (row_to_delete[0],))
                conn.commit()

        # Check and delete based on id_potoy
        if id_potoy is not None:
            cursor.execute('''
                SELECT id_perilambanei
                FROM PERILAMBANEI
                WHERE id_paraggelias = ? AND id_potoy = ?
                LIMIT 1
            ''', (id_paraggelias, id_potoy))
            row_to_delete = cursor.fetchone()

            if row_to_delete:
                cursor.execute('''
                    DELETE FROM PERILAMBANEI
                    WHERE id_perilambanei = ?
                ''', (row_to_delete[0],))
                conn.commit()

        print("Row successfully deleted from PERILAMBANEI")
    except Exception as e:
        print("Error: " + str(e))


def remove_from_paraggelia(id_paraggelias, delfoods=None, deldrinks=None):
    for item in delfoods:
        delete_proion_from_perilambanei(id_paraggelias, get_id_from_fagito(item))
    for item in deldrinks:
        delete_proion_from_perilambanei(id_paraggelias, None, get_id_from_poto(item))


# remove_from_paraggelia("12", ["Fries"], ["Water"])


def get_kratiseis():
    cursor.execute('''
        SELECT KRATISI.id_kratisis, KRATISI.imera_ora, KRATISI.arithmos_atomon, PELATIS.onoma, PELATIS.eponimo
        FROM PELATIS
        JOIN KANEI ON PELATIS.id_pelati = KANEI.id_pelati
        JOIN KRATISI ON KRATISI.id_kratisis = KANEI.id_kratisis
        WHERE KRATISI.imera_ora > ?
    ''', (getdatetime(),))
    result = cursor.fetchall()
    return result


'''def get_fagito_poto_from_paraggelia(id_paraggelias):
    food = []
    drinks = []
    cursor.execute(
        SELECT id_fagitoy, id_potoy FROM PERILAMBANEI WHERE id_paraggelias = ?
    , (id_paraggelias,))
    results = cursor.fetchall()
    for item in results:
        if item[0] is not None:
            food.append(get_onoma_from_id_fagitoy(item[0]))
        if item[1] is not None:
            drinks.append(get_onoma_from_id_potoy(item[1]))
    
    return food, drinks'''


def get_fagito_poto_from_paraggelia(id_paraggelias):
    cursor.execute('''
        SELECT onoma FROM FAGITO
        JOIN PERILAMBANEI ON FAGITO.id_fagitoy = PERILAMBANEI.id_fagitoy 
        WHERE id_paraggelias = ?
    ''', (id_paraggelias,))
    fagito = cursor.fetchall()
    cursor.execute('''
            SELECT onoma FROM POTO
            JOIN PERILAMBANEI ON POTO.id_potoy = PERILAMBANEI.id_potoy 
            WHERE id_paraggelias = ?
        ''', (id_paraggelias,))
    poto = cursor.fetchall()
    return fagito, poto


def kerdi_for_day(day):
    kerdi = 0
    cursor.execute('''
        SELECT kostos FROM PARAGGELIA
        WHERE strftime('%Y-%m-%d', imer_ora) = ?
    ''', (day,))
    results = cursor.fetchall()
    kerdi = sum(float(item[0]) for item in results if item[0] is not None)
    return kerdi


print(kerdi_for_day('2024-01-01'))


def kerdi_for_month(month):
    kerdi = 0
    cursor.execute('''
        SELECT kostos FROM PARAGGELIA
        WHERE strftime('%Y-%m', imer_ora) = ?
    ''', (month,))
    results = cursor.fetchall()
    kerdi = sum(float(item[0]) for item in results if item[0] is not None)
    return kerdi


print(kerdi_for_month('2024-01'))


def top5_pelatis_names():
    cursor.execute('''
        SELECT PELATIS.onoma, PELATIS.eponimo, COUNT(KANEI.id_pelati) as pelatis_count
        FROM PELATIS
        JOIN KANEI ON PELATIS.id_pelati = KANEI.id_pelati
        GROUP BY KANEI.id_pelati
        ORDER BY pelatis_count DESC
        LIMIT 10
    ''')

    results = cursor.fetchall()

    for item in results:
        print(f"Name: {item[0]} {item[1]}, Number of reservations: {item[2]}")


# Example usage
top5_pelatis_names()

def top5_drinks():
    pass

def top5_foods():
    pass

'''
def top10_biggest_spenders():
    cursor.execute(
        SELECT PELATIS.id_pelati, PELATIS.onoma, PELATIS.eponimo, SUM(PARAGGELIA.kostos) as total_spending
        FROM PELATIS
        JOIN KANEI ON PELATIS.id_pelati = KANEI.id_pelati
        JOIN KRATISI ON KANEI.id_kratisis = KRATISI.id_kratisis
        JOIN TRAPEZI ON KRATISI.id_trapeziou = TRAPEZI.id_trapeziou
        JOIN PARAGGELIA ON KRATISI.id_trapeziou = PARAGGELIA.id_trapeziou
        GROUP BY PELATIS.id_pelati
        ORDER BY total_spending DESC
        LIMIT 10
    )

    results = cursor.fetchall()

    for item in results:
        print(f"id_pelati: {item[0]}, Name: {item[1]} {item[2]}, Total Spending: {item[3]}")

    conn.close()


# Example usage
top10_biggest_spenders()

'''
