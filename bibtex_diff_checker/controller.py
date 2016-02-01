import model
import pymongo
import bibtexparser
from Tkinter import *
import os
import git
from git import Repo
import shutil

class Controller():
    """ This class is used as an interface between the model and the view """    

    def __init__(self,v):
        """initialize view instance and compare the given files"""
        self.view = v
        self.compare_files()        

    def compare_files(self):
        """parse the two bibtex files using bibtex parser and create two bibtex database objects replicate those two databases as unQLite databases collections and compare the records from the local file with records from the master file"""
        self.model = model.Model(self.view.master_file.get(),self.view.local_file.get())
        list_add_prop = []
        list_if_equal = []
        (list_if_equal,list_add_prop) = compare_records(self.model.db_local,self.model.db_master)
        self.view.list_differences(list_if_equal,list_add_prop)

    def update(self,is_update,list_change,list_add):
        """ 
            Update the model and the local file with the user driven modifications and close the controller instance
            Args:
                is_update: Flag indicates if the user made any selections to update the current local file
                list_change: List of properties for each record that have different values on the master file and the local file
                list_add: List of properties for each record that are present on the master file but not on the local
        """    
        self.model.update(is_update,list_change,list_add)
        self.model.update_bibtexDB(is_update)
        self.file_update(is_update)
        self.close()

    def file_update(self,is_update):
        """
            Update the current local file with changes selected by the user
            Args:
                is_update: Flag indicates if the user made any selections to update the current local file            
        """
        if(is_update):
            open(self.view.local_file.get(), 'w').close()
            with open(self.view.local_file.get(), 'w') as bibtex_file:
                bibtex_str = bibtexparser.dumps(self.model.bibdb_local)
                bibtex_file.write(bibtex_str.encode('utf8'))


    def close(self):
        self.view.close()
        
def delete_id (elem):
    """Delete the property '__id' from the dictionary
        Args:
            elem: Dictionary
    """
    for each in elem:
        if(each[0]=="__id"):
            elem.remove(each)
    return elem

def compare_records(coll1,coll2):
    """Compares the records in the unqLite db collection coll1 with the records in collection coll2 and prepares two lists
        Args:
            coll1: Local File MongoDb collection
            coll2: Master File MongoDb collection
        Returns:
            (list1,list2): list1 has records with properties having different values on the two colelctions 
                list2 has records with properties present in coll2 but not in coll1
    """
    tk=Tk()
    list_if_equal=[]
    list_add_prop=[]
    local_list = coll1.all()
    
    for element in local_list:
        result = coll2.filter(lambda obj: obj['ID'] == element["ID"])
        if(len(result)==1):
            master = result[0]
            a = sorted(element.items())
            b = sorted(master.items())
            a= delete_id(a)
            b= delete_id(b)
            for idx,val in enumerate(b):
                value = None    
                for each in a:
                    if (each[0]==b[idx][0]):
                        value = each[1]
                        break
                if (value!=None):                       
                    #if the property exists with a different value 
                    if(b[idx][1]!=value):                            
                        e = (element["ID"],(b[idx][0],value,idx,IntVar()),(b[idx][0],b[idx][1],idx,IntVar()))
                        list_if_equal.append(e)
                else:
                    e = (element["ID"],(b[idx][0],b[idx][1],idx,IntVar()))
                    list_add_prop.append(e)
    tk.destroy() 
    return (list_if_equal,list_add_prop)

def commit_remote(repo,file):
    """ Commits to the index of the local git repository and calls the git push
        Args:
            repo: Reference to the head of the local git repository
            file: File that will be added to the index for the commit and push
                to the remote git repository
        Raises:
            git.exc.GitCommandError: If git.push() fails
    """    
    
    try:
        repo.index.add([file])
        commit = repo.index.commit("Modified File"+file)
        
        for each in repo.heads:
            branch = each
        
        merge_base = repo.merge_base(repo.remotes.origin,branch)
        repo.index.merge_tree(branch,base=merge_base)
        repo.remotes.origin.push()
    
    except git.exc.GitCommandError:
        print "Git Push Error"

#outside        
def create_local_repo(remote_git,dir,branch):
    """ Uses the git.clone_from method to clone a remote git repository locally
        Args:
            remote_git: Url of the remote git repository
            dir: Local directory where the contents of the 
                remote git will be downloaded
            branch: Name of the branch on the remote git which will be used for cloning
        Returns:
            git.repo: Reference to the local git repository
        Raises:
            git.exc.InvalidGitRepositoryError: If remote git repository is bare
            git.exc.GitCommandError: If remote git repository does not exist
    """    

    if(os.path.exists(dir)):
         shutil.rmtree(dir)
    try:
        repo = Repo.clone_from(
                url=remote_git,
                to_path=dir,
                branch=branch            
                )
        if repo.bare:  
            raise git.exc.InvalidGitRepositoryError
        else:
            return repo
        
    except git.exc.GitCommandError:
        print "Please make sure you have the correct access rights and the repository exists"

def extract_bib_files(path):
    """ 
        Extracts all the bib files from the given path
        Args:
            path : The directory name from which bib files will be extracted
        Returns:
            List[string]: Returns a list of bib files present in path
    """    
    list = []
    for root, dirs, files in os.walk(path):
        for name in files:
            if(os.path.join(root, name)).endswith(".bib"):
                list.append(((os.path.join(root, name))))
        for name in dirs:
            if(os.path.join(root, name)).endswith(".bib"):
                list.append(((os.path.join(root, name))))
    return list
