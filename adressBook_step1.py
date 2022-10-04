from tkinter import ttk
from tkinter import *
from tkinter import filedialog
import os
from PIL import Image,ImageTk# cmd:  pip install pillow
import sqlite3

#************************************************************************************************************************************


mesProfile={1:""}


#************************************************************************************************************************************

def add_customer():
  name=entryName.get()
  phone=entryPhone.get()
  moreinfo=entryMore.get()
  #create connection
  conn=sqlite3.connect('DataBase.db') 
  cur=conn.cursor()
  cur.execute("INSERT INTO customers(`name`,`phone`,`moreinfo`) values(?,?,?)",(name,phone,moreinfo))
  conn.commit()
  conn.close()
  
 
  conn=sqlite3.connect('DataBase.db') #ouvrir connection
  cur=conn.cursor()   
  select=cur.execute("select * from customers order by id desc")
  select=list(select)
  tree.insert('',END,values=select[0])
  """
  nombreClients = nombreClients + 1
  print("Le nombre de clients est : " , nombreClients )
  """
  conn.close()
  
  
  conn=sqlite3.connect('DataBase.db') #ouvrir connection
  cur=conn.cursor()
  select=cur.execute("select * from customers order by id desc")
  select=list(select)
  id=select[0][0]
  filename=entryPhoto.get()
  
  im=Image.open(filename)
  rgb_img=im.convert('RGB')
  rgb_img.save(("images/profile_"+str(id)+"."+"jpg"))
  conn.close()
  
  
#************************************************************************************************************************************ 
  

def delete_customer():
  
  
  idselect=tree.item(tree.selection())['values'][0]
  conn=sqlite3.connect('DataBase.db') #ouvrir connection
  cur=conn.cursor()
  delete=cur.execute("delete from customers where id={}".format(idselect))
  conn.commit()
  conn.close()
  
  tree.delete(tree.selection())
 


#************************************************************************************************************************************

def sortByName():
  
  
  #clear the treeview
  for x in tree.get_children():
    tree.delete(x)
  
  #*******
  conn=sqlite3.connect('DataBase.db') 
  cur=conn.cursor()   
  select=cur.execute("select * from customers order by name asc")
  conn.commit()
  #remplir treeview
  for row in select:
    tree.insert('',END,values=row) 
  conn.close()
  



#************************************************************************************************************************************


def SearchByName(event):
  
  #clear the treeview
  for x in tree.get_children():
    tree.delete(x)  
    
  name=entrySearchByName.get()
  conn=sqlite3.connect('DataBase.db') 
  cur=conn.cursor()
  select=cur.execute("select * from customers where name=(?)",(name,))
  conn.commit()
  #remplir treeview
  for row in select:
    tree.insert('',END,values=row)   
  conn.close()  
  


#************************************************************************************************************************************    

def SearchByPhone(event):
  #clear the treeview
  for x in tree.get_children():
    tree.delete(x)  
    
  phone_searched=entrySearchByPhone.get()
  conn=sqlite3.connect('DataBase.db') #ouvrir connection
  cur=conn.cursor()
  select=cur.execute("select * from customers where phone=(?)",(phone_searched,))
  conn.commit()
  #remplir treeview
  for row in select:
    tree.insert('',END,values=row)   
  conn.close()  


#************************************************************************************************************************************  
  
def BrowsePhoto():
  entryPhoto.delete(0,END)
  
  filename=filedialog.askopenfilename(initialdir="/",title="select file")
  print(filename)
  entryPhoto.insert(END,filename)
  
  
  
  
#************************************************************************************************************************************

  
def treeActionSelect(event):
  
  #load image
  label_image.destroy()
  
  idSelect=tree.item(tree.selection())['values'][0]
  imgProfile="images/profile_"+str(idSelect)+"."+"jpg"
  #print(imgProfile)
  load=Image.open(imgProfile)
  load.thumbnail((100,100))
  photo=ImageTk.PhotoImage(load)
  
  #remplir le dictionaire par image:
  mesProfile[1]=photo
  
  lblImage=Label(root,image=photo)
  lblImage.place(x=10,y=350)
  
  #recuperer info de user
  nameSelect=tree.item(tree.selection())['values'][1]
  phoneSelect=tree.item(tree.selection())['values'][2]
  moreinfoSelect=tree.item(tree.selection())['values'][3]
  
  lid=Label(root,text="ID : "+str(idSelect))
  lid.place(x=110,y=350)
  lname=Label(root,text="Name : "+str(nameSelect))
  lname.place(x=110,y=380)
  lphone=Label(root,text="Phone : "+str(phoneSelect))
  lphone.place(x=110,y=410)
  Tinfo=Text(root)
  Tinfo.place(x=260,y=360,width=280,height=100)  
  Tinfo.insert(END,"More info : "+moreinfoSelect)
  
  
  
#************************************************************************************************************************************
root=Tk()
root.title("adress book")
root.geometry("550x480")  

#************************************************************************************************************************************

#add title
lblTitle=Label(root,text="Adress Book",font=("Arial",21) ,bg="darkblue",fg="white")
lblTitle.place(x=0,y=0,width=250)

#************************************************************************************************************************************

#search area

lblSearchByName=Label(root,text="search by name",bg="darkblue",fg="white")
lblSearchByName.place(x=250,y=0,width=120)
entrySearchByName=Entry(root)
entrySearchByName.bind("<Return>",SearchByName)
entrySearchByName.place(x=380,y=0,width=160)

lblSearchByPhone=Label(root,text="search by phone",bg="darkblue",fg="white")
lblSearchByPhone.place(x=250,y=20,width=120)
entrySearchByPhone=Entry(root)
entrySearchByPhone.bind("<Return>",SearchByPhone)
entrySearchByPhone.place(x=380,y=20,width=160)

#************************************************************************************************************************************

#label name & surname
lblName=Label(root,text="name & surname",bg="black",fg="yellow")
lblName.place(x=5,y=50,width=125)
entryName=Entry(root)
entryName.place(x=140,y=50,width=400)


#label & entry phone
lblPhone=Label(root,text="Phone number",bg="black",fg="yellow")
lblPhone.place(x=5,y=80,width=125)
entryPhone=Entry(root)
entryPhone.place(x=140,y=80,width=400)

#label & entry photo:
lblPhoto=Label(root,text="Phto",bg="black",fg="yellow")
lblPhoto.place(x=5,y=110,width=125)
bPhoto=Button(root,text="Browse",bg="darkblue",fg="yellow",command=BrowsePhoto)
bPhoto.place(x=480,y=110,height=25)
entryPhoto=Entry(root)
entryPhoto.place(x=140,y=110,width=320)

#more info
lblMore=Label(root,text="More info",bg="black",fg="yellow")
lblMore.place(x=5,y=140,width=125)
entryMore=Entry(root)
entryMore.place(x=140,y=140,width=400)

#************************************************************************************************************************************

#command button

bAdd=Button(root,text="Add Customer",bg="darkblue",fg="yellow",command=add_customer)
bAdd.place(x=5,y=170,width=255)

bDelete=Button(root,text="Delete selected",bg="darkblue",fg="yellow",command=delete_customer)
bDelete.place(x=5,y=205,width=255)

bEdit=Button(root,text="Edit selected",bg="darkblue",fg="yellow")
bEdit.place(x=5,y=240,width=255)

bSort=Button(root,text="Sort By Name",bg="darkblue",fg="yellow",command=sortByName)
bSort.place(x=5,y=275,width=255)

bExit=Button(root,text="Exit App",bg="darkblue",fg="yellow",command=quit)
bExit.place(x=5,y=310,width=255)


#************************************************************************************************************************************

#photo lighada tle3 par defaut
load=Image.open("images/profile.png")
load.thumbnail((130,130))
photo=ImageTk.PhotoImage(load)
label_image=Label(root,image=photo)
label_image.place(x=10,y=340)

#************************************************************************************************************************************


#add treeview
tree=ttk.Treeview(root,columns=(1,2,3),height=5,show="headings")
tree.place(x=265,y=170,width=290,height=175)
      
tree.bind("<<TreeviewSelect>>",treeActionSelect)

# Add scrollbar
vsb = ttk.Scrollbar(root , orient="vertical",command=tree.yview)
vsb.place(x=530, y=200, height=175)
tree.configure(yscrollcommand=vsb.set)

#add headings
tree.heading(1,text="ID")
tree.heading(2,text="Name")
tree.heading(3,text="Phone")

#define column width
tree.column(1,width=50)
tree.column(2,width=100)

#display data in treeview object
conn=sqlite3.connect('DataBase.db')
cur=conn.cursor()
select=cur.execute("select*from customers")
for row in select:
 tree.insert('', END , value=row)#END:inserer la ligne a la fin de l'enregistrement
conn.close()


#************************************************************************************************************************************

root.mainloop()