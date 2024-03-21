# UDEV Tools

Create udev rules with a simple command line.

## Install 
<!-- ### With pip
    pip3 install udev_tools git+https://github.com/JosefGst/udev_tools -->

### From source
    git clone https://github.com/JosefGst/udev_tools.git
    cd udev_tools
    pip3 install .

## Usage
### Minimal example

    get_udev

The program will stop and wait for you to plugin the usb device. After the device got plugged in it automatically recognize it and displays the udev rules. 

---
By default the device will be called "ttyDevice". To change it use:

    get_udev new_gadget

To inlcude the KERNELS information sot he rule applies only on the specified prot run:

    get_udev -k

To write to a file use the --output flag followed with the path to the file. The rule will be appended to it.

    get_udev -o my.rules

### Full example:

    get_udev my_gadget -k -o my.rules

You should have a rules.rules file which can be copied to **/etc/udev/rules.d/** directory

## Activate the new rules 

    sudo udevadm control --reload-rules && sudo service udev restart && sudo udevadm trigger

## Run Tests

    python3 -m nose2 -v

# TODO

- [ ] add unit tests
- [ ] save output directly in /etc/udev/rules.d/ directory (is sudo permitted)
- [ ] pip3 install udev_tools git+https://github.com/JosefGst/udev_tools not working
- [ ] github actions
- [ ] (optional) check if directory exists, otherwise create