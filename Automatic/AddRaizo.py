#!usr/bin/python

import os, stat, subprocess, shlex, re, sys

number = ""
letter = ""

#search the partition number to use in the menu entry on 40_custom file
def searchPartitionNumber():
        print("\33[0;34mSearching where is mounted \33[4;35m/\33[0m")
        #search the path of the partition, for example: /dev/sda1
        out = subprocess.Popen(shlex.split("df /"), stdout=subprocess.PIPE).communicate()
        aux=re.search(r'(/[^\s]+)\s',str(out))
        #comprobe if the path was found and get the path
        if aux:
                path= aux.group(1) 
                global letter
                letter = str(ord(path[7:8])- 97)
                global number
                number = path[8:]
        else:
                print ("cannot parse df") 
                sys.exit(2)
        #print the results
        print ("\t\33[4;35m/\33[0;34m mounted at \33[4;35m%s\33[0;34m - \33[5;93m(hd%s,%s)" % (path,letter,number))

#download last Raizo ISO and put in /boot-isos directory
def downloadISO(file_path):
        command = "wget https://sourceforge.net/projects/live-raizo/files/latest/download -O " + file_path
        print("\t\33[6;33mDownloading Live-Raizo.iso...\n\33[0;34m")
        os.system(command)
        print("\t\33[6;32mLive-Raiso.iso downloaded")

#add raizo menu entry in your linux
def addEntry(file_path):
        print("\n\33[0;34mAdding \33[0;37mLive-Raizo \33[0;34mmenu entry")
        #Insert the new Menu Entry in 40_custom file
        with open(file_path,'a+') as custom_file:
                custom_file.write("\n\nmenuentry \"Live-Raizo\" --class live-raizo --class debian --class gnu-linux --class gnu --class os {\n")
                custom_file.write("\techo \"Loading Live-Raizo ISO\"\n")
                custom_file.write("\tinsmod iso9660\n")
                custom_file.write("\tset isofile=\"/boot-isos/Live-Raizo.iso\"\n")
                custom_file.write("\tloopback loop (hd"+ letter +","+ number +")$isofile\n")
                custom_file.write("\tlinux (loop)/live/vmlinuz locale=es_MX.UTF-8 keyboard-layouts=latam boot=live union=overlay components noconfig=sudo username=user hostname=raizo user-fullname=Live-Raizo-User findiso=$isofile debug --verbose ip=frommedia vga=791 persistence\n")
                custom_file.write("\tinitrd (loop)/live/initrd.img\n")
                custom_file.write("}")
        print("\33[0;32mLive-Raizo added")


def main():
        if os.getuid() == 0:
                searchPartitionNumber()
                print("\n\33[0;34mChecking if \33[4;35m/boot-isos\33[0;34m folder exists")
                if(not os.path.exists("/boot-isos")):
                        print("\33[2;34mfolder not found, creating...")
                        os.system("sudo mkdir /boot-isos")
                        print("\t\33[6;33mfolder created")
                else:
                        print("\t\33[6;33mfolder found")
                while(True):
                        try:
                                decision = input("\n\33[0;34mDo you want to download \33[0;37mLive-Raizo.iso\33[0;34m? \33[1;34m(\33[1;32my\33[1;34m/\33[1;31mn\33[1;34m) \n" + 
                                "\33[0;37mNote: \33[0;34mIf you select \33[1;31mn\33[0;34m, you need to download manualy and set the file in \33[4;35m/boot-isos\33[0;34m with  \33[0;37mLive-Raizo.iso \33[0;34mname\n")
                        except KeyboardInterrupt:
                                sys.exit(2)
                        if(decision == "y"):
                                downloadISO("/boot-isos/Live-Raizo.iso")
                                break
                        elif(decision == "n"):
                                print("\t\33[6;31mDowload Skiped")
                                break
                        else:
                                print("\t\033[6;31mInvalid option, try again")
                addEntry("/etc/grub.d/40_custom")
                print("\n\33[0;31mGiving permissions...")
                os.system("sudo chmod 744 /etc/grub.d/40_custom")
                print("\t\33[6;32mpermissions added")
                grub_update = "sudo grub-mkconfig -o /boot/grub/grub.cfg"
                print("\n\33[0;31mStarting Grub-Update...\n\33[0;34m")
                os.system(grub_update)
                print("\t\33[6;32mGrub-Update finished")
                
        else:
                print ("\033[6;31myou need to run the script with sudo")
quit(main())