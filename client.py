
import socket
import threading
import tkinter as tk
from tkinter import *
from tkinter import scrolledtext
from tkinter import messagebox
from tkinter import filedialog
from PIL import Image
import io
import base64
from PIL import Image
import zlib





#birden çok fonksiyonu aynı anda çalıştırabilmek için
def sequence(*functions):
    def func(*args, **kwargs):
        return_value = None
        for function in functions:
            return_value = function(*args, **kwargs)
        return return_value
    return func


HOST="127.0.0.1"
PORT=1234  #0-65535 range

client=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    

root=tk.Tk()
# root2=tk.Tk()



# root2.geometry("600x800")
# root2.title("İkinci Ekran")
# #root.resizable(False,False)
# root2.eval('tk::PlaceWindow . center')



#direkt tkinterdan aldığımız root ekran oluyor
root.geometry("600x700")
root.title("Kullanıcı Ekranı")
#root.resizable(False,False)
root.eval('tk::PlaceWindow . center')
#burada çarpıya basılında exit(0) ile çıkılmalı



def add_message(message):
    message_box.config(state=tk.NORMAL)
    message_box.insert(tk.END, message + '\n')
    message_box.config(state=tk.DISABLED)


def connect():
    try:
        client.connect((HOST,PORT))
        #client bir soket nesnesi olduğu için connect özelliği var
        print("server'a başarıyla bağlanıldı")
        add_message("Server: Servera başarıyla bağlanıldı")
    except:
        messagebox.showerror("Servera bağlanma hatası",
                             f"{HOST} ip adresine ve {PORT} post numarasına sahip servera bağlanırken hata oluştu")
        print("server a bağlanma hatası")
        #exit(0)
        
    #client in burada bir soket nesnesi olduğunu ve soket kütüphanesinin özelliklerini taşıdığını unutmamak gerekir
    username=username_textbox.get()
    myPhoneNumber=sender_phone_textbox.get()
    if username=="" or myPhoneNumber=="":
        messagebox.showerror("error","Kullanıcı adınızı ve telefon numaranızı girin!")
    #burası input değil ayrı bir form ile alınmalı
    
    #buradan sonra username_textbox, sending_phone_textbox ve register button gödünmez oluyor 
    # ve başlılar kullanıcı adıyla değişiyor
    if username!="" and myPhoneNumber!="":
        username_textbox.pack_forget()
        register_button.pack_forget()
        sender_phone_textbox.pack_forget()
        username_label.config(text=username)
        sender_phone_label.config(text=myPhoneNumber)
    
    
    
    
    
    
    if username!="" and myPhoneNumber!="":
        sendingPackage=(f"{username},{myPhoneNumber}")
        client.sendall(sendingPackage.encode())
        #ilk giden mesaj bu ama biz görseli meya mesajı burada göndermiyoruz
    else:
        messagebox.showerror("Geçersiz kullanıcı adı","kullanıcı adı ya da telefon numaranız boş"+
                              "\nuygulama kapanıyor...")
        #exit(0) 
       
    threading.Thread(target=listen_for_messages_from_server,args=(client,myPhoneNumber)).start()
    #her ne kadar client içinde olsak da, client da sürekli diğer client lardan mesaj geldi mi diye bakmalı
    #yani burada da bir thread mekanizması olmalı  
    #threading kütüphanesi ile 1. arguman olarak sürekli çalışmasını istediğimiz şeyi
    #2. arguman olarak iterable bir obje veririz
    
#ya send_image diye bir fonksiyon oluşmalı ya da send message içinde koşullarla ifade etmeliyiz
#servarda da gelen mesaj resim mi yoksa text mi diye kontrol edilmeli   
    
def send_image():
    # pass
    if SEND_MESSAGE_LOCK==True:
        
    
        #messagebox.showerror("error","send_image içine girdik")
        data = filedialog.askopenfile(initialdir="/")
        path = str(data.name)
        image = open(path,"rb")
       
        #read binary demek
        bytes=image.read(2048)
        
        
        sendingPhone=sending_phone_textbox.get()
        
        #gönderilmesi gereken asıl veri----> bytes şeklinde resim ve göndrerilecek telefon numarası
        client.sendall(f"**image_message_starting**,{sendingPhone}".encode())
        #byte iletimi başlangıcı**************************************************
        
        while bytes:
            client.send(  bytes  )
            bytes=image.read(2048)
            #göndermede de bir sıkıntı olabilir çünkü her yeniden göndermede devam ediyo gibiydi
            #bir de klasör isimlerinde sıkıntı olabilir
         
        
        image.close()
        
        # client.send(f"**image_message_end**+++".encode()) 
        print("resim gönderimi tamamlandı")
        
        
        
        #byte iletimi sonu *******************************************************
        
        
        
    else:
        pass
    

# SEND_MESSAGE_LOCK=False
def lock_changer():
    #messagebox.showerror("error","lock_changer içine girdik")
    #global değikeni fonksiyon içinden değiştirme
    global SEND_MESSAGE_LOCK
    SEND_MESSAGE_LOCK=True    
    

def send_message():   
    message=message_textbox.get()
    sendingPhone=sending_phone_textbox.get()
    if message!="" and sendingPhone !="":
        sending_message=f"**text_message_beginning**{message}~{sendingPhone}**text_message_end**"
        # for i in sending_message:
        client.sendall( sending_message.encode() )
        
        #client.sendall((  f"**text_message**{message},{sendingPhone}"  ).encode())  #burayı geçici olarak değiştirdim
        #############################################
        
        #bu sefer gidecek mesaj eğer text ise başında text_message da yazılı gider ve server bunu ayrıştırır
        #  "text_messageselam,hüseyin"
        #"selam"
        #  "selam,0534"
        print(f"{sendingPhone} telefon numarasına göndermesi için servera şu mesaj gitti: {message}")
        message_textbox.delete(0,len(message))
    else:
        messagebox.showerror("empty message","gönderilecek mesaj veya telefon numarasını boş bıraktınız, tekrar deneyin"+
                            "\nUygulama kapatılıyor...")
        #exit(0)   #burası uygulamayı sonlandırıyor
        
        
        

        
    




def empty_fun():
    pass



DARK_GREY = '#121212'
MEDIUM_GREY = '#1F1B24'
OCEAN_BLUE = '#464EB8'
WHITE = "white"
FONT = ("Helvetica", 17)
BUTTON_FONT = ("Helvetica", 15)
PICTURE_BUTTON_FONT = ("Helvetica", 8)
MESSAGE_BUTTON_FONT = ("Helvetica", 11)
SMALL_FONT = ("Helvetica", 13)


#kullanıcı adı ve telefon numarasını girdikten sonraki submit butonu ile
#her ikisi de serverda gereken yere gitmeli ve 
#sumbit butonuna basılınca üst tarafta 2 tane textbox yok olmalı ve yerine 
#bizim bilgilerimizin olduğu labellar çağrılmalı (onların olduğu ve tanımlandığı fonksiyon çağrılmalı)
#Hüseyin Türkmen,  0534 gibi


root.grid_rowconfigure(0, weight=1)
root.grid_rowconfigure(1, weight=1)
root.grid_rowconfigure(2, weight=1)
root.grid_rowconfigure(3, weight=3)
root.grid_rowconfigure(4, weight=1)

top_frame=tk.Frame(root,width=600,height=100,bg=OCEAN_BLUE)
top_frame.grid(row=0,column=0,sticky=tk.NSEW)
#sanırım NSEW taşmamayı vs sağlıyo

second_top_frame=tk.Frame(root,width=600,height=100,bg=OCEAN_BLUE)
second_top_frame.grid(row=1,column=0,sticky=tk.NSEW)

third_top_frame=tk.Frame(root,width=600,height=100,bg=OCEAN_BLUE)
third_top_frame.grid(row=2,column=0,sticky=tk.NSEW)

middle_frame=tk.Frame(root,width=600,height=200,bg=MEDIUM_GREY)
middle_frame.grid(row=3,column=0,sticky=tk.NSEW)

bottom_frame=tk.Frame(root,width=600,height=100,bg=DARK_GREY)
bottom_frame.grid(row=4,column=0,sticky=tk.NSEW)

#her eleman tk ya göre tanımlanır ama
#frame lerin render edilmesi için grid,
#label, button, textbox gibi frame üzerinde gelecek itemlerin render edilmesi için ise pack yapılması gerekir

username_label= tk.Label(top_frame,text="Kullanıcı Adınız: ",
                         font=FONT,bg=WHITE,fg=DARK_GREY)
#burada yükseklik olarak top frame in tamamını doldurur
username_label.pack(side=tk.LEFT,padx=10)

username_textbox= tk.Entry(top_frame,font=FONT,bg=MEDIUM_GREY,fg=WHITE,width=23)
username_textbox.pack(side=tk.LEFT)

#----------------------------------------------------------------------------------------------------
sender_phone_label= tk.Label(second_top_frame,text="Telefon Numaranız: ",font=FONT,bg=WHITE,fg=DARK_GREY)
sender_phone_label.pack(side=tk.LEFT,padx=10)

sender_phone_textbox= tk.Entry(second_top_frame,font=FONT,bg=MEDIUM_GREY,fg=WHITE,width=23)
sender_phone_textbox.pack(side=tk.LEFT)

#----------------------------------------------------------------------------------------------------
sending_phone_label= tk.Label(third_top_frame,text="Gönderilecek kişi: ",font=FONT,bg=WHITE,fg=DARK_GREY)
sending_phone_label.pack(side=tk.LEFT,padx=10)

sending_phone_textbox= tk.Entry(third_top_frame,font=FONT,bg=MEDIUM_GREY,fg=WHITE,width=23)
sending_phone_textbox.pack(side=tk.LEFT)

#----------------------------------------------------------------------------------------------------

register_button=tk.Button(top_frame,text="Kayıt ol",font=BUTTON_FONT,bg=OCEAN_BLUE,fg=WHITE,
                          command=sequence(lock_changer,connect)
                          )
register_button.pack(side=tk.LEFT,padx=15)
#----------------------------------------------------------------------------------------------------

send_immage_button=tk.Button(middle_frame,text="Resim gönder",font=PICTURE_BUTTON_FONT,bg=OCEAN_BLUE,fg=WHITE,
                          command=send_image
                          )
 #buranın çağıracaklarını daha sonra belirleyeceğiz
send_immage_button.pack(side=tk.TOP,padx=15)

#----------------------------------------------------------------------------------------------------


message_box = scrolledtext.ScrolledText(middle_frame, font=SMALL_FONT, bg=MEDIUM_GREY, fg=WHITE, width=67, height=26.5)
message_box.config(state=tk.DISABLED)
message_box.pack(side=tk.TOP)

#----------------------------------------------------------------------------------------------------

message_textbox= tk.Entry(bottom_frame,font=FONT,bg=MEDIUM_GREY,fg=WHITE,width=38)
message_textbox.pack(side=tk.LEFT,padx=10)

message_button=tk.Button(bottom_frame,text="Gönder",font=MESSAGE_BUTTON_FONT,bg=OCEAN_BLUE,fg=WHITE,
                         command=sequence(   send_message)     
                         )

#----------------------------------------------------------------------------------------------------

message_button.pack(side=tk.LEFT,padx=10)
# command=lambda: message_button.pack_forget()   bu şekilde bir elementi silebiliriz
#üstteki sequence fonksiyonuna birden fazla parametre göndererek tek buton ile birden fazla fonksiyon çağırabiliriz
#    command=sequence(   send_message,lambda: message_button.pack_forget()   bu şekilse

#----------------------------------------------------------------------------------------------------

      
        

def listen_for_messages_from_server(client,myPhoneNumber):
    #burada tüm kullanıcılar serverdan gelen tüm mesajları alabliyor
    #ama bizimkileri sadece belirli kişiler görebilmeli
    while 1:
        #bağlantıyı yapan client sürekli dünliyor...(serverdan gelen mesajları)
        #diğer clientlardan gelen mesajları da client server üzerinden dinleyecek
        first_message_from_server=client.recv(2048)
        print("\n servardan gelen ilkkkkk mesaj: ")
        print(first_message_from_server)
        print("\n")
        #burası her türlü resim veya text geliyor diye bir mesaj içerir
        #şuan gelen mesaj bytes
        
        #burdaki firts message hem resim gelirse alınacak ilk bytes dizisi,
        #hem de text gelirse onun decode edilmemiş halidir
        
        # ilk_mesaj=first_message_from_server.decode("utf-8")
        #burada gelen client ın ilk text mesajından sonraki bytes mesajlarını da alıp decode etmeye çalışıyo,
        #bir sınır vs bir şey verip bu bloktan çıkmasını sağlamamız gerekiyor
        #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        
        
        print("ilk ayırıcı mesaj alındı")
        # if(str(ilk_mesaj).startswith("text_from_server")):
        if("text_from_server" in str(first_message_from_server)):
            #yani server ın asıl mesajı göndermeden önce gönderdiği encode (bytes) halindeki mesajın 
            #string halinde istenen keyword varsa buraya gir ve yeni mesajları bekle
            text_message_from_server=client.recv(2048).decode("utf-8")
            print("serverdan text mesajı alma bloğuna girdik!")
            if text_message_from_server!="":
                #serverdan gelen mesaj username~mesaj şeklinde geleceği için böyle alırız
                #buradaki client en başta bizim server name imizi bilen ve ona bağlanıp onu dinleyen client olduğu için
                #otomatikmen serverdan gelen tüm mesajlar ve servera diğer cleintlar tarafından send edlien tüm  mesajları burada görebilirz
                
                print(text_message_from_server)
                
                
                receivedPhoneNumber=text_message_from_server.split("~")[0]
                content=text_message_from_server.split("~")[1]
                
                if myPhoneNumber!=receivedPhoneNumber:
                     
                    add_message(f"[{receivedPhoneNumber} ] telefon numarasına sahip kullanıcı alttaki mesajı attı:\n-->  {content} \n")
                else:
                    add_message("kendi numarama kendi mesajım geldi !")
                    
            else:
                messagebox.showerror("empty message","client'dan alınan mesaj boş")
        else:
            print("serverdan resim alma bloğuna girdik!")
            temporary_bytes=client.recv(2048)
            #servardan alınan ilk resim bytes parçası
            print("\nAAAAAAAAAAAAAAAAAA\n")
            print("\n")
            print(temporary_bytes)
            #buradaki temporary_bytes değişkeni resim gelmişse, gelen resmin ilk bytes ıdır.
            
            #şuana kadar ilk gelen bytes ı aldık ve yazdırdık
            
            
            file=open('picture_on_clients_from_server.jpg',"wb")
            
            
 
 
 
 #burada alınan tüm bytes ları aynı anda dosyaya yazdırıp gerekli clienta da geri yoluuyoruz
            counter=1  
            while True:
                print(f"servardan resim mesajı alınmaya devam ediliyor..{counter}")
                counter+=1
                file.write(temporary_bytes)
                temporary_bytes=client.recv(2048)
                
                if len(temporary_bytes)<2048:
                    file.write(temporary_bytes)
                    
                    ending_message=str(temporary_bytes)
                    print("\n serverdan son gelen mesaj verisi: \n",str(temporary_bytes))
                    break
            print("\nwhile sonlandı\n")  
            print("servardan gelen son resim mesajı şudur\t:" , ending_message) 
            # print("\n",ending_message.split("+++"))
       
            file.close()           
            print("servardan resim alımı tamamlandı")
            
            

            
            
            

#############################################################################################
#############################################################################################

def main():
    #yeni oluşan client otomatik olarak bizim server a bağlanır
    #program her çalışınca 1 client oluşur ama zaten biz 5 client için 5 kez cmd açacağız
    
    root.mainloop()
    # root2.mainloop()
    # root2.mainloop()
    
    
    
    #tkinter çalışmaya başlar
    
    #creating a socket object
    
    #ıpv4 ve tcp kullanan bir soket oluşturuyoruz
    
    #burada yaptıklarımız aynı olmalı  ki sever ve client iletişim kurabilsin
    
    
    
        
    #burada thread ile yapmadık çünkü client ın sürekli bir şeyi izlemesi gerekmiyor
    
#############################################################################################
#############################################################################################
        
if __name__ == '__main__':
    main()
    
    
