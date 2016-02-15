'''
#-*- coding: utf-8 -*-  
#python3.0 scaner1.py 
Created on 2016年2月3日
@author: age

不同平台，实现对所在内网端的ip扫描 
使用方法 python ip_scaner.py 192.168.1.1 
(会扫描192.168.1.1-255的ip) 
'''
  
import platform 
import sys 
import os 
import time 
import threading 
import smtplib  
from email.mime.text import MIMEText  
from email.header import Header  
  
def get_os():   #获得os的类型，区分，n和c作用；
    os = platform.system() 
    if os == "Windows": 
        return "n"
    
    else: 
        return "c"
    #print('OS is ',os)    #此处为何不打印？应为return会断开程序，造成无法进行；
    #print ('123123456')
    
def ping_ip(ip_str):
    #global j 
    
    cmd = ["ping", "-{op}".format(op=get_os()),"1",ip_str] 
    output = os.popen(" ".join(cmd)).readlines() 
    
    flag = False
    for line in list(output): 
        if not line: 
            continue
        if str(line).upper().find("TTL") >=0:   #find()返回第一次出现位置；否则为-1；
            flag = True
            break   #break，用法不熟练；
    if flag: 
        print ("ip: %s is ok "%ip_str)
        #把结果写进txt，发送email；
        f=open('ip.txt','a')
        f.write(ip_str)
        f.write(time.ctime())
        f.write('\n')
        
        #print(j)
        #print('正在操作：',output[0])

#尝试改写多线程模块：
def find_ip(ip_prefix):
    threads=[]
    global j
    for i in range(1,25):    #循环次数；
        pass
        ip='%s.%s'%(ip_prefix,i)
        #print("i=",i,"  ip=",ip)
        t=threading.Thread(target=ping_ip,args=(ip,))
        #t=threading.Thread(ping_ip,(ip,))
        threads.append(t)
        #print(t)
    #for j in range(0,24):    #启动线程个数
    for j in threads:
        j.start()
        #print(j)    #打印threads[]；
    #for k in range(0,24):    #等待线程个数；
    for k in threads:
        k.join()
        #threads[k].join()
        
def send_email(): 
    content='测试'
    sender = 'lw2006wl@126.com'  
    receiver = 'julietliuw@sina.com'  
    subject = 'email test'  
    smtpserver = 'smtp.126.com'  
    username = 'lw2006wl@126.com'  
    password = 'liuwei@2006'  
    
    #msg = MIMEText('你好,abcd','plain','utf-8')    #下移；
    
    #msg['Subject'] = Header(subject, 'utf-8')
    
    
    try:
        f=open('ip.txt')
        ip=f.readlines()
        content="".join(ip)     #记住用法！！！
        msg = MIMEText(content,'plain','utf-8')
        msg['Subject'] = Header(subject, 'utf-8')
        #content=ip
        smtp = smtplib.SMTP()  
        smtp.connect('smtp.126.com')  
        smtp.login(username, password)  
        smtp.sendmail(sender, receiver, msg.as_string())  
        smtp.quit()  
        print('done')
    except Exception as e:
        print(str(e))
         
    finally:
        f.close()
    

        

if __name__ == "__main__": #参数172.24.100.1
    print ("start time %s"%time.ctime()) 
    #get_os()
    commandargs = sys.argv[1:]  #args[]是一个参数列表，需要拿出来；
    print('1,commandargs=',commandargs) 
    args = "".join(commandargs) #此处编程一个string；方便使用
    print('2,args=',args)   
    
    ip_prefix = '.'.join(args.split('.')[:-1]) 
    print("3,ip_prefix=",ip_prefix)
    find_ip(ip_prefix) 
    send_email()
    #print(ip_list)
    print ("end time %s"%time.ctime())
    
    
    
    
    