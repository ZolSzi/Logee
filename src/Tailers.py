'''
Created on 2013.05.22.

@author: Zoltan Sziladi
'''
import os
import threading
import time

class FileTailer(object):
    '''
    Responsible for tailing a file in the local file system
    '''


    def __init__(self, filepath):
        '''
        Constructor
        '''
        self.filepath = filepath
        self.line_terminators_joined = '\r\n'
        self.filesize = None
        self.file = None
        self.thread = threading.Thread(target=self.read_lines)
        self.thread.daemon = False
        
    
    def listen(self, callback):
        self.callback = callback
        
    def stop_listening(self):
        self.callback = None;
        
    def tail(self):
        filestat = os.stat(self.filepath)
        if self.filesize is None:
            self.filesize = filestat.st_size
        self.file = open(self.filepath)
        self.thread.start()
            
    def read_lines(self):
        while self.callback is not None:
            filestat = os.stat(self.filepath)
            if self.filesize < filestat.st_size:
                self.file.seek(self.filesize)
                line = self.file.readline()
                while line:
                    self.callback(line.strip(self.line_terminators_joined))
                    line = self.file.readline()
                self.filesize = filestat.st_size
            time.sleep(1)
                    