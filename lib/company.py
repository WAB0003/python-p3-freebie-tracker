import sqlite3
from freebie import Freebie

CONN = sqlite3.connect("./lib/freebies.db")
CURSOR = CONN.cursor()

class Company():
    def __init__(self, name, founding_year, id=None):
        self.name = name
        self.founding_year = founding_year
        self.id = id
    
    # Create a table that companies get saved into:
    @classmethod
    def create_table(cls):
        sql = """
            CREATE TABLE IF NOT EXISTS companies (
                id INTEGER PRIMARY KEY,
                name TEXT,
                founding_year INTEGER  
            )
        """
        CURSOR.execute(sql)
    
    # Create a drop table to refresh every time code is ran
    @classmethod
    def drop_table(cls):
        sql = "DROP TABLE IF EXISTS companies"
        CURSOR.execute(sql)
        
    # Create option to save information to Table once created:
    def save(self):
        sql = """
            INSERT INTO companies (name, founding_year)
            VALUES (?, ?)
        """
        CURSOR.execute(sql, (self.name, self.founding_year))
        CONN.commit()
        self.id = CURSOR.lastrowid
        
    #! Create a freebies property for company
    def get_freebies(self):
        sql = """
            SELECT * FROM freebies
            WHERE comp_id = ?
        """
        found_freebies = CURSOR.execute(sql, (self.id,)).fetchall()
        return found_freebies
    
    freebies = property(get_freebies)
    
    #! Create a devs property for company
    def get_devs(self):
        sql = """
            SELECT devs.id, devs.name
            FROM devs
            INNER JOIN freebies
            ON devs.id = freebies.dev_id
            WHERE freebies.comp_id = ?
        """
        found_devs = CURSOR.execute(sql, (self.id,)).fetchall()
        return found_devs
    
    devs = property(get_devs)
    
    
    #*Aggregate Methods
    def give_freebie(self,Dev,item_name,value):
        item_name = Freebie.create(item_name,value,self.id,Dev.id)
        return item_name
        
    @classmethod
    def oldest_company(cls):
        sql = """
            SELECT *
            FROM companies
            ORDER BY founding_year 
            ASC LIMIT 1    
        """
        oldest_comp = CURSOR.execute(sql).fetchone()
        return oldest_comp
        
        