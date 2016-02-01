from controller import *
from unqlite import *
import unittest

class ControllerTest(unittest.TestCase):
    def test_compare_records(self):
            list1=[]
            list1.append({u'title': u'Haskino: {H}askell and {A}rduino', u'booktitle': u'Practical Aspects of Declarative Languages', u'author': u'Grebe, Mark and Gill, Andy', 'ID': 'Grebe:15:Haskino', u'year': u'2016', 'ENTRYTYPE': u'inproceedings'})
            list1.append({u'numpages': u'12', u'publisher': u'ACM', u'doi': u'10.1145/2804302.2804311', u'keyword': u'Design Pattern, FFI, Monads, Remote Procedure Call', u'title': u'The Remote Monad Design Pattern', u'xxurl': u'https://www.youtube.com/watch?v=guMLPr6eBLo', u'booktitle': u'Proceedings of the 8th ACM SIGPLAN Symposium on Haskell', u'author': u'Andy Gill and Neil Sculthorpe and Justin Dawson and\nAleksander Eskilson and Andrew Farmer and Mark Grebe\nand Jeffrey Rosenbluth and Ryan Scott and James\nStanton', u'abstract': u'Remote Procedure Calls are expensive.  This paper\ndemonstrates how to reduce the cost of calling\nremote procedures from Haskell by using the\n\\emph{remote monad design pattern}, which amortizes\nthe cost of remote calls.  This gives the Haskell\ncommunity access to remote capabilities that are not\ndirectly supported, at a surprisingly inexpensive\ncost.\n\nWe explore the remote monad design pattern\nthrough six models of remote execution patterns, using a simulated Internet of Things toaster as a\nrunning example.  We consider the expressiveness and\noptimizations enabled by each remote execution\nmodel, and assess the feasibility of our approach.\nWe then present a full-scale case study: a Haskell\nlibrary that provides a Foreign Function Interface\nto the JavaScript Canvas API.  Finally, we discuss\nexisting instances of the remote monad design\npattern found in Haskell libraries.', 'ENTRYTYPE': u'inproceedings', u'link': u'http://dl.acm.org/citation.cfm?id=2804311', u'location': u'Vancouver, BC, Canada', u'xurl': u'http://www.ittc.ku.edu/csdl/fpg/files/Gill-15-RemoteMonad.pdf', 'ID': 'Gill:15:RemoteMonad', u'pages': u'59--70', u'address': u'New York, NY, USA'})             ,
            
            list2=[]
            list2.append({u'title': u'Haskino: {H}askell and {A}rduino', u'booktitle': u'Practical Aspects of Declarative Languages', u'author': u'Grebe, Mark and Gill, Andy', 'ID': 'Grebe:15:Haskino', u'year': u'2015', 'ENTRYTYPE': u'inproceedings'})
            list2.append({u'numpages': u'12', u'publisher': u'ACM', u'doi': u'10.1145/2804302.2804311', u'keyword': u'Design Pattern, FFI, Monads, Remote Procedure Call', u'title': u'The Remote Monad Design Pattern', u'xxurl': u'https://www.youtube.com/watch?v=guMLPr6eBLo', u'booktitle': u'Proceedings of the 8th ACM SIGPLAN Symposium on Haskell', u'author': u'Andy Gill and Neil Sculthorpe and Justin Dawson and\nAleksander Eskilson and Andrew Farmer and Mark Grebe\nand Jeffrey Rosenbluth and Ryan Scott and James\nStanton', u'abstract': u'Remote Procedure Calls are expensive.  This paper\ndemonstrates how to reduce the cost of calling\nremote procedures from Haskell by using the\n\\emph{remote monad design pattern}, which amortizes\nthe cost of remote calls.  This gives the Haskell\ncommunity access to remote capabilities that are not\ndirectly supported, at a surprisingly inexpensive\ncost.\n\nWe explore the remote monad design pattern\nthrough six models of remote execution patterns, using a simulated Internet of Things toaster as a\nrunning example.  We consider the expressiveness and\noptimizations enabled by each remote execution\nmodel, and assess the feasibility of our approach.\nWe then present a full-scale case study: a Haskell\nlibrary that provides a Foreign Function Interface\nto the JavaScript Canvas API.  Finally, we discuss\nexisting instances of the remote monad design\npattern found in Haskell libraries.', 'ENTRYTYPE': u'inproceedings', u'link': u'http://dl.acm.org/citation.cfm?id=2804311', u'location': u'Vancouver, BC, Canada', u'xurl': u'http://www.ittc.ku.edu/csdl/fpg/files/Gill-15-RemoteMonad.pdf', u'year': u'2015','ID': 'Gill:15:RemoteMonad', u'pages': u'59--70', u'address': u'New York, NY, USA'})
            

            test_db = UnQLite();
            test_coll1 = test_db.collection('test_coll1')
            test_coll1.create()
            test_coll1.store(list1)
            test_coll2 = test_db.collection('test_coll2')
            test_coll2.create()
            test_coll2.store(list2)            
            
            list1 = []
            list2 = []
            (list1,list2) = compare_records(test_coll1,test_coll2)
            assert len(list1)==1
            assert len(list2)==1
                        
    def test_delete_id(self):
            dict1 = dict()
            dict1.update({u'title': u'Haskino: {H}askell and {A}rduino', u'booktitle': u'Practical Aspects of Declarative Languages',u'__id':u'1234'})
            result = delete_id((dict1.items()))
            assert len(result)==2
            
    def test_positive_create_local_repo(self):
        import os
        git_url = "https://github.com/mziauddin/Bibtex-File-Comparison-and-Update.git"
        branch = "master"
        path = os.getcwd()+"/"+"clone_remote"  
        repo = create_local_repo(git_url,path,branch)
        assert not repo.bare
        shutil.rmtree(path)

    def test_negative_create_local_repo(self):

        import sys
        import os
        from StringIO import StringIO

        saved_stdout = sys.stdout
        try:
            out = StringIO()
            sys.stdout = out
#this is a fake git url            
            git_url = "https://github.com/mziauddin/Bibtex-File-Comparison.git"
            branch = "master"
            path = os.getcwd()+"/"+"clone_remote"              
            create_local_repo(git_url,path,branch)
            output = out.getvalue().strip()
            assert output == 'Please make sure you have the correct access rights and the repository exists'
        finally:
            sys.stdout = saved_stdout
            
    def test_negative_extract_bib_files(self):
#this is a fake directory
        import os        
        path = os.getcwd()+"/"+"no_dir" 
        result = extract_bib_files(path)
        assert not result
        
    def test_positive_extract_bib_files(self):
#create a dir
    
        import os
        directory = os.getcwd()+"/"+"bib_files"
        if not (os.path.exists(directory)):
            os.mkdir(directory)
           
        filename1 = "test1.bib"
        with open(os.path.join(directory, filename1), 'wb') as temp_file:
            temp_file.write("")
        filename2 = "test2.bib"        
        with open(os.path.join(directory, filename2), 'wb') as temp_file:
            temp_file.write("")
        
        expected = [directory+"/"+filename1,directory+"/"+filename2]    
        result = extract_bib_files(directory)
        assert len(result)==2
        assert sorted(expected) == sorted(result)
        shutil.rmtree(directory)
        
    def test_commit_remote(self):
        import os
        git_url = "https://github.com/mziauddin/Bibtex-File-Comparison-and-Update.git"
        branch = "master"
        path = os.getcwd()+"/"+"clone_remote"  
        repo = create_local_repo(git_url,path,branch)
        filename1 = "test1.bib"
        with open(os.path.join(path, filename1), 'wb') as temp_file:
            temp_file.write("")
        commit_remote(repo,path+"/"+filename1)            
        
if __name__ == "__main__":
    unittest.main()