# UDEV Tools

Helps to make udev rules.

## Install 
### With pip
    pip3 install udev_tools git+https://github.com/JosefGst/udev_tools

### From source
    git clone git@github.com:JosefGst/udev_tools.git
    cd udev_tools
    pip3 install .

## Usage

From inside the repository main directory run

    get_udev

The program will stop and wait for you to plugin the usb device. After the device got plugged in it automatically recognize it and displays the udev rules. To write to a file use the -o --output flag followd with the path to the file. The rule will be appended to it.

    get_udev -o my.rules

By default the device will be called "ttyDevice". To change it use:

    get_udev new_gadget

You should have a rules.rules file which can be copied to **/etc/udev/rules.d/** directory

## Activate the new rules 

    sudo udevadm control --reload-rules && sudo service udev restart && sudo udevadm trigger

# TODO

- [ ] check if directory exists, otherwise create
- [ ] add unit tests