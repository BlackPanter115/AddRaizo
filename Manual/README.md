# Adding Live Raizo Manually
To add Live Raizo you need to follow the next steps

* Check the partition number where is mounted /
* Download the last version of Live Raizo iso
* Create the /boot-isos directory
* Add the menu Entry
* Update Grub

## Check the partition number where is mounted /
To know where is mounted / you can use [GParted](https://gparted.org/) or another method that you want, alternatively you can use the script named CheckPartition.py

**NOTE:** If you use GParted or another method, consider this:
```
/dev/sdxy where:

* x it's the letter of the HDD
* y it's the partition number
The letter is a reference to HDD number (a = 0, b = 1, etc)

For example: if / is mounted in /dev/sda1, you have / mount in the HDD0 in the partition number 1
```
