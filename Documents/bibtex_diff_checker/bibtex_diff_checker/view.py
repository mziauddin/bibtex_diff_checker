import Tkinter as tk        
from Tkinter import *
import controller
import os
import git
from git import Repo
import shutil
import Tkinter, Tkconstants, tkFileDialog

class View(tk.Frame):
    """ ..class:: View
            This class is used for getting user inputs. It uses the tkinter GUI package. 
            ..data::master_file    
                StringVar() variable holds the name of the master file
            ..data::local_file
                StringVar() variable holds the name of the local file
            ..data::master_path
                StringVar() variable holds the name of the directory which holds the master file
            ..data::local_path
                StringVar() variable holds the name of the directory which holds the local file            
    """
    def __init__(self, *args, **kwargs):
        """This method creates a window for the user to select whether his files are on disk or git"""
        tk.Frame.__init__(self, *args, **kwargs)
        self.option = IntVar()
        self.master_file = StringVar()
        self.local_file = StringVar()
        self.master_path = os.getcwd()+"/"+"testing_01"  
        self.local_path = os.getcwd()+"/"+"testing_02"        
        Radiobutton(self, text = "Files on Disk",variable = self.option,value = 1).grid(row = 0, column = 1)
        Radiobutton(self, text = "Files on Git",variable = self.option, value = 2).grid(row = 1, column = 1)
        ok_button = Button(self,text = "Submit",command = self.choose_option)
        ok_button.grid(columnspan=2)

    def openmasterfile(self,event):
        """method is used to select a file from the local hard disk"""
        self.master_file.set(tkFileDialog.askopenfilename()) 

    def openlocalfile(self,event):
        """method is used to select a file from the local hard disk"""
        self.local_file.set(tkFileDialog.askopenfilename())            

    def choose_option(self):
        """check for the option user selected and help the user select his files"""
        if(self.option.get()==1):
            self.select_disk_files()
        else:
            self.select_git_files()

    def select_disk_files(self):
        """create a new window to input the two repositories from which the two bibtex files will be selected"""        
        def onFrameConfigure(canvas):
    #'''Reset the scroll region to encompass the inner frame'''
            canvas.configure(scrollregion=canvas.bbox("all"))        
        new_window = tk.Toplevel(self)
        canvas = tk.Canvas(new_window, borderwidth=0, background="#ffffff")
        window = tk.Frame(canvas, background="#ffffff") 
        vsb = tk.Scrollbar(new_window, orient="vertical", command=canvas.yview)   
        hsb = tk.Scrollbar(new_window, orient="horizontal", command=canvas.xview)
        canvas.configure(xscrollcommand = hsb.set,yscrollcommand=vsb.set)
        vsb.pack(side="right", fill="y")
        hsb.pack(side="top", fill="x")
        canvas.pack(side="left", fill="both", expand=True)
        canvas.create_window((4,4), window=window, anchor="nw")     
        window.bind("<Configure>", lambda event, canvas=canvas: onFrameConfigure(canvas))
        label_1 = Label(window, text = "Local File")
        label_2 = Label(window, text = "Master File")
        master_file_entry = Entry(window, textvariable=self.master_file)
        master_file_entry.bind("<Button-1>", self.openmasterfile)
        local_file_entry = Entry(window, textvariable=self.local_file)
        local_file_entry.bind("<Button-1>", self.openlocalfile)
        label_1.grid(row = 0,sticky=E)
        label_2.grid(row = 1,sticky=E)
        master_file_entry.grid(row = 0, column = 1)
        local_file_entry.grid(row=1,column=1)
        ok_button = Button(window,text = "Submit",command = self.call_controller)
        ok_button.grid(columnspan=2)

    def select_git_files(self):
        """creates a new window and accepts the names of the two git repositories to be used by the application"""
        master_repo = StringVar()
        local_repo = StringVar()
        branch_name_master = StringVar()
        branch_name_local = StringVar()
        def onFrameConfigure(canvas):
            '''Reset the scroll region to encompass the inner frame'''
            canvas.configure(scrollregion=canvas.bbox("all"))
        new_window = tk.Toplevel(self)
        canvas = tk.Canvas(new_window, borderwidth=0, background="#ffffff")
        window = tk.Frame(canvas, background="#ffffff") 
        vsb = tk.Scrollbar(new_window, orient="vertical", command=canvas.yview)   
        hsb = tk.Scrollbar(new_window, orient="horizontal", command=canvas.xview)
        canvas.configure(xscrollcommand = hsb.set,yscrollcommand=vsb.set)
        vsb.pack(side="right", fill="y")
        hsb.pack(side="top", fill="x")
        canvas.pack(side="left", fill="both", expand=True)
        canvas.create_window((4,4), window=window, anchor="nw")     
        window.bind("<Configure>", lambda event, canvas=canvas: onFrameConfigure(canvas))
        label_1 = Label(window, text = "Git Repo 1")
        label_2 = Label(window, text = "Git Repo 2")
        label_3 = Label(window, text = "Branch_Name")
        label_4 = Label(window, text = "Branch_Name")
        r1 = Entry(window, textvariable=master_repo)
        br_master = Entry(window, textvariable=branch_name_master)
        r2 = Entry(window, textvariable=local_repo)
        br_local = Entry(window, textvariable=branch_name_local)
        text = master_repo.get()
        master_repo.set(text)
        text = local_repo.get()
        local_repo.set(text)
        label_1.grid(row = 0,sticky=E)
        label_4.grid(row = 1,sticky=E)
        label_2.grid(row = 2,sticky=E)
        label_3.grid(row = 3,sticky=E)
        r1.grid(row = 0, column = 1)
        br_master.grid(row=1,column=1)        
        r2.grid(row=2,column=1)
        br_local.grid(row=3,column=1)        
        ok_button = Button(window,text = "Submit",command =lambda: self.select_files(master_repo.get(),local_repo.get(),branch_name_master.get(),branch_name_local.get()))
        ok_button.grid(columnspan=2)
    
    def select_files(self,repo1,repo2,branch1,branch2):
        """given the names of two repositories and their branch names this method creates a local repository and pulls down the content from git"""       
        if(os.path.exists(self.master_path)):
             shutil.rmtree(self.master_path)
        self.repo_master = create_local_repo(repo1,self.master_path,branch1)
        if(os.path.exists(self.local_path)):
             shutil.rmtree(self.local_path)
        self.repo_local = create_local_repo(repo2,self.local_path,branch2)
        self.repo_master.remotes.origin.pull()
        self.repo_local.remotes.origin.pull()
        self.select_rb_files()
        
    def select_rb_files(self):
        """creates a window which list the different bibtex files present in the local directories of both the master and local repositories """        
        def onFrameConfigure(canvas):
            '''Reset the scroll region to encompass the inner frame'''
            canvas.configure(scrollregion=canvas.bbox("all"))
        new_window = tk.Toplevel(self)
        canvas = tk.Canvas(new_window, borderwidth=0, background="#ffffff")
        window = tk.Frame(canvas, background="#ffffff") 
        vsb = tk.Scrollbar(new_window, orient="vertical", command=canvas.yview)   
        hsb = tk.Scrollbar(new_window, orient="horizontal", command=canvas.xview)
        canvas.configure(xscrollcommand = hsb.set,yscrollcommand=vsb.set)
        vsb.pack(side="right", fill="y")
        hsb.pack(side="top", fill="x")
        canvas.pack(side="left", fill="both", expand=True)
        canvas.create_window((4,4), window=window, anchor="nw")     
        window.bind("<Configure>", lambda event, canvas=canvas: onFrameConfigure(canvas))
        self.list_master_repo = extract_bib_files(self.master_path)
        self.list_local_repo = extract_bib_files(self.local_path)
        line = 0            #line variable holds the current row number on the gui for our grid formatting
        if(len(self.list_master_repo)>0):
            Label(window,text="Select the master file",font=("Times", 16),foreground="Blue").grid(row = line+1,columnspan=2,sticky=W,padx=2,pady=2)
            for idx,val in enumerate(self.list_master_repo):
                line = line+1
                Radiobutton(window, text=self.list_master_repo[idx],variable=self.master_file,value = self.list_master_repo[idx]).grid(row=line+1,column=0,sticky=W,padx=1,pady=1)
        line = line+2
        if(len(self.list_local_repo)>0):
            Label(window,text="Select the local file",font=("Times", 16),foreground="Blue").grid(row = line+1,columnspan=2,sticky=W,padx=1,pady=1)
            for idx,val in enumerate(self.list_local_repo):
                line = line+1
                Radiobutton(window, text=self.list_local_repo[idx],variable=self.local_file,value = self.list_local_repo[idx]).grid(row=line+1,column=0,sticky=W,padx=1,pady=1)
        Button(window, text="Done", command=self.call_controller).grid(columnspan=2,sticky=W,padx=1,pady=1)

    def list_differences(self,list,list2):
        """create a window to display the differences between the two files as two categories: one shows the differences between values of
            the two properties for a record and the other shows the property present in the master file but not in the local file
            Args:
                list: list of record that have a difference in properties on the master file and the local file
                list2:list of record that have a property on the master file which is not present on the local file
        """                    
        def onFrameConfigure(canvas):
            '''Reset the scroll region to encompass the inner frame'''
            canvas.configure(scrollregion=canvas.bbox("all"))
        new_window = tk.Toplevel(self)
        canvas = tk.Canvas(new_window, borderwidth=0, background="#ffffff")
        window = tk.Frame(canvas, background="#ffffff") 
        vsb = tk.Scrollbar(new_window, orient="vertical", command=canvas.yview)   
        hsb = tk.Scrollbar(new_window, orient="horizontal", command=canvas.xview)
        canvas.configure(xscrollcommand = hsb.set,yscrollcommand=vsb.set)
        vsb.pack(side="right", fill="y")
        hsb.pack(side="top", fill="x")
        canvas.pack(side="left", fill="both", expand=True)
        canvas.create_window((4,4), window=window, anchor="nw")     
        window.bind("<Configure>", lambda event, canvas=canvas: onFrameConfigure(canvas))
        line = 0
        if(len(list)>0):
            current_elem = list[0][0]
            Label(window,text="There is a difference in the below properties for the master and local file",font=("Times", 16),foreground="Blue").grid(columnspan=2,sticky=W,padx=2,pady=2)
            for idx,val in enumerate(list):
                line = line+1
                new_elem = list[idx][0]
                if(new_elem!=current_elem or idx==0):
                    Label(window,text="ID:"+current_elem,font=("Times", 14,"bold")).grid(row=line+1,sticky=W,padx=1,pady=1)
                    current_elem=new_elem
                    line = line +1
                Label(window,text=list[idx][1][0]+":").grid(row=line+1,column=0,sticky=W,padx=1,pady=1)
                Label(window, text=list[idx][1][1]).grid(row=line+1,column=1,sticky=W,padx=1,pady=1)
                Label(window,text=list[idx][2][0]+":").grid(row=line+1,column=2,sticky=W,padx=1,pady=1)
                Radiobutton(window, text=list[idx][2][1],variable=list[idx][2][3],value = 1).grid(row=line+1,column=3,sticky=W,padx=1,pady=1)
        line = line+2
        if(len(list2)>0):
            Label(window,text="Below property is not present in the local file",font=("Times", 16),foreground="Blue").grid(row = line,columnspan=2,sticky=W,padx=1,pady=1)
            Label(window,text="Select properties you want to add",font=("Times", 16),foreground="Blue").grid(row = line+1,columnspan=2,sticky=W,padx=1,pady=1)
            line = line +2
            current_elem = list2[0][0]    
            for idx,val in enumerate(list2):
                line = line+1
                new_elem = list2[idx][0]
                if(new_elem!=current_elem or idx==0):
                    Label(window,text="ID:"+current_elem,font =("Times", 14,"bold")).grid(row=line+1,columnspan=2,sticky=W,padx=1,pady=1)
                    current_elem=new_elem
                    line = line+1
                Label(window,text=list2[idx][1][0]+":").grid(row=line+1,sticky=W,padx=1,pady=1)
                Radiobutton(window, text=list2[idx][1][1],variable=list2[idx][1][3],value = 1).grid(row=line+1,column=1,sticky=W,padx=1,pady=1)
        self.update = True
        if(len(list)==0 and len(list2)==0):
            Label(window,text="No differences between the two files",font=("Times", 16),foreground="Blue").grid(row = line,columnspan=2,sticky=W,padx=1,pady=1)
            self.update = False
        Button(window, text="Done", command=lambda:self.controller.update(self.update,list,list2)).grid(columnspan=2,sticky=W,padx=1,pady=1)
        
    def call_controller(self):
        """Create the controller instance """
        self.controller = controller.Controller(self)        

    def close(self):
        """deletes the instance of View , commits the new added features to the local file to the remote repository and deletes all the temporary directories
            that were created for this application """
        if(self.option.get()==2):         
            commit_remote(self.repo_local,self.local_file.get())
            shutil.rmtree(self.master_path)
            shutil.rmtree(self.local_path)        
        self.destroy()
        root_close()
    
if __name__ == "__main__":
    root = tk.Tk()
    view = View(root)
    view.pack(side="top", fill="both", expand=True)    
    def root_close():
        root.destroy()

    root.mainloop()