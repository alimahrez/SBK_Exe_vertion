import time
from tkinter import *
from tkinter import messagebox
from PIL import Image,ImageTk
from tkinter import ttk
from DBLib import *
import xlsxwriter
import webbrowser


# The Global important variables
MainDB = {}
IdDB = list()
UpdateDB = {}
Name        = 0
Account     = 1
Shift       = 2
BreakTime   = 3
BreakStatus = 4
BreakOut    = 5
BreakIn     = 6

DeleteCheckBox = list()
init_row = 0
Number_Of_User_Break = 0

def callback(url):
    webbrowser.open_new(url)

def Init_MainDB() :
    global MainDB
    MainDB = DB_Read_All_DB()

def Clear_MainDB() :
    MainDB.clear()

def Init_IdDB() :
    global IdDB
    for user in MainDB :
        IdDB.append(user)

def Clear_IdDB():
    IdDB.clear()

def CurrentTime():
    T = [int(time.strftime("%H")),int(time.strftime("%M")),time.strftime("%P")]
    return T

def CurrentDate():
    Date = time.strftime("%D")
    return Date

def Data_Time_Print():
    WeekDay = time.strftime("%a")
    Day = time.strftime("%d")
    Month = time.strftime("%m")
    Hour = time.strftime("%I")
    Min  = time.strftime("%M")
    FullDateVersion = f"({WeekDay}_{Day}_{Month}) ({Hour}_{Min})"
    return FullDateVersion

def Clear_List(CopyList) :
    CopyList.clear()

def raise_frame(frame):
    frame.tkraise()

def submit_click(frame) :
    if (adminname.get() == "") and (adminpassword.get() == "") and (con_adminpassword.get() == "") :
        messagebox.showerror("ERROR","Empty Fields")
        return 0        
    if adminpassword.get() == con_adminpassword.get() :
        DB_Add_Admin_Record(adminname.get(),adminpassword.get())
        raise_frame(frame)
    else:
        messagebox.showerror("ERROR","Password does not match")
        return 0

def login_click(frame) :
    if (DB_User_Passwd_Chick(username.get(),password.get())) :
        raise_frame(frame)
    else:
        messagebox.showerror("ERROR","username or password is incorrect")
        return 0

def AddAgentWindow():

    def Add_Agent_Click():
        if (ExNumber.get() == 0) and (AgName.get() == "") :
            messagebox.showerror("ERROR","Empty Fields")
        else :
            if DB_Insert_Agent(ExNumber.get(),AgName.get()) :
                ExtentionNumberEntery.delete(0, 'end')
                AgentNameEntery.delete(0, 'end')
                messagebox.showinfo("X","Added successfully")
            else:
                ExtentionNumberEntery.delete(0, 'end')
                AgentNameEntery.delete(0, 'end')
                messagebox.showerror("X","Agent already exists")
    
    AddAgent_Window = Toplevel()
    AddAgent_Window.title('BKSys.Add The New Agent')
    AddAgentFrame = Frame(AddAgent_Window)
    AddAgentFrame.pack()

    ExtentionNumberLable = Label(AddAgentFrame,text="Extention Number")
    ExtentionNumberEntery = ttk.Entry(AddAgentFrame,textvariable=ExNumber)
    AgentNameLable = Label(AddAgentFrame,text="Agent Name")
    AgentNameEntery = ttk.Entry(AddAgentFrame,textvariable=AgName)
    AddButton = ttk.Button(AddAgentFrame,text="Add",command=Add_Agent_Click)

    ExtentionNumberLable.grid(row=0,column=0,padx=3,pady=3,sticky=W)
    ExtentionNumberEntery.grid(row=0,column=1,padx=3,pady=3,sticky=W)
    AgentNameLable.grid(row=1,column=0,padx=3,pady=3,sticky=W)
    AgentNameEntery.grid(row=1,column=1,padx=3,pady=3,sticky=W)
    AddButton.grid(row=2,columnspan=2)

def DeleteAgentWindow():
    i = 0
    Clear_List(DeleteCheckBox)
    Clear_MainDB()
    Clear_IdDB()
    Init_MainDB()
    Init_IdDB()

    def Delete_Agent() :
        index=0
        for itrat in DeleteCheckBox :
            if DeleteCheckBox[index].get() == 0 :
                index += 1 
            else :
                DB_Delete_Agent(DeleteCheckBox[index].get())
                index += 1
        Delete_Agent_Window.destroy()


    Delete_Agent_Window = Toplevel()
    Delete_Agent_Window.title('BKSys.Delete Agent From Data base')
    cTableContainer = Canvas(Delete_Agent_Window, width=400, height=300)
    cTableContainer.grid(row=0,column=0,padx=10)
    fTable = Frame(cTableContainer)
    fTable.grid(padx=60,sticky=NS)
    sbVerticalScrollBar = ttk.Scrollbar(Delete_Agent_Window, orient="vertical")
    sbVerticalScrollBar.grid(row=0,column=1,sticky=NS)
    cTableContainer.config(yscrollcommand=sbVerticalScrollBar.set, highlightthickness=0)
    sbVerticalScrollBar.config(orient=VERTICAL, command=cTableContainer.yview)

    for Id in IdDB :
        DeleteCheckBox.append(IntVar())
        Agent = ttk.Checkbutton(fTable, text = f"{MainDB[Id][Name]}",variable=DeleteCheckBox[i],onvalue =Id,offvalue = 0)
        Agent.grid(sticky=W)
        i += 1 
    
    AddButton = ttk.Button(fTable,text="Delete",command=Delete_Agent)
    AddButton.grid()

    cTableContainer.update_idletasks()
    cTableContainer.config(scrollregion=fTable.bbox())
    cTableContainer.create_window(0, 0, window=fTable, anchor=NW)

    Delete_Agent_Window.mainloop()

def Generate_Agent_Report():
    
    Clear_MainDB()
    Clear_IdDB()
    Init_MainDB()
    Init_IdDB()

    #creat new excel file and new sheet into it
    outworkbook = xlsxwriter.Workbook("BreakSheet"+Data_Time_Print()+".xlsx")
    outsheet = outworkbook.add_worksheet()

    outsheet.write(0,0,"Ext")
    outsheet.write(0,1,"NAME")
    outsheet.write(0,2,"Break")

    SheetRow = 1
    for Id in IdDB :
        outsheet.write(SheetRow,0,Id)
        outsheet.write(SheetRow,1,MainDB[Id][Name])
        outsheet.write(SheetRow,2,MainDB[Id][BreakTime])
        SheetRow += 1
    
    outworkbook.close()
    messagebox.showinfo("Done","Done")

def AboutWindow(): 
    About_Window = Toplevel()
    About_Window.title('BKSys.About')
    
    Pra = """
  it an emerging idea to create a community that Practical, 
  Hands-on Problems and Solutions Activities in programing 
  and  embedded  system  field. This program is one of his 
  projects to organize working time in companies and works
  -hops to ensure greater productivity during work and gre
  -ater comfort break for workers.

  This program  was programmed totally using python if you 
  interested  you  can see and download the full code from 
  my blogger.
    """
    TitleLable = Label(About_Window, text = "About VECCHIATRON")
    TitleLable.config(font =("Courier", 14))
    TitleLable.pack()

    TextBox = Text(About_Window, height = 15, width = 60)
    TextBox.pack()
    

    link1 = Label(About_Window, text="VECCHIATRON.COM", fg="blue", cursor="hand2")
    link1.pack()
    link1.bind("<Button-1>", lambda e: callback("https://vecchiatron.blogspot.com/"))

    TextBox.insert(END,Pra)

def Prepare_Window():
    pass

def BreakSystemWindow():
    global Number_Of_User_Break
    Status = {}
    Helth = {}
    Spend = {}
    ClickFlag = {}
    OutTime = {}
    InTime = {}
    SpendTime = {}
    StatusList = list()
    Clear_MainDB()
    Clear_IdDB()
    Init_MainDB()
    Init_IdDB()

    for Id in IdDB :
        StatusList.append(MainDB[Id][BreakStatus])
    Number_Of_User_Break = StatusList.count('Green')

    for Id in IdDB :
        SpendTime[Id] = MainDB[Id][BreakTime]

    def StartButt(Id):
        global Number_Of_User_Break
        if ClickFlag[Id] :
            OutTime[Id] = CurrentTime()
            Status[Id].config(fg="Green")
            Number_Of_User_Break += 1
            U.config(text=f"{Number_Of_User_Break}")
            ClickFlag[Id] = False
        else : 
            pass
    
    def StopButt(Id):
        global Number_Of_User_Break
        if not ClickFlag[Id] :
            InTime[Id] = CurrentTime()
            Status[Id].config(fg="Red")
            Number_Of_User_Break -= 1
            U.config(text=f"{Number_Of_User_Break}")
            
            if InTime[Id][0] == OutTime[Id][0] :
                SpendTimeMin = InTime[Id][1] - OutTime[Id][1]
                SpendTime[Id] += SpendTimeMin
            elif (InTime[Id][0] > OutTime[Id][0]) and ((InTime[Id][0] - OutTime[Id][0]) == 1) :
                LastTime = 60 - OutTime[Id][1]
                SpendTimeMin = LastTime + InTime[Id][1]
                SpendTime[Id] += SpendTimeMin
            Helth[Id].config(text=f"(Helth | 00:{60-SpendTime[Id]})")
            Spend[Id].config(text=f" (Spend | 00:{SpendTime[Id]})")            
            ClickFlag[Id] = True
        else : 
            pass

    def User_Content_Creation(x) :
        global init_row
        ClickFlag[x] = True

        Spration = Label(fTable,text="---------------------------------------",font='bold')
        Spration.grid(row=init_row,columnspan=5)
        init_row +=1
        User1= Label(fTable,text=f"{MainDB[x][Name]}",fg="Green",font='bold')
        User1.grid(row=init_row,columnspan=5)
        init_row +=1
        StartB= ttk.Button(fTable,text="START",command=lambda:StartButt(x))
        StartB.grid(row=init_row,column=0,padx=5)

        StopB = ttk.Button(fTable,text="STOP",command=lambda:StopButt(x))
        StopB.grid(row=init_row,column=1,padx=5)

        Status[x] = Label(fTable,text="⚫",fg=f"{MainDB[x][BreakStatus]}",font=('Helvatical bold',20))
        Status[x].grid(row=init_row,column=2)
        Helth[x] = Label(fTable,text=f"(Helth | 00:{(60-SpendTime[Id])})")
        Helth[x].grid(row=init_row,column=3)
        Spend[x] = Label(fTable,text=f" (Spend | 00:{SpendTime[Id]})")
        Spend[x].grid(row=init_row,column=4)
        init_row +=1

    def Clock() :
        Hour = time.strftime("%I")
        Minute = time.strftime("%M")
        Second = time.strftime("%S")
        DigitalClock.config(text=f"{Hour}:{Minute}:{Second}")
        DigitalClock.after(1000,Clock)

    BreakSys_Window = Toplevel()
    BreakSys_Window.title('The Breaks')
    BreakSys_Window.geometry("700x670+50+10")
    BreakSys_Window.resizable(0,0)

    BreakControl = Frame(BreakSys_Window)
    BreakControl.pack()

    DaBoard = Frame(BreakSys_Window)
    DaBoard.pack()

    cTableContainer = Canvas(BreakControl, width=500, height=500)
    cTableContainer.grid(row=1,column=0,padx=10)
    fTable = Frame(cTableContainer)
    fTable.grid(padx=60,sticky=NS)
    sbVerticalScrollBar = ttk.Scrollbar(BreakControl, orient="vertical")
    sbVerticalScrollBar.grid(row=1,column=1,sticky=NS)
    cTableContainer.config(yscrollcommand=sbVerticalScrollBar.set, highlightthickness=0)
    sbVerticalScrollBar.config(orient=VERTICAL, command=cTableContainer.yview)
    cTableContainer.create_window(0, 0, window=fTable, anchor=NW)

    for Id in IdDB:
        User_Content_Creation(Id)
    cTableContainer.update_idletasks()
    cTableContainer.config(scrollregion=fTable.bbox())

    N = Label(DaBoard,text="Break",font=('Helvatical bold',20))
    N.grid(row=0,column=0)
    U = Label(DaBoard,text=f"{Number_Of_User_Break}",fg="Green",font=('Helvatical bold',20))
    U.grid(row=1,column=0)
    DigitalClock = Label(DaBoard,text="",font=('Helvatical bold',20),fg="Red",bg="Black")
    DigitalClock.grid(row=0,column=1,rowspan=2)
    Clock()
    BreakSys_Window.mainloop()
    for Id in IdDB :
        DB_Update_Break_Time(Id,SpendTime[Id])

def build_boot() :
    #create main widget for boot window
    admin_label = Label(BootFrame,text="Admin name")
    admin_name = ttk.Entry(BootFrame,textvariable=adminname)
    admin_password_label = Label(BootFrame, text="Password")
    admin_password = ttk.Entry(BootFrame,textvariable=adminpassword,show="*")
    admin_confirm_label = Label(BootFrame, text="Password Confirm")
    admin_password_confirm = ttk.Entry(BootFrame,textvariable=con_adminpassword,show="*")
    submit = ttk.Button(BootFrame, text="Submit",command=lambda:submit_click(LoginFrame))
    #put the widget on the screen 
    admin_label.grid(row=0,column=0,padx=3,pady=3,sticky=W)
    admin_name.grid(row=0,column=1,padx=3,pady=3,sticky=W)
    admin_password_label.grid(row=1,column=0,padx=3,pady=3,sticky=W)
    admin_password.grid(row=1,column=1,padx=3,pady=3,sticky=W)
    admin_confirm_label.grid(row=2,column=0,padx=3,pady=3,sticky=W)
    admin_password_confirm.grid(row=2,column=1,padx=3,pady=3,sticky=W)
    submit.grid(row=3,column=0,columnspan=2,pady=20)

def build_login() :
    #password label and password entry box
    usernameLabel = Label(LoginFrame, text="User Name")
    usernameEntry = ttk.Entry(LoginFrame, textvariable=username)
    passwordLabel = Label(LoginFrame,text="Password")
    passwordEntry = ttk.Entry(LoginFrame, textvariable=password, show='*')
    #login button
    loginButton = ttk.Button(LoginFrame, text="Login",command=lambda:login_click(SBKWindow))
    usernameLabel.grid(row=0, column=0,padx=3,pady=3,sticky=W)
    usernameEntry.grid(row=0, column=1,padx=3,pady=3,sticky=W)
    passwordLabel.grid(row=1, column=0,padx=3,pady=3,sticky=W)  
    passwordEntry.grid(row=1, column=1,padx=3,pady=3,sticky=W)
    loginButton.grid(row=2, column=0,columnspan=2,pady=20)  

def BSK_main_window() :
    ActControl = LabelFrame(SBKWindow,text="Act Control", bd=3, padx=20, pady=20)
    ActControl.grid(row=0,column=0,padx=5, pady=5)
    Prepare = ttk.Button(ActControl, text="Prepare",command=Prepare_Window)
    Prepare.grid(padx=10, pady=5,sticky=W+E)
    StartBKSys= ttk.Button(ActControl, text="Start The Break System",command=BreakSystemWindow)
    StartBKSys.grid(padx=10, pady=5,sticky=W+E)

    UserManager = LabelFrame(SBKWindow, text="User Manager", bd=3, padx=10, pady=10)
    UserManager.grid(row=0,column=2,padx=5, pady=5)
    AddAgent = ttk.Button(UserManager, text="Add Agent",command=AddAgentWindow)
    AddAgent.grid(pady=1,sticky=W+E)
    DeleteAgent= ttk.Button(UserManager, text="Delete Agent",command=DeleteAgentWindow)
    DeleteAgent.grid(pady=1,sticky=W+E)
    ShowAll= ttk.Button(UserManager, text="Report",command=Generate_Agent_Report)
    ShowAll.grid(pady=1,sticky=W+E)
    About= ttk.Button(UserManager, text="About",command=AboutWindow)
    About.grid(padx=10, pady=10)
#---------------------------------------(Main App)---------------------------------------

# Main configuration for the Window
boot = Tk()
boot.title("SBK_VECCHIATRON")
boot.geometry("583x591+468+158")
boot.resizable(0,0)
boot.iconphoto(True,PhotoImage(file='v.png'))
boot.configure(borderwidth="1")
boot.configure(relief="sunken")
boot.configure(background="#dbd8d7")
boot.configure(cursor="arrow")
boot.configure(highlightbackground="#d9d9d9")
boot.configure(highlightcolor="black")
boot_style = ttk.Style()
boot_style.theme_use('clam')

#declaration all variables names
username = StringVar()
password = StringVar()
adminname = StringVar()
adminpassword = StringVar()
con_adminpassword = StringVar()
ExNumber = IntVar()
AgName = StringVar()
AgAccount = StringVar()

# Logo Frame
LogoFrame = Frame(boot)
LogoFrame.grid(row=0, column=0, sticky='news')
Label1 = Label(LogoFrame)
_img1 = PhotoImage(file="l.png")
Label1.configure(image=_img1)
Label1.configure(text='''Label''')
Label1.pack()

# # Boot Frame for booting the program frist time use 
BootFrame = Frame(boot,padx=50,pady=50)
BootFrame.grid(row=1)
BootFrame.grid_rowconfigure(0, weight=1)
BootFrame.grid_columnconfigure(0, weight=1)
build_boot()

# # Login Frame for any time the program will use 
LoginFrame = Frame(boot,padx=100,pady=100)
LoginFrame.grid(row=1)
LoginFrame.grid_rowconfigure(0, weight=1)
LoginFrame.grid_columnconfigure(0, weight=1)
build_login()

# main program window
SBKWindow = Frame(boot,pady=50)
SBKWindow.grid(row=1)
SBKWindow.grid_rowconfigure(0, weight=1)
SBKWindow.grid_columnconfigure(0, weight=1)
BSK_main_window()

# frist login chick
ChickFile = open("bootchieck.txt","r+")
if ChickFile.read() == "1" :
    DB_connection()
    raise_frame(BootFrame)
    ChickFile.write("0")
    ChickFile.close()
    DB_Add_Mastr_Record()
    DB_Push()
else:
    raise_frame(LoginFrame)
    ChickFile.close()
    Init_MainDB()
    Init_IdDB()
    DateStart = CurrentDate()
    TimeStart = CurrentTime()
    DataFile = open("FristTimeOpen.txt","r")
    if DataFile.read() == DateStart :
        pass
    else :
        if (TimeStart[0] >= 0) and (TimeStart[0] <= 3) and (TimeStart[2] >= 'am') :
            pass
        else :
            for Id in IdDB :
                DB_Update_Break_Time(Id,0)
            DataFile.close()
            DataFile = open("FristTimeOpen.txt","w")
            DataFile.write(DateStart)
            DataFile.close()
            Clear_MainDB()
            Clear_IdDB()
            Init_MainDB()
            Init_IdDB()


boot.mainloop()