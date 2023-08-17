from kivymd.app import MDApp
from kivy.lang.builder import Builder
from kivymd.uix.screen import MDScreen
from kivymd.uix.screenmanager import MDScreenManager
from kivy.core.window import Window
from kivymd.uix.datatables import MDDataTable
from kivy.metrics import dp
from kivymd.uix.snackbar import Snackbar
from datetime import date
from kivymd.uix.textfield import MDTextFieldRect
from kivymd.uix.button import MDFillRoundFlatButton
import mysql.connector
from kivymd.uix.label import MDLabel
from kivymd.uix.dialog import MDDialog
from kivymd.uix.list import   IconLeftWidget, ThreeLineIconListItem, ThreeLineAvatarListItem,TwoLineAvatarListItem,MDList,OneLineListItem,IconRightWidget,OneLineAvatarIconListItem
from kivymd.uix.card import MDCard
from kivymd.uix.progressbar import MDProgressBar
from kivymd.uix.button import MDRaisedButton,MDFlatButton
from kivy.clock import Clock
import threading
import time



class MainApp(MDApp):

    def build(self):
        self.clicked= False
        self.ensi=False
        self.nive=False
        self.file= False
        self.clas= False
        self.grou=False
        self.dialo=None
        self.savedialo= None
        self.appscreens= MDScreenManager()
        self.welcomescreen= MDScreen()
        self.mainscreen= MDScreen()
        self.welcomescreen= Builder.load_file('w_welcome.kv')
        self.mainscreen= Builder.load_file('w_main.kv')
        self.dialogbox= Builder.load_file('listens.kv') # dilog box lists
        self.savedialogbox= Builder.load_file('startsaving.kv') #dialog box start saving
         
         



        
        self.appscreens.add_widget(self.welcomescreen)
        self.appscreens.add_widget(self.mainscreen)
        
        

        return self.appscreens



    def on_start(self):
        try:
            self.conn= mysql.connector.connect(
                host='db4free.net',
                user='baroudi',
                passwd='68415e49',
                database='dbbaroudi')
            self.cur= self.conn.cursor()
            self.welcomescreen.ids.iconconnect.icon='autorenew'
            self.welcomescreen.ids.iconconnect.text_color= 'green'
        except:
            self.welcomescreen.ids.iconconnect.icon='autorenew-off'
            self.welcomescreen.ids.iconconnect.text_color= 'red'
            
        today=date.today()
        d1 = today.strftime("%d/%m/%Y")
        self.mainscreen.ids.lyoum.text=date.today().strftime("%A") + "  " + str(d1)

   
    def checkpresent(self, instance_table,current_row):
        
        #print(current_row)
        pass




    def returnens(self, instance):
        selected_item = instance.text
        selected_item=selected_item.strip()
        if self.ensi==True:  
            self.welcomescreen.ids.comboens.text= selected_item
            self.enschoix=selected_item  
            
            self.welcomescreen.ids.comboniv.text=''
            self.welcomescreen.ids.combofil.text=''
            self.welcomescreen.ids.combocla.text=''
            self.welcomescreen.ids.combogro.text=''
            
        if self.nive==True:
            self.welcomescreen.ids.comboniv.text= selected_item
            self.nivchoix=selected_item  
            self.welcomescreen.ids.combofil.text=''
            self.welcomescreen.ids.combocla.text=''
            self.welcomescreen.ids.combogro.text=''
        if self.file==True:
            self.welcomescreen.ids.combofil.text= selected_item
            self.filchoix=selected_item  
            self.welcomescreen.ids.combocla.text=''
            self.welcomescreen.ids.combogro.text=''
        if self.clas== True:
            self.welcomescreen.ids.combocla.text= selected_item
            self.clachoix=selected_item  
            self.welcomescreen.ids.combogro.text=''
        if self.grou==True:
            self.welcomescreen.ids.combogro.text= selected_item
            self.grochoix=selected_item  
            
            
        
        
        
        



        self.dialo.dismiss()
    def selectitem(self):
        
        #dialog box to select ens or niveau or class or groupe
        for i in self.listens:
            ensitem=OneLineListItem(text= i)
            ensitem.bind(on_release= self.returnens)
            self.dialogbox.ids.container.add_widget(
                ensitem

            )    
        if not self.dialo:
            
            self.dialo = MDDialog(title=self.titre,
                        type="custom",
                    content_cls= self.dialogbox 
                    )
        self.dialo.title=self.titre
        self.dialo.open()  

    #remplir les list
    def comboens(self):
        try:
            self.ensi=True
            self.nive=False
            self.file= False
            
            self.clas= False
            self.grou=False
            self.dialogbox.ids.container.clear_widgets()
            
            self.cur.execute('SELECT DISTINCT ens FROM Absence;')
            result= self.cur.fetchall()
            self.listens=[]
            self.listens.clear()
            for i in result :
                self.listens.append(i[0])
            self.titre='Enseignement'
            self.selectitem()
        except:
            Snackbar(text="Vous devez Sélectionner les critère précédente!",bg_color=(1, 0, 0, 1)).open()    
    def comboniv(self):
        try:
            self.ensi=False
            self.nive=True
            self.file= False
            self.clas= False
            self.grou=False
            
            self.dialogbox.ids.container.clear_widgets()
            self.cur.execute("SELECT DISTINCT niveau FROM Absence WHERE ens='" + str(self.enschoix)+ "' ;")
            result= self.cur.fetchall()
            self.listens=[]
            self.listens.clear()
            for i in result :
                self.listens.append(i[0])
            self.titre='Niveau'    
            self.selectitem()
        except:
            Snackbar(text="Vous devez Sélectionner les critère précédente!",bg_color=(1, 0, 0, 1)).open()

    def combofili(self):
        try:
            self.ensi=False
            self.nive=False
            self.file= True
            self.clas= False
            self.grou=False
            self.dialogbox.ids.container.clear_widgets()
            
            self.cur.execute("SELECT DISTINCT filiere FROM Absence WHERE ens='" + str(self.enschoix)+ "' AND niveau='" + str(self.nivchoix)+ "';")
            result= self.cur.fetchall()
            self.listens=[]
            self.listens.clear()
            for i in result :
                self.listens.append(i[0])
            self.titre='Filiere'
            self.selectitem()
        except:
            Snackbar(text="Vous devez Sélectionner les critère précédente!",bg_color=(1, 0, 0, 1)).open()

    def comboclas(self):
        try:
            self.ensi=False
            self.nive=False
            self.file= False
            self.clas= True
            self.grou=False
            
            self.dialogbox.ids.container.clear_widgets()
            
            self.cur.execute("SELECT DISTINCT classe FROM Absence WHERE ens='" + str(self.enschoix)+ "' AND niveau='" + str(self.nivchoix)+ "' AND filiere='" + str(self.filchoix)+ "' ;")
            result= self.cur.fetchall()
            self.listens=[]
            self.listens.clear()
            
            for i in result :
                self.listens.append(i[0])
            self.titre='Classe'
            self.selectitem()   
        except:
            Snackbar(text="Vous devez Sélectionner les critère précédente!",bg_color=(1, 0, 0, 1)).open()    #

    def combogrou(self):
        try:
            self.ensi=False
            self.nive=False
            self.file= False
            self.clas= False
            self.grou=True
            self.dialogbox.ids.container.clear_widgets()
            
            self.cur.execute("SELECT DISTINCT groupe FROM Absence WHERE ens='" + str(self.enschoix)+ "' AND niveau='" + str(self.nivchoix)+ "' AND filiere='" + str(self.filchoix)+ "' AND classe ='" + str(self.clachoix)+ "' ;")
            result= self.cur.fetchall()
            self.listens=[]
            self.listens.clear()
            for i in result :
                self.listens.append(i[0])
            self.titre='Groupe'
            self.selectitem()
        # save the current absence to the table 
        except:
            Snackbar(text="Vous devez Sélectionner les critère précédente!",bg_color=(1, 0, 0, 1)).open()
    def saveabsence(self):
        
        #self.savedialogbox.ids.container
        self.rest=int(len(self.listens))+int(len(self.listfinal))

        self.totalrec=self.rest
        self.minus= int(100/self.totalrec)
        self.totalrecT=100
        self.ii=0
        if not self.savedialo:
        
            self.savedialo = MDDialog(title='Sauvgarder ?',
                        type="custom",
                    content_cls= self.savedialogbox,
                    radius=[20, 7, 20, 7],
                    auto_dismiss=False,
                    buttons=[
                        MDFlatButton(
                            id='btncancel',
                            text="Annuler", text_color=self.theme_cls.primary_color, on_release= self.closeDialog
                        ),
                        MDFlatButton(
                            id='btnsave',
                            text="Enregistrer", text_color=self.theme_cls.primary_color, on_release=self.start_loop
                        ),
                ], 
                    )
        self.savedialo.buttons[0].disabled = False  # Disable the OK button
        self.savedialo.buttons[1].disabled = False  # Disable the Cancel button           
        self.savedialogbox.ids.lab.text=" Cliquer Sur Enregistrer pour sauvgarder"
        self.savedialo.open() 
        #lcard=MDCard(id='cardpr')
        
       # pr=MDProgressBar(pos_hint ={'center_x':0.5,'center_y':0.5} ,size_hint_y= 0.05,size_hint_x=0.7,value=6)
        
       # lcard.add_widget(pr)
        
       # self.mainscreen.add_widget(lcard)
    def closeDialog(self, instance):
        self.savedialo.dismiss()
        
    def starsaving(self):
        try:
            self.savedialo.buttons[0].disabled = True  # Disable the OK button
            self.savedialo.buttons[1].disabled = True  # Disable the Cancel button

            #self.savedialogbox.ids.prog.opacity=1
            self.savedialogbox.ids.lab.text=str('Enregistrement en cours...' )
            for i in self.listens:
                
                #self.ii=self.totalrecT-self.rest
                #self.rest=self.rest-1
                self.ii=self.ii+self.minus
                item_id=i[0]
               # print(item_id)

                sql= "UPDATE Absence SET present = 'Non' WHERE ens='" + str(self.enschoix)+ "' AND niveau='" + str(self.nivchoix)+ "' AND filiere='" + str(self.filchoix)+ "' AND classe ='" + str(self.clachoix)+ "' AND id ='" + str(item_id)+ "';"
                self.cur.execute(sql)
                self.conn.commit()
                # Update the label text on the main thread using Clock
                #print('______________', self.ii , '________________________________')
                self.update_prog(self.ii)
                time.sleep(0.2)  # Sleep for 1 second
                
            for id in self.listfinal :
                self.ii=self.ii+self.minus
                #print(id)
                sql= "UPDATE Absence SET present = 'Oui' WHERE ens='" + str(self.enschoix)+ "' AND niveau='" + str(self.nivchoix)+ "' AND filiere='" + str(self.filchoix)+ "' AND classe ='" + str(self.clachoix)+ "' AND id ='" + str(id)+ "';"
                self.cur.execute(sql)
                self.conn.commit() 
                # Update the label text on the main thread using Clock
                #print('______________', self.ii , '________________________________')
                self.update_prog(self.ii)
                time.sleep(0.2)  # Sleep for 1 second
            self.update_prog(100)
            time.sleep(0.2)  # Sleep for 1 second
            self.savedialo.dismiss()  
                               
                        
            self.ii=0
            self.savedialogbox.ids.prog.value=0
            self.savedialogbox.ids.lab.text=" Cliquer Sur Enregistrer pour sauvgarder"
            
            #self.savedialogbox.ids.prog.opacity=0
                 
        except:
            self.savedialo.dismiss() 
            self.gowelcome()     
            #print('errrorrrrrrrrrrrrrrrrrrrrrrrr')
            #Snackbar(text="Vous devez Sélectionner les critère précédente!",bg_color=(0, 1, 0, 1)).open()
            
            self.mainscreen.ids.saveb.bg_color=(0, 1, 0, 1)
            self.mainscreen.add_widget(MDDialog(text='error').open())


    def start_loop(self, *args):
        
        # Create a new thread for the loop
        thread = threading.Thread(target=self.starsaving)
        thread.start()
    def update_prog(self, text):
        # Update the label text on the main thread using Clock
        def updateprogress(dt):
            #self.label.text = text
            newv= int(text)
            self.savedialogbox.ids.prog.value=newv
            #self.savedialogbox.ids.lab.text=str(text )
        Clock.schedule_once(updateprogress)





    # fill the list with checked students
    def checked(self, instance_table, current_row):

        if current_row[0] not in self.listfinal:
            self.listfinal.append(current_row[0])
            
        else:
            self.listfinal.remove(current_row[0])

        #print(self.listfinal)


    #gestion des window
    def gowelcome(self):
        self.mainscreen.ids.mlist.clear_widgets()
        self.listfinal.clear()
        #self.table.clear_widgets
        #self.table.update_row()

        self.appscreens.current= 'welcome'
        self.appscreens.transition.direction= 'right'
    
    def screenmanage(self):
        try:
            # self.table.row_data = []
            self.clicked=False
            self.clearlist=[]
            self.listens=[]
            self.listfinal=[]
            self.listfinal.clear()
            self.listens.clear()
            self.cur.execute("SELECT id,nom,gender,present FROM Absence WHERE ens='" + str(self.enschoix)+ "' AND niveau='" + str(self.nivchoix)+ "' AND filiere='" + str(self.filchoix)+ "' AND classe ='" + str(self.clachoix)+ "' AND groupe ='" + str(self.grochoix)+ "' ;")
            result= self.cur.fetchall()
            #print(result)
            
            self.listens=result
            #print(self.listens)
            
            
            listmd=self.mainscreen.ids.mlist

            for i in self.listens:
                item_id=i[0]
                if i[3]=='Non':
                    back= '#FF0060'

                else:
                    back='#1B9C85'
                    self.listfinal.append(item_id)   
                #item_id = str(uuid.uuid4())
                if i[2]=='Male':
                    genderid= 'face-man'

                else:
                    genderid='face-woman'
                    
                
                listmd.add_widget(ThreeLineIconListItem(
                                IconLeftWidget(icon=genderid),
                                text=i[1],
                                font_style='H6',
                                secondary_text= "ID : "+item_id,
                                tertiary_text='Genre : '+ i[2],
                                id= item_id,
                                on_release=lambda item_id=item_id:self.choix(item_id),
                                bg_color=back
                                )
                )

                
                #print(item_id)
                
                

            self.appscreens.current= 'main'
            self.appscreens.transition.direction= 'left'
        except:
            Snackbar(text="une erreur s'est produite, veuillez vérifier votre connexion.",bg_color=(1, 0, 0, 1)).open()
    def choix(self,data):
        #print( data.id)
        idl=data.id
        todo_list = self.mainscreen.ids.mlist
        #print(todo_list)
        for child in todo_list.children:
            #print(child)
            if child.id == idl:
                child.bg_color ='#1B9C85'
                if idl not in self.listfinal:
                    self.listfinal.append(idl)
                    
                else:
                    self.listfinal.remove(idl)
                    child.bg_color ='#FF0060'

                #print(self.listfinal)          
                 #self.mainscreen.ids.tablescroll.children(idl).bg_color='red'
        
        



if __name__=='__main__':
    Window.size=360,640

    
    MainApp().run() 
       