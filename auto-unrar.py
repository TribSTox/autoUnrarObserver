#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Directory observer for automatically unrar files
# arg : path to observe
# optional arg : path to unrar
# dependencies : pip install watchdog pyunpack

import sys, os
from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer
 
pathToObserve = sys.argv[1]
try:
    pathWhereUnrar = sys.argv[2]
except:
    pathWhereUnrar = sys.argv[1]
 
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class MonHandler(FileSystemEventHandler):

    # appelée à chaque fois qu'un fichier est créé
    def on_created(self, event):
        _, ext = os.path.splitext(event.src_path)
        if ext[1:] == "rar":
            print("Decompression du fichier %s !" % event.src_path)
            from pyunpack import Archive
            Archive(event.src_path).extractall(pathWhereUnrar)

observer = Observer()
# Surveiller récursivement tous les événements du dossier fourni en argument
# et appeler les méthodes de RarHandler quand un fichier est créé
observer.schedule(MonHandler(), path=pathToObserve, recursive=True)


observer.start()

# boucle infinie pour maintenir le thread principal actif
try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    # Ctrl + C arrête tout
    observer.stop()
# on attend que tous les threads se terminent proprement
observer.join()
