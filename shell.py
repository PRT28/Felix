import taurus

f=open("taurus.txt","r")
print(f.read())

while(True):
    text=input("taurus> ")
    if text.strip() == "": continue
    if text=="exit":
        print("Exiting Taurus Terminal!!!!")
        break
    result,err=taurus.run('<stdin>',text)
    
    if err:print(err.error())
    elif result:
        if len(result.elements) == 1:
            print(repr(result.elements[0]))
        else:
            print(repr(result))
    
    