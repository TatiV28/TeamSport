from telethon import TelegramClient,sync, events, types
import pymorphy2
import re
import csv
import os.path
# Remember to use your own values from my.telegram.org!
api_id = 
api_hash = ''
client = TelegramClient('anon', api_id, api_hash)
@client.on(events.NewMessage(pattern=r''))

async def normal_handler(event):
    print(event.message)
    mes=str(event.message.message);
    mes = re.sub(r'[^\w\s]+[+]+[-]',' ',mes)
    id_client=int(re.sub("\D", "", str(event.message.peer_id)))
    print(re.sub("\D", "", str(event.message.peer_id)))
    if (os.path.isfile(str(id_client))==False):
        f = open(str(id_client), 'w')
        f.close()
        await event.reply('это ваше первое обращение ко мне сформилируйте вопрос и отправьте мне, и следуйте дальнейшим инструкциям. Если вдруг хотите задать новый вопрос напишите new или сразу текстом')
        
    if ((mes=='new') or (mes=='новый вопрос')):
        f = open(str(id_client), 'w')
        f.close()
        await event.reply('вводите новый вопрос')
    else:
        f = open(str(id_client), 'r')
        firstLine = f.readline()
        f.close()
        ses=firstLine.split(' ')         
        print(ses)
        words=mes.split()
        print(words)
        print(ses[0]+' '+words[0]+' '+str(len(ses))+' '+str((ses[0]=='id') and (words[0]=='-')and (len(ses)>2)))
        if ((ses[0]=='id') and (words[0]=='+')):
            #start fist step
            count=0
            with open(".//1w.csv", mode="r") as r_file1:
                reader = csv.DictReader(r_file1, delimiter=';')
                for row in reader:
                     if (row['id']==ses[1]):
                        await event.reply('Шаг 1: \n'+row['Шаг 1']+'? \n как выполните шаг напишите +')
                        for i in range(1,15):
                          if (row['Шаг '+str(i)])!=' ':
                              count=i+1
            count=count-1
            if count==1:
                f = open(str(id_client), 'w')
                await event.reply('Совет по прошлому вопросу дан!\n Задавай смелее новый вопрос')  
                f.close()
            print(' COUNT '+str(count))    
            f = open(str(id_client), 'w')
            f.write('step '+ses[1]+' 1 '+str(count))
            f.close()

        elif((ses[0]=='id') and (words[0]=='-')and (len(ses)>2)):
            #next question
            print('success')
            with open(".//1w.csv", mode="r") as r_file1:
                reader = csv.DictReader(r_file1, delimiter=';')
                for row in reader:
                     if (row['id']==ses[2]):
                        await event.reply('Ваш вопрос: \n'+row['Question']+'? \n если да, напишите +, иначе напишите -')
            del ses[1]
            f = open(str(id_client), 'w')
            f.write(' '.join(ses))
            f.close()
            print(' '.join(ses))
        elif((ses[0]=='step') and (words[0]=='+')):
            #next step
            count=0
            step=int(ses[2])+1
            with open(".//1w.csv", mode="r") as r_file1:
                reader = csv.DictReader(r_file1, delimiter=';')
                for row in reader:
                     if (row['id']==ses[1]):
                        await event.reply('Шаг '+str(step)+' из '+ses[3]+': \n'+row['Шаг '+str(step)]+'? \n как выполните шаг напишите +')    
            f = open(str(id_client), 'w')
            if (step<int(ses[3])):
                f.write('step '+ses[1]+' '+str(step)+' '+ses[3])
            else:
                f.write()
                await event.reply('Задавай смелее вопрос')  
            f.close()
        elif((ses[0]=='id') and (words[0]=='-')and (len(ses)==2)):
            #next question
            await event.reply('Переформулируйте вопрос')
            f = open(str(id_client), 'w')
            f.close()
        else:             
            morph = pymorphy2.MorphAnalyzer()
            i=len(words)-1
            for word in reversed(words):
                        type_word=morph.parse(word)[0].tag.POS
                        #print(type_word+' ')
                        if ((type_word=="PREP") or (type_word=="CONJ") or (type_word=="INTJ") or (type_word=="PRCL")):
                            del words[i]
                            i=i-1
                        else:
                            words[i]=morph.parse(word)[0].normal_form
                            i=i-1            
            with open(".//1w.csv", mode="r") as r_file1:
                reader = csv.DictReader(r_file1, delimiter=';')
                curaccur2=0;
                curaccur3=0;
                curaccur4=0;                
                print(words)
                row2=[]
                row3=[]
                row4=[]
                for row in reader:
                   sub=row['word_help']
                   wordsr=sub.split()
                   accur=10000.000*len(list(set(wordsr) & set(words)))/len(wordsr)
                   #print(words, ' ',wordsr,' ',list(set(wordsr) & set(words)), ' ', accur)
                   if ((accur>curaccur2)):
                       row4=row3
                       row3=row2
                       row2=row
                       curaccur2=accur
                       #print(curaccur)
                   if ((accur>curaccur3) and (row['id']!=row2['id'])):
                       row4=row3
                       row3=row
                       curaccur3=accur
                   if ((accur>curaccur4)and (row['id']!=row2['id'])and (row['id']!=row3['id'])):
                       row4=row
                       curaccur4=accur
            if (curaccur2==0):
                if ((mes=='+') or (mes=='привет')or (mes=='как дела')):
                    await event.reply('Смелее задай вопрос!')
                else:
                    await event.reply('не могу ответить на ваш вопрос')
                    f=open('messages_from_chat', 'a')
                    f.write(' '+event.message.message+'\n')
                    f.close()
            else:
                ans='id '+row2['id']
                if (curaccur3>0):
                    ans=ans+' '+row3['id']
                if (curaccur4>0):
                    ans=ans+' '+row4['id']
                f = open(str(id_client), 'w')
                f.write(ans)
                f.close()
                
                await event.reply('Ваш вопрос: \n'+row2['Question']+'? \n если да, напишите +, иначе напишите -')
            print(words)
    
    

client.start()
print("start")


#user_markup.row('/start') 


client.run_until_disconnected()
#f.close()
