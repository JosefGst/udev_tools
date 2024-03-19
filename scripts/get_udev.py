# ls.py v1

import argparse
import pyudev


def detect_tty_usb_devices():
    context = pyudev.Context()
    monitor = pyudev.Monitor.from_netlink(context)

    print("Please plugin your USB device...")


    for device in iter(monitor.poll, None):
        if device.subsystem == 'tty' and ('usb' in device.get('ID_BUS', '') or 'acm' in device.get('ID_BUS', '')):
            if device.action == 'add':
                udev_info = device.device_node.split('/')[-1]
                kernel_info = device.parent.parent.parent.device_path.split('/')[-1]

                vendor_id = device.get('ID_VENDOR_ID', '')
                product_id = device.get('ID_MODEL_ID', '')

                print(f"Found device: {udev_info} {kernel_info} {vendor_id}:{product_id}")

                return (udev_info, kernel_info, vendor_id, product_id)

    return None

def write_to_file(data):
    with open('.99-tkoh.rules.tmp', 'w') as file:
        for symlink, info in data.items():
            line = 'KERNEL=="ttyUSB*", ATTRS{{idVendor}}=="{}", ATTRS{{idProduct}}=="{}", KERNELS=="{}", SYMLINK+="{}"\n'.format(
                info['id_vendor'], info['id_product'], info['kernel'], symlink
            )
            file.write(line)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-n',"--name",default="ttyDevice", help='Give a name to your usb device. eg. \"motor\". Default is \"ttyDevice\".')
    parser.add_argument('-f',"--file",default="rule.rules", help='Path to the \".rules\" file.')
    args = parser.parse_args()
    print(args.name)

    print(detect_tty_usb_devices())


if __name__ == "__main__":
    main()
    

    