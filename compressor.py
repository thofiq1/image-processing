
import os
from tkinter import *
from tkinter import messagebox
from PIL import Image
from io import BytesIO
   
path=''
maxsize=1500

def is_transparent(image):
    trans=False
    data = image.getdata()
    #lofpixels = []
    for pixel in data:
        if type(pixel) is tuple:
            if len(pixel)>3:
                alpha=pixel[-1]
                #print(alpha)
                if alpha==0:
                    trans=True
                    break
                else:
                    trans=False
            else:
                trans=False
                
        else:
            
            if pixel==0:
                trans=True
                break
            else:
                trans=False
                
                
    return trans
        # lofpixels.append(pixel)
    
def convert_to_jpg(image):
    
    im=Image.open(path+"/"+image)
    for i in range(len(image)):
        if image[i]==".":
            index=i
    newname=image[0:index]
    im = im.convert('RGB')
    #im.save(path+"/"+newname+".jpg")
    return im,newname+".jpg"

def imgWrite(img,imgname):
    img.save(path+"/newimages/"+imgname,quality=5000)


def checksize(w,h):
    ratio=w/h
    
    if ratio>1:
        width=maxsize
        height=maxsize*h//w
        # print("ORIGINAL SIZE: "+str(w)+" x "+str(h))
        # print("LANDSCAPE MODE: "+str(width)+" x "+str(height))
    else: 
        height=maxsize
        width=maxsize*w//h
        # print("ORIGINAL SIZE: "+str(w)+" x "+str(h))
        # print("PORTRAIT MODE: "+str(width)+" x "+str(height))
    return width,height
def convert_to_png(image):
    im=Image.open(path+"/"+image)
    # for i in range(len(image)):
    #     if image[i]==".":
    #         index=i
    # newname=image[0:index]
    im = im.convert('RGB')
    #im.save(path+"/"+newname+".jpg")
    
    return im,image

def TakePath():
    
    master = Tk() 
    master.geometry('500x500')
    master.title("Image Post-Processor ")
    master.resizable(0,0)
    label1=Label(master,text="Image Post-Processor",width=30,font=("bold",20))
    label1.place(x=5,y=20)
    label2=Label(master,text="Enter Folder Path*",width=20,font=("bold",10))
    label2.place(x=100,y=130)
    entry_1 = Entry(master)
    entry_1.place(x=240,y=130)
    label3=Label(master,text="Enter Maximum Size",width=20,font=("bold",10))
    label3.place(x=90,y=180)
    entry_2 = Entry(master)
    entry_2.place(x=240,y=180)
    def retrieve_input():
        global path
        global maxsize
        path=entry_1.get()
        maxsize=entry_2.get()
        if path !='':
            try:
                f = os.listdir(path)
                master.destroy()
                
            except:
                messagebox.showinfo("Error", "Please Enter Valid Image Path")
            
            
        else:
            messagebox.showinfo("Error", "Please Enter The Image Path")
        if maxsize != '':
            try:
                maxsize=int(maxsize)
            except:
                messagebox.showinfo("Error", "Please Enter int")
        
        return path,maxsize

    button = Button(master, text='Submit', width=15, command=lambda:[retrieve_input()]) 
    button.place(x=200,y=240)
    mainloop() 

def main():
    global path
    global maxsize
    TakePath()
    if maxsize=='':
        maxsize=1500
    maxsize=int(maxsize)
    files =os.listdir(path)
    
    
    if not os.path.exists(path+"/newimages"):
        os.makedirs(path+"/newimages")
    for newimage in files:
        if os.path.isfile(os.path.join(path, newimage)):
            try:   
                fl=Image.open(path+"/"+newimage)
            except:
                continue
            trans=is_transparent(fl)
            print(newimage+"     "+str(trans))
            if trans is False:                
                fl,newimage=convert_to_jpg(newimage)
                #fl=Image.open(path+"/"+newimage)
            elif fl.format != "PNG":
                fl,newimage=convert_to_png(newimage)
            img_file = BytesIO()  
            if fl.size[1]>maxsize or fl.size[0]>maxsize:
                w,h=checksize(fl.size[0],fl.size[1])
                ow=fl.size[0]
                oh=fl.size[1]
                osize=os.path.getsize(path+"/"+newimage)
                
                print(os.stat(path+"/"+newimage).st_size)
                fl=fl.resize((w,h),Image.ANTIALIAS)
            
            imgWrite(fl,newimage)
            print(img_file.tell())
            
if __name__=="__main__":
    main()