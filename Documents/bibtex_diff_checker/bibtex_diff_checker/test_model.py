from model import *
from controller import *
import unittest
from unqlite import *

class ModelTest(unittest.TestCase):    
    def test_change_record_db(self):

        list1=[]
        list1.append({u'title': u'Haskino: {H}askell and {A}rduino', u'booktitle': u'Practical Aspects of Declarative Languages', u'author': u'Grebe, Mark and Gill, Andy', 'ID': 'Grebe:15:Haskino', u'year': u'2016', 'ENTRYTYPE': u'inproceedings'})
        list1.append({u'numpages': u'12', u'publisher': u'ACM', u'doi': u'10.1145/2804302.2804311', u'keyword': u'Design Pattern, FFI, Monads, Remote Procedure Call', u'title': u'The Remote Monad Design Pattern', u'xxurl': u'https://www.youtube.com/watch?v=guMLPr6eBLo', u'booktitle': u'Proceedings of the 8th ACM SIGPLAN Symposium on Haskell', u'author': u'Andy Gill and Neil Sculthorpe and Justin Dawson and\nAleksander Eskilson and Andrew Farmer and Mark Grebe\nand Jeffrey Rosenbluth and Ryan Scott and James\nStanton', u'abstract': u'Remote Procedure Calls are expensive.  This paper\ndemonstrates how to reduce the cost of calling\nremote procedures from Haskell by using the\n\\emph{remote monad design pattern}, which amortizes\nthe cost of remote calls.  This gives the Haskell\ncommunity access to remote capabilities that are not\ndirectly supported, at a surprisingly inexpensive\ncost.\n\nWe explore the remote monad design pattern\nthrough six models of remote execution patterns, using a simulated Internet of Things toaster as a\nrunning example.  We consider the expressiveness and\noptimizations enabled by each remote execution\nmodel, and assess the feasibility of our approach.\nWe then present a full-scale case study: a Haskell\nlibrary that provides a Foreign Function Interface\nto the JavaScript Canvas API.  Finally, we discuss\nexisting instances of the remote monad design\npattern found in Haskell libraries.', 'ENTRYTYPE': u'inproceedings', u'link': u'http://dl.acm.org/citation.cfm?id=2804311', u'location': u'Vancouver, BC, Canada', u'xurl': u'http://www.ittc.ku.edu/csdl/fpg/files/Gill-15-RemoteMonad.pdf', 'ID': 'Gill:15:RemoteMonad', u'pages': u'59--70', u'address': u'New York, NY, USA'})             ,

        test_db = UnQLite();
        test_coll = test_db.collection('test')
        test_coll.create()
        test_coll.store(list1)
        
        import Tkinter
        tk = Tk()
        rb = IntVar()
        rb.set(1)
        list2=[]
        list2.append(('Grebe:15:Haskino',('year','2016',1,rb),('year','2017',1,rb)))
        change_property_db(list2,test_coll)

        actual = test_coll.filter(lambda obj : obj["ID"].startswith("Grebe:15:Haskino"))
        expected_year  = '2017'
        assert actual[0]["year"]== expected_year
        
        tk.destroy()

    def test_add_record_db(self):

        list1=[]
        list1.append({u'title': u'Haskino: {H}askell and {A}rduino', u'booktitle': u'Practical Aspects of Declarative Languages', u'author': u'Grebe, Mark and Gill, Andy', 'ID': 'Grebe:15:Haskino', u'year': u'2016', 'ENTRYTYPE': u'inproceedings'})
        list1.append({u'numpages': u'12', u'publisher': u'ACM', u'doi': u'10.1145/2804302.2804311', u'keyword': u'Design Pattern, FFI, Monads, Remote Procedure Call', u'title': u'The Remote Monad Design Pattern', u'xxurl': u'https://www.youtube.com/watch?v=guMLPr6eBLo', u'booktitle': u'Proceedings of the 8th ACM SIGPLAN Symposium on Haskell', u'author': u'Andy Gill and Neil Sculthorpe and Justin Dawson and\nAleksander Eskilson and Andrew Farmer and Mark Grebe\nand Jeffrey Rosenbluth and Ryan Scott and James\nStanton', u'abstract': u'Remote Procedure Calls are expensive.  This paper\ndemonstrates how to reduce the cost of calling\nremote procedures from Haskell by using the\n\\emph{remote monad design pattern}, which amortizes\nthe cost of remote calls.  This gives the Haskell\ncommunity access to remote capabilities that are not\ndirectly supported, at a surprisingly inexpensive\ncost.\n\nWe explore the remote monad design pattern\nthrough six models of remote execution patterns, using a simulated Internet of Things toaster as a\nrunning example.  We consider the expressiveness and\noptimizations enabled by each remote execution\nmodel, and assess the feasibility of our approach.\nWe then present a full-scale case study: a Haskell\nlibrary that provides a Foreign Function Interface\nto the JavaScript Canvas API.  Finally, we discuss\nexisting instances of the remote monad design\npattern found in Haskell libraries.', 'ENTRYTYPE': u'inproceedings', u'link': u'http://dl.acm.org/citation.cfm?id=2804311', u'location': u'Vancouver, BC, Canada', u'xurl': u'http://www.ittc.ku.edu/csdl/fpg/files/Gill-15-RemoteMonad.pdf', 'ID': 'Gill:15:RemoteMonad', u'pages': u'59--70', u'address': u'New York, NY, USA'})             ,

        test_db = UnQLite();
        test_coll = test_db.collection('test')
        test_coll.create()
        test_coll.store(list1)
        
        import Tkinter
        tk = Tk()
        rb = IntVar()
        rb.set(1)
        list2=[]

        list2.append(('Grebe:15:Haskino',('object','Nothing',1,rb)))
        add_property_db(list2,test_coll)

        actual = test_coll.filter(lambda obj : obj["ID"].startswith("Grebe:15:Haskino"))
        expected_prop_val = 'Nothing'
        assert actual[0]['object']== expected_prop_val
        
        tk.destroy()
    def test_update_bibtexDB(self):
        str ="""@inproceedings{Grebe:15:Haskino,
          year={2016},
          booktitle={Practical Aspects of Declarative Languages},
          title={Haskino: {H}askell and {A}rduino},
          author={Grebe, Mark and Gill, Andy}
        }
        """        

        bib_database = bibtexparser.loads(str)
        test_db = UnQLite();
        test_coll = test_db.collection('test')
        test_coll.create()
        test_coll.store(bib_database.entries)

        import Tkinter
        tk = Tk()
        rb = IntVar()
        rb.set(1)


        list2=[]
        list2.append(('Grebe:15:Haskino',('object','Nothing',1,rb)))
        add_property_db(list2,test_coll)
        update_bibtex(True,bib_database,test_coll)

        actual = test_coll.filter(lambda obj : obj["ID"].startswith("Grebe:15:Haskino"))
        expected_prop_val = 'Nothing'
        assert actual[0]["object"]== expected_prop_val

        for elem in bib_database.entries:
            result = elem
        assert result['object']=='Nothing'  

        tk.destroy()
if __name__ == "__main__":
    unittest.main()

