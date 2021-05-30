import taurus

f=open("taurus.txt","r")
print(f.read())

while(True):
    text=input("taurus> ")
    if text=="exit":
        print("Exiting Taurus Terminal!!!!")
        break
    result,err=taurus.run('<stdin>',text)
    
    if err:print(err.error())
    else:print(repr(result))
    
    