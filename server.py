
from http import client
import socket
import threading
import _thread
import PIL.Image as Image 
import io
import base64
import zlib


# HOST="192.168.0.101"
HOST="127.0.0.1"

PORT=1234  #0-65535 range
LISTENER_LIMIT=5

active_clients=[]   #bağlı olan tüm kullanıcılar  ((username1,client1),(username2,client2),... )

#sürekli gelen mesaj var  mı diye bakacak---------------------------------------------------------------

            
            
#client gelirse ondan gelen mesajı alacak ve client ı listeye ekleyecek----------------------------------------
#burası trhread e bağlı olduğu için her yeni client gelince çalıacak ve her yeni gelen clietn ı handle edecek 
def client_handler(client):
    #server burada client ın mesajını bekleyecek/ mesaj client ismiyle birlikte gelecek
    temporaryClient=("","")
    while 1:
        clientInfos=client.recv(2048).decode("utf-8")
        #huseyin,0534
        mesajGondereninTelefonu=clientInfos.split(",")[1]
        #!!!! client tarafında bağlantı kurulunca ilk olarak username i gönderdiğimiz için
        #ilk gelen mesajı da otomatik olarak username olarak aldık (server tarafında)
        
        #her zaman sen yaparken encode yap, recv yaprken decode yap
        #encode ederken parametre yok ama decode ederken utf 8 e göre
        #gelen mesajı decode ederiz (çözümleriz)
        #gelen mesajı aldık
        if clientInfos!="":
            temporaryClient=clientInfos.split(",")
            active_clients.append((temporaryClient,client))
            print(active_clients[len(active_clients)-1][0][1], "telefon numaralı client listeye eklendi" )
            break
            #burada break i yazmazsak saçmalıyor...
            # ( ("hüseyin","0534"),client1 ),   ( ("selim","0539"),client2 )
            
        else:
            print("client'dan kullanıcı adı boş geldi")
            
        #kullanıcı listeye eklendiğin anda listeye yeni eklenen client dan gelen mesajlar dinlenmeye başlar
        
        
    threading.Thread(target=listen_for_messages, args=(client,mesajGondereninTelefonu)).start()
    
    
def listen_for_messages(client,mesajGondereninTelefonu):
    #print(active_clients[0][1].getsockname)  
    #mesajGondereninTelefonu resim alma işlemi için de aynı şekilde geçerlidir
    while 1:      
        print(f"listening for mesages from {mesajGondereninTelefonu}")
        
        gelen_ana_mesaj=client.recv(2048).decode("utf-8")
        #hem text hem de resim mesasları gelen_ana_mesaj değişkenine atanacak
        #ama text mesaj gelirse yalnızca for ile gönderilen ilk parça gelecek ki,
        #yalnızca string e çevirip ilk kısmını starts with ile kontrol edeceğimiz için sıknıtı oluşturmaz
        
        #burada clientın ilk send isteği buraya gelmiş olacağı için,(resim gönderdiğinde)
        #client resim gönderirken for döngüsünde ilk yaptığı işlemi manuel olarak da önceden 1 kez göndermemiz gerekir
        #----------------------------------
        if str(gelen_ana_mesaj).startswith("**text_message_beginning**"):
            mesajVeGonderilecekTelefonBilgisi=gelen_ana_mesaj
            mesajVeGonderilecekTelefonBilgisi=mesajVeGonderilecekTelefonBilgisi.replace("**text_message_beginning**","")
            mesajVeGonderilecekTelefonBilgisi=mesajVeGonderilecekTelefonBilgisi.replace("**text_message_end**","")
            
            #üstteki 2 satır değişmesin bozuluyor
            
            print(mesajVeGonderilecekTelefonBilgisi)
            
            #for multiple stuations: "selam~0534,0536"
            message=mesajVeGonderilecekTelefonBilgisi.split("~")[0]
            gonderilenTelefon=mesajVeGonderilecekTelefonBilgisi.split("~")[1]
            telefonlar=gonderilenTelefon.split(",")
            #point here--------
            #  "0534,0536,0537"
            #gelen mesajı aldık
            if message!="":
                final_msg=mesajGondereninTelefonu+"~"+message
                #tekKullanıcıyaGonderilecekMesaj=mesajGondereninTelefonu+","+message+","+gonderilenTelefon
                # ( ("hüseyin","0534"),client1 )   ,( ("selim","0539"),client1 )
                for i in telefonlar:
                    for index in active_clients:
                        if index[0][1]==i:
                            aranan_index=index
                    #aranan index= ("hüseyin","0534"),client1 )
                    asıl_gonderilen_telefon_clientı=aranan_index[1]
                    asıl_gonderilen_telefon_clientı.sendall("text_from_server".encode())
                    send_message_to_client(asıl_gonderilen_telefon_clientı,final_msg)
                
                #client a text mesajı geldiğini bildiriyoruz
                
                
                print(f"{mesajGondereninTelefonu} telefon numaralı client  şu mesaj gönderdi:  {message}")
            
    
                #bu şekilde tek bir kullanıcıya aşağıdaki gibi bir mesajı iletecek fonksiyona şu parametreler gider
                #  "0534,selam,0537"
                          
                #send_message_to_all(final_msg) ****************************************************

                
            else:
                print(f"{mesajGondereninTelefonu} telefon nolu client'dan mesaj boş geldi")

        else:
            #------------------------------------ text değil de resim mesajları için çalışacak kısım
            print("resim gelmeye başladı")
            #client içinde resim alma bloğuna girebilmek için burdan bir mesaj atıyoruz(text halinde)
            
            
            resimGonderen=mesajGondereninTelefonu
            resimGonderilen=str(gelen_ana_mesaj).split(",")[1]
            print(f"\nresim gonderen: {resimGonderen}, resim gonderilen: {resimGonderilen}")
            #bu haliyle hem resimleri hem de alıcıyı, göndereni alabiliyoruz
            
            # ( ("hüseyin","0534"),client1 )   ,( ("selim","0539"),client1 )
            for index in active_clients:
                if index[0][1]==resimGonderilen:
                    aranan_index=index
            #aranan index= ("hüseyin","0534"),client1 )
            resimGonderilenClient=aranan_index[1]
            resimGonderilenClient.sendall("image_from_server".encode())
            #burası client ın image bloğuna girmesini sağlar
            
            
            #bu üstteki blokta bir hata var düzelmesi gerek
            
            
            
            file=open('picture_on_server.jpg',"wb")
            temporaryBytes=client.recv(2048)
            
 
 
 
 #burada alınan tüm bytes ları aynı anda dosyaya yazdırıp gerekli clienta da geri yoluuyoruz
            ending_message=""
            counter=1  
            while True:
                print(f"resim mesajı alınmaya devam ediliyor..{counter}")
                counter+=1
                file.write(temporaryBytes)
                resimGonderilenClient.send(temporaryBytes)
                temporaryBytes=client.recv(2048)
                
                #üstteki 2 satırın yerini değiştirme sıkıntı çıkabiliyor..!!
                
                #tam burası client a giden ilk resim bytes parçası olur
                
                
                #---------
                #tam bu satırda gönderme işlemi yapılır-----------------
                #-------
                #burada 2048 dolana kadar almaya devam ettiği için
                #resmin son parçası ile "**image_message_end**,1" kısmı birleşik geliyor -- sorun
                # print(temporaryBytes)
                # length = len(temporaryBytes)
                # print("\n",f"size= {length} ")
                #bu şekilde gelen verinin size ını buluruz, bu if e gelindiğince son byte da alınmış olur
                if len(temporaryBytes)<2048:
                    file.write(temporaryBytes)
                    resimGonderilenClient.send(temporaryBytes)
                    #burada küçük olan son bytes ı dosyaya yazmayı unutuyorduk, onu düzelttim
                    
                    
                    
                    #son paketi aldık demektir
                    # str(temporaryBytes).startswith("b\'**image_message_end**")
                    #b'**image_message_end**'
                    #son bitti mesajı da byte halinde geleceği için bytes halinin stringini yazdım ve ona göre kontrol ettim
                    ending_message=str(temporaryBytes)
                    print("\n son gelen veri: \n",str(temporaryBytes))
                    break
            print("\nwhile sonlandı\n")  
            print("son mesaj şudur\t:" , ending_message) 
            # print("\n",ending_message.split("+++"))
       
            file.close()           
            print("resim alımı tamamlandı")
            
            
            #burada tüm bytesları client tarafına gönderdik ancak alıcı ilk text  mesajımızdan sonraki
            #bytes mesajlarımızı da alıp decode etmek istiyor ve bu yüzden client tarafında hata alıyoruz
            #bu durumun client tarafında düzelmesi gerekir
            
        
            
            
            
            
            
#////////////////////////////////////////////////////////////////////////////////////////////////////// 


           
#//////////////////////////////////////////////////////////////////////////////////////////////////////
# tek bir client'a mesaj gönder ------------------------------------------------------------------------------
def send_message_to_client(client,message):
    client.sendall(message.encode()) 
    #client değişkenine mesajı yolla
    


# tüm clientlara mesaj gönder------------------------------------------------------------------------------
def send_message_to_all(message):
    #burası tğm aactive clientler için tek tek send_message_to_client fonksiyonunu çalıştırır ve 
    #listedki her bir elemanın ağzından diğer tüm kullanıcılara bir mesajı gönderir
    for user in active_clients:
        send_message_to_client(user[1],message)
        #user[1] zaten burada client nesnesi olmuş oluyor
        #zaten gelen veir
        
        # ( ("hüseyin","0534"),client1 )  ,  ( ("selim","0539"),client2 ),( ("beyza","0537"),client3 )
        #client.sendto(anotherShouldBeAnotherClientButNotSure)
        

#############################################################################################
#############################################################################################
#Main function
def main():
    #Creating the socket and object
    server= socket.socket(socket.AF_INET,socket.SOCK_STREAM)  #ıpv4 and tsp
    
    try:
        server.bind((HOST,PORT))
        print("başarıyla bağlantı oluşturuldu")
    except:
        print(f"{HOST}numaralı hosta ve {PORT} numaralı bağlantıyı yaratırken hata oluştu")
    
    
    server.listen(5)
    #aynı anda max 5 client
    
    
    #bağlantı kurulmadan buraya bakılmaz bile
    #bağlantı kurulunca bağlanan client ın ismi alınır ve object olarak kendisi alınır
    while 1:
        print("#gelecek client'lar için bekleniyor")
        client,address=server.accept() 
        #print(client.getsockname)
        #burada address bir touple dır ve client ın host ve port unu tutar address=(host,port)
        print(f"{address[0]} host numarasına ve {address[1]} soket numarasına sahip client'a başarıyla bağlanıldı")
        
        #sürekli client var mı diye bakacağımız için  thread yapıyoruz
        
        threading.Thread(target=client_handler, args=(client,)).start()
        
#############################################################################################
#############################################################################################
        

if __name__ == '__main__':
    main()
    
    