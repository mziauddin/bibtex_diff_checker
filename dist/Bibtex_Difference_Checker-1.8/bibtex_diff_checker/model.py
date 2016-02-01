import bibtexparser
import Tkinter as tk        
from Tkinter import *
from ttk import *
import Tkinter, Tkconstants, tkFileDialog
from unqlite import UnQLite

class Model():
    """Creates and maintains UnQLite and Bibtex databases"""
    def __init__(self,master,local):
        """define  UnQLite database"""        
        db = UnQLite()
        """ define collection where we'll insert local files content"""
        self.db_local = db.collection('db_local')
        self.db_local.create()
        """ define collection where we'll insert master files content"""
        self.db_master = db.collection('db_master')
        self.db_master.create()

        with open(local) as bibtex_file:
            bibtex_str = bibtex_file.read()

        """create bibtex database for local file"""
        self.bibdb_local = bibtexparser.loads(bibtex_str)             
        self.db_local.store(self.bibdb_local.entries)

        with open(master) as bibtex_file:
            bibtex_str = bibtex_file.read()

        """create bibtex database for master file"""
        bibdb_master = bibtexparser.loads(bibtex_str)             
        self.db_master.store(bibdb_master.entries)
        

    def update_bibtexDB(self,is_update):
        """Update the bibtex database with the records from the unQLite database
            Args:
                is_update:Flag indicates if the user made any selections to update the current local file
        """
        update_bibtex(is_update,self.bibdb_local,self.db_local)

    def update(self,is_update,list_change,list_add):
        """Update the unQLite collections
            Args:
                is_update:Flag indicates if the user made any selections to update the current local file
                list_change: List of properties for each record that have different values on the master file and the local file
                list_add: List of properties for each record that are present on the master file but not on the local
        """
        if(is_update):
            change_property_db(list_change,self.db_local)
            add_property_db(list_add,self.db_local)
        

def change_property_db(list, db_coll):
    """Update the records in the database collection with the modified values from the list
        Args:
            list: List of properties for each record that have different values on the master file and the local file
            db_coll: database collection that will to be updated
    """
    for idx,val in enumerate(list):
        if (list[idx][2][3].get()):
            record =  db_coll.filter(lambda obj: obj['ID'].startswith(list[idx][0]))
            record[0][list[idx][1][0]] = list[idx][2][1]
            db_coll.update(record[0]['__id'], record[0])                        

def add_property_db(list,db_coll):
    """Update the records in the database collection with the values from the list
        Args:
            list: List of properties for each record that are present on the master file but not on the local
            db_coll: database collection that will to be updated
    """
    for idx,val in enumerate(list):
            record =  db_coll.filter(lambda obj: obj['ID'].startswith(list[idx][0]))
            record[0][list[idx][1][0]] = list[idx][1][1]
            db_coll.update(record[0]['__id'], record[0])                        


def update_bibtex(is_update,bibdatabase,db_coll):
    """Updates the bibtex database by comparing the properties for each record with records from the unQLite database
        Args:
            is_update:Flag indicates if the user made any selections to update the current local file
            bibdatabase: Bibtex database that needs to be updated
            db_coll:Mongo database collection 
    """
    if(is_update):  
        for dict in bibdatabase.entries:
            change = False 
            if dict.has_key("_id"):
                dict.pop("_id")
            record =  db_coll.filter(lambda obj: obj['ID'].startswith(dict["ID"]))
            if(len(record)>0):
                for each in record[0].items():
                    if(each[0]!="__id"):
                        dict[each[0]]=each[1]

