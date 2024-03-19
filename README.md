# UDEV Tools

Helps to make udev rules.

## Usage

From inside the repository main directory run

    python udev_tools/get_udev.py

The program will stop and wait for you to plugin the usb device. After the device got plugged in it automatically recognize it and create a rules.rules file.
Change the destination file with:

    python udev_tools/get_udev.py -f my.rules

By default the device will be called "ttyDevice". To change it use:

    python udev_tools/get_udev.py new_gadget

You should have a rules.rules file which can be copied to **/etc/udev/rules.d/** directory

## Activate the new rules 

    sudo udevadm control --reload-rules && sudo service udev restart && sudo udevadm trigger

# TODO

- [ ] 