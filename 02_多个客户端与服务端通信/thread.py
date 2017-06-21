import threading 

def  print_work(cnt):
    for i in range(cnt):
        print('new thread print:', i)


t = threading.Thread(target=print_work, args=(10,))
t.start();
sum = 0
for i in range(100):
    sum = sum + i 
print('Sum =', str(sum))