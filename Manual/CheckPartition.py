import subprocess, shlex, re, sys

#search the partition number to use in the menu entry on 40_custom file
def main():
        print("\33[0;34mSearching where is mounted \33[4;35m/\33[0m")
        #search the path of the partition, for example: /dev/sda1
        out = subprocess.Popen(shlex.split("df /"), stdout=subprocess.PIPE).communicate()
        aux=re.search(r'(/[^\s]+)\s',str(out))
        #comprobe if the path was found and get the path
        if aux:
                path= aux.group(1) 
                letter = str(ord(path[7:8])- 97)
                number = path[8:]
        else:
                print ("cannot parse df") 
                sys.exit(2)
        #print the results
        print ("\t\33[4;35m/\33[0;34m mounted at \33[4;35m%s\33[0;34m - \33[5;93m(hd%s,%s)" % (path,letter,number))
quit(main())