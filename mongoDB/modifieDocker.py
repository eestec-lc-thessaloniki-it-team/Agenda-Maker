#!/usr/bin/python3

import sys,os

#fill these 2 with your username and database name that you give in the init-mongo.js
username="mavroudo"
dbname="mongo_db"

help=\
"""The valid parameters are :
        destroy: completely deletes the docker image and volumes
        start : creates and start the daemon for mongo
        stop   : stops the docker
        restart: restarts the docker
        connect: to connect to the database
    You can only use one of them
"""
def printhelp():
    print(help)

def stop():
    t=os.system("docker-compose stop")

def destroy():
    stop()
    t=os.system("rm -r mongo-volume")
    t=os.system("docker-compose rm -v")

def start():
    t=os.system("docker-compose up -d")

def restart():
    t=os.system("docker-compose restart")

def connect():
    t=os.system("""docker exec -it mongo-container-local mongo -u {} --authenticationDatabase {}""".format(username,dbname))

def mode(chosedMode:str):
        switcher={
            "destroy": destroy,
            "start":start,
            "stop":stop,
            "restart":restart,
            "connect":connect

        }
        fun=switcher.get(chosedMode,lambda: printhelp())
        fun()


if __name__=="__main__":
    chosedMode=sys.argv[1:]
    if len(chosedMode)>1:
        printhelp()
    func=mode(chosedMode[0])








