import sqlite3

CONN = sqlite3.connect("./lib/freebies.db")
CURSOR = CONN.cursor()

from freebie import Freebie

#* All Dev Table in this color
class Dev():
    def __init__(self, name, id=None):
        self.name = name
        self.id = id
        
    @property
    def name(self):
        return self._name
    
    @name.setter
    def name(self,new_name):
        if type(new_name) == str:
            self._name = new_name
        else:
            print("Name entered is not a string")

    
    #* Create a table that devs get saved into:
    @classmethod
    def create_table(cls):
        sql = """
            CREATE TABLE IF NOT EXISTS devs (
                id INTEGER PRIMARY KEY,
                name TEXT  
            )
        """
        CURSOR.execute(sql)
    
    #* Create a drop table to refresh every time code is ran
    @classmethod
    def drop_table(cls):
        sql = "DROP TABLE IF EXISTS devs"
        CURSOR.execute(sql)
        
    #* Create option to save information to Table once created:
    def save(self):
        sql = """
            INSERT INTO devs (name)
            VALUES (?)
        """
        CURSOR.execute(sql, (self.name,)) #* leave comma in when one item
        CONN.commit()
        self.id = CURSOR.lastrowid
        
    #! Create a freebies property for devs
    def get_freebies(self):
        sql = """
            SELECT * FROM freebies
            WHERE dev_id = ?
        """
        found_freebies = CURSOR.execute(sql, (self.id,)).fetchall()
        return found_freebies
    
    freebies = property(get_freebies)
    
    #! Create a devs property for company
    def get_companies(self):
        sql = """
            SELECT companies.id, companies.name
            FROM companies
            INNER JOIN freebies
            ON companies.id = freebies.comp_id
            WHERE freebies.dev_id = ?
        """
        found_companies = CURSOR.execute(sql, (self.id,)).fetchall()
        return found_companies
    
    companies = property(get_companies)
    
    #* Aggregate Methods
    def received_one(self, item_name):
        all_freebies = [freebie[1].lower() for freebie in self.freebies]
        if item_name.lower() in all_freebies:
            return True
        else:
            return False
        
    def give_away(self, Dev, Freebie):
        if self.id == Freebie.dev_id:
            Freebie.update_dev_id(Dev.id)
            return (f"{Freebie.item_name} now belongs to {Dev.name}")
        else:
            return "Freebie Doesn't Belong to you"
            
        