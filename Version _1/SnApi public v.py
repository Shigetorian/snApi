import json
import random
import time
import datetime
import os
import threading
from os.path import basename
from tkinter import *
from tkinter import filedialog as fd
from tkinter.filedialog import askdirectory
try:
    import progressbar
except:
    os.system('pip install progressbar')
    import progressbar
try:
    import yadisk
except:
    os.system('pip install yadisk')
    import yadisk


class snApi():
    def __constant_init(self):
        self.user = {
            'username': '',
            'password': ''

        }
        self.userdata = {
            'username': "",
            'status': "",
            'all_post': 0,
            'views': 0,
            'achievement': 0

        }
        self.post = {
            'theme': "",
            'text': [],
            'file': [],
            'data': ""

        }
        self.file = {
            'filename': "",
            'username': "",
            'updata': "",
            'link': ""

        }
        self.profile = {
            'username': "",
            'status': "",
            'views': 0,
            'all_post': 0,
            'achievement': 0,
            'posts': []
        }
        self.message = {
            'username': "",
            'theme': "",
            'text': [],
            'file': [],
            'data': ""

        }
        self.mail = {
            'inbox': '',
            'sent': ''

        }
        self.pbar = False

    def __time(self):
        return time.strftime("%d-%m-%Y %H:%M", time.localtime())

    def file_path(self):
        root = Tk()
        path = fd.askopenfilename()
        root.destroy()
        root.mainloop()
        return path

    def __thread(self):
        while True:
            if self.pbar == True:
                bar = progressbar.ProgressBar().start()
                for t in range(100):
                    bar.update(t)
                    time.sleep(0.05)
                    if self.pbar == False:
                        bar.finish()
                        t = 0
                        break

                bar.finish()
            else:
                continue

    def __fs_init(self):
        self.server_main = "<token>"

    def __thread_init(self):
        my_thread = threading.Thread(target=self.__thread)
        my_thread.start()

    def files_load(self):
        try:
            self.__fs_download_user(self.user['username'], 'files.json')
            files = json.load(open('cash/files.json', mode='r'))
            os.remove('cash/files.json')
            return files
        except:
            return False

    def profile_load(self, username):
        try:
            self.pbar = True
            userdata = self.download_userdata(username)
            posts = self.__posts_load(username)
            self.__change_views(username, userdata['views']+1)
            self.profile['username'] = userdata['username']
            self.profile['status'] = userdata['status']
            self.profile['views'] = userdata['views']+1
            self.profile['all_post'] = userdata['all_post']
            self.profile['achievement'] = userdata['achievement']
            self.profile['posts'] = posts
            self.pbar = False
            return self.profile
        except:
            self.pbar = False
            return False

    def __posts_load(self, username):
        self.__fs_download_user(username, 'posts.json')
        posts = json.load(open('cash/posts.json', mode='r'))
        os.remove('cash/posts.json')
        return posts

    def __fs_update_fs(self):
        self.__fs_download_user(self.user['username'], 'files.json')
        files = json.load(open('cash/files.json', mode='r'))
        files.append(self.file)
        self.__fs_upload_user(files, 'files.json')

    def __fs_upload_user(self, data, filename, username=None):
        if username == None:
            json.dump(data, open('cash/'+filename, mode='w'))
            self.s0.upload('cash/' + filename, 'users/' +
                           self.user['username']+'/'+filename, overwrite=True)
            os.remove('cash/'+filename)
        else:
            json.dump(data, open('cash/'+filename, mode='w'))
            self.s0.upload('cash/' + filename, 'users/' +
                           username+'/'+filename, overwrite=True)
            os.remove('cash/'+filename)

    def __fs_upload_file(self, path):
        self.file['username'] = self.user['username']
        self.file['updata'] = self.__time()
        self.file['filename'] = str(basename(path))
        self.s0.upload(
            path, 'files/'+self.user['username']+'/'+self.file['filename'], overwrite=True)
        self.file['link'] = self.s0.get_download_link(
            "files/"+self.user['username']+'/'+self.file['filename'])
        self.__fs_update_fs()

    def upload_file(self, file):
        try:
            self.pbar = True
            self.__fs_upload_file(file)
            self.pbar = False
            return True
        except:
            self.pbar = False
            return False

    def __fs_download_user(self, username, filename):
        self.s0.download('/users/' + str(username) + '/' +
                         filename, 'cash/' + filename)

    def download_file(self, filename):
        try:
            self.pbar = True
            path = askdirectory()
            self.s0.download('/files/' + self.user['username'] + '/' +
                             filename, path+'/'+filename)
            self.pbar = False
            return True
        except:
            self.pbar = False
            return False

    def remove_user(self, username):
        try:
            self.pbar = True
            self.s0.remove('users/' + str(username), permanently=True)
            self.s0.remove('files/' + str(username), permanently=True)
            self.pbar = False
            return True
        except:
            self.pbar = False
            return False

    def remove_file(self, filename):
        try:
            self.pbar = True
            self.s0.remove('files/' +
                           self.user['username']+'/'+filename, permanently=True)
            self.pbar = False
            return True
        except:
            self.pbar = False
            return False

    def upload_userdata(self, username, status):
        try:
            self.pbar = True
            self.userdata['username'] = username
            self.userdata['status'] = status
            self.__fs_upload_user(self.userdata, 'userdata.json')
            self.pbar = False
            return True
        except:
            self.pbar = False
            return False

    def download_userdata(self, username=None):
        try:
            if username != None:
                self.__fs_download_user(username, 'userdata.json')
                data = json.load(open('cash/userdata.json', mode='r'))
                os.remove('cash/userdata.json')
                return data
            else:
                self.__fs_download_user(self.user['username'], 'userdata.json')
                data = json.load(open('cash/userdata.json', mode='r'))
                os.remove('cash/userdata.json')
                return data
        except:
            return False

    def write_post(self, theme, text, files=None):
        self.pbar = True
        self.__fs_download_user(self.user['username'], 'posts.json')
        posts = json.load(open('cash/posts.json', mode='r'))
        if files != None:
            for file in files:
                self.__fs_upload_file(file)
                self.post['file'].append(self.file['link'])
        else:
            self.post['file'] = None
        self.post['theme'] = str(theme)
        self.post['text'] = text
        self.post['data'] = self.__time()
        posts.append(self.post)
        self.__change_all_post(self.user['username'], len(posts))
        self.__fs_upload_user(posts, 'posts.json')
        self.pbar = False
        return posts

    def __change_statistics(self, username):
        pass

    def __change_views(self, username, views):
        self.userdata = self.download_userdata(username)
        self.userdata['views'] = views
        self.__fs_upload_user(self.userdata, 'userdata.json')

    def __change_all_post(self, username, all_post):
        self.userdata = self.download_userdata(username)
        self.userdata['all_post'] = all_post
        self.__fs_upload_user(self.userdata, 'userdata.json')

    def send_mail(self, username, theme, text, files):
        self.pbar = True
        self.__fs_download_user(username, 'inputm.json')
        messages = json.load(open('cash/inputm.json', mode='r'))
        if files != None:
            for file in files:
                self.__fs_upload_file(file)
                self.message['file'].append(self.file['link'])
        else:
            self.message['file'] = None
        self.message['username'] = self.user['username']
        self.message['theme'] = str(theme)
        self.message['text'] = text
        self.message['data'] = self.__time()
        messages.append(self.message)
        self.__fs_upload_user(messages, 'inputm.json', username)
        self.__fs_download_user(self.user['username'], 'outputm.json')
        outmessages = json.load(open('cash/outputm.json', mode='r'))
        self.message['username'] = username
        outmessages.append(self.message)
        self.__fs_upload_user(outmessages, 'outputm.json',
                              self.user['username'])
        self.pbar = False
        return messages

    def load_mail(self, username):
        self.__fs_download_user(username, 'outputm.json')
        self.__fs_download_user(username, 'inputm.json')
        self.mail['inbox'] = json.load(open('cash/inputm.json', mode='r'))
        self.mail['sent'] = json.load(open('cash/outputm.json', mode='r'))
        os.remove('cash/outputm.json')
        os.remove('cash/inpputm.json')
        return self.mail
    def init(self):
        self.pbar = True
        self.__constant_init()
        self.__fs_init()
        # self.__thread_init()
        self.s0 = yadisk.YaDisk(token=self.server_main)
        try:
            file = open('cash/usercash.json', mode='r')
            rest = json.load(file)
            self.pbar = False
            return str(rest)
        except:
            self.pbar = False
            return False

    def signup(self, username, password):
        try:
            self.pbar = True
            self.__fs_download_user(username, "userget.json")
            os.remove('cash/userget.json')
            rt = random.randint(0, 1000)
            self.user['username'] = str(username)+str(rt)
            self.user['password'] = str(password)
            self.s0.mkdir('/users/'+self.user['username'])
            self.s0.mkdir('/files/'+self.user['username']+'/')

            self.__fs_upload_user(self.user, 'userget.json')
            self.__fs_upload_user([], 'posts.json')
            self.__fs_upload_user([], 'inputm.json')
            self.__fs_upload_user([], 'outputm.json')
            self.__fs_upload_user([], 'files.json')
            self.pbar = False
            return self.user['username'], self.user['password']
        except:
            self.pbar = True
            self.user['username'] = str(username)
            self.user['password'] = str(password)
            self.s0.mkdir('/users/'+self.user['username'])
            self.s0.mkdir('/files/'+self.user['username'])

            self.__fs_upload_user(self.user, 'userget.json')
            self.__fs_upload_user([], 'posts.json')
            self.__fs_upload_user([], 'inputm.json')
            self.__fs_upload_user([], 'outputm.json')
            self.__fs_upload_user([], 'files.json')
            self.pbar = False
            return True

    def auth(self, username, password):
        try:
            self.pbar = True
            self.__fs_download_user(username, 'userget.json')
            self.user = json.load(open('cash/userget.json', mode='r'))
            os.remove('cash/userget.json')
            password_n = self.user['password']
            if password == password_n:
                json.dump(username, open('cash/usercash.json', mode='w'))
                self.pbar = False
                return True
            else:
                self.pbar = False
                return False
        except:
            self.pbar = False
            return False
