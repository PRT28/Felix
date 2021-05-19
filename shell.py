import felix

while(True):
    text=input("felix> ")
    if text=="exit":
        print("Exiting Felix Terminal")
        break
    result,err=felix.run('<stdin>',text)
    
    if err:print(err.error())
    else:print(result)
    
    