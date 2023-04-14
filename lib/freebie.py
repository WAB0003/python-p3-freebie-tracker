import sqlite3

CONN = sqlite3.connect("./lib/freebies.db")
CURSOR = CONN.cursor()

#! Create Freebies Class
class Freebie():
    def __init__(self, item_name, value, comp_id=None, dev_id=None, id=None):
        self.id = id
        self.item_name = item_name
        self.value = value
        self.comp_id = comp_id
        self.dev_id = dev_id
        
    @property
    def item_name(self):
        return self._item_name
    @item_name.setter
    def item_name(self,new_item_name):
        if type(new_item_name)==str:
            self._item_name = new_item_name
        else:
            raise Exception("Bad Item Name...")
        
    @property
    def dev_id(self):
        return self._dev_id
    @dev_id.setter
    def dev_id(self, dev_id):
        all_devs = CURSOR.execute("SELECT id from devs").fetchall()
        all_ids = [row[0] for row in all_devs]
        if dev_id in all_ids:
            self._dev_id = dev_id
        else:
            raise Exception("No Dev with id provided")
     
        
    #! Create a table that freebies get saved into:
    @classmethod
    def create_table(cls):
        sql = """
            CREATE TABLE IF NOT EXISTS freebies (
                id INTEGER PRIMARY KEY,
                item_name TEXT,
                value INTEGER,
                comp_id INTEGER,
                dev_id INTEGER
            )
        """
        
        CURSOR.execute(sql)
    
    #! Create a drop table to refresh every time code is ran
    @classmethod
    def drop_table(cls):
        sql = "DROP TABLE IF EXISTS freebies"
        CURSOR.execute(sql)
    
    #! Create option to save information to Table once created:
    def save(self):
        sql = """
            INSERT INTO freebies (item_name, value, comp_id, dev_id)
            VALUES (?, ?, ?, ?)
        """
        CURSOR.execute(sql, (self.item_name, self.value, self.comp_id, self.dev_id))
        CONN.commit()
        self.id = CURSOR.lastrowid
    #! Create function that makes instance and saves to database
    @classmethod
    def create(cls,item_name, value, comp_id, dev_id):
        item_name = cls(item_name, value, comp_id, dev_id)
        item_name.save()
        return item_name

        
    #! Create a dev property for frisby.      
    def get_dev(self):
        sql = """
            SELECT * FROM devs
            WHERE id = ?
            LIMIT 1
        """
        found_dev = CURSOR.execute(sql, (self.dev_id,)).fetchone()
        return found_dev
    
    dev = property(get_dev)
    
    #! Create a company property for frisby
    def get_company(self):
        sql = """
            SELECT * FROM companies
            WHERE id = ?
            LIMIT 1
        """
        found_company = CURSOR.execute(sql, (self.comp_id,)).fetchone()
        from company import Company
        return Company.new_from_db(found_company)
    
    company = property(get_company)
    
    
    #! Create an update freebie 
    def update_dev_id(self,new_dev_id):
        sql = """
            UPDATE freebies
            SET dev_id = ?
            WHERE id = ?
        """
        CURSOR.execute(sql, (new_dev_id, self.id))
        CONN.commit()
        
    
    
    #*Aggregate Methods
    def print_details(self):
        print(f"{self.dev[1]} owns a {self.item_name} from {self.company[1]}")
        
        
    
    