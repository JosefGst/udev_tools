# ls.py v1

import argparse
import pyudev
import signal


def detect_tty_usb_devices():
    context = pyudev.Context()
    monitor = pyudev.Monitor.from_netlink(context)
    print("Please plugin your USB device...")

    for device in iter(monitor.poll, None):
        if device.subsystem == "tty" and (
            "usb" in device.get("ID_BUS", "") or "acm" in device.get("ID_BUS", "")
        ):
            if device.action == "add":
                udev_info = device.device_node.split("/")[-1]
                kernel_info = device.parent.parent.parent.device_path.split("/")[-1]
                vendor_id = device.get("ID_VENDOR_ID", "")
                product_id = device.get("ID_MODEL_ID", "")
                # print(f"Found device: {udev_info} {kernel_info} {vendor_id}:{product_id}")
                return (udev_info, kernel_info, vendor_id, product_id)
    return None


def write_to_file(data, file_path, device_name):
    file = open(file_path, "a")
    line = 'KERNEL=="{}*", ATTRS{{idVendor}}=="{}", ATTRS{{idProduct}}=="{}", KERNELS=="{}", SYMLINK+="{}"\n'.format(
        data[0].rstrip(data[0][-1]), data[1], data[2], data[3], device_name
    )
    file.write(line)


def handler(signum, frame):
    res = input("Ctrl-c was pressed. Do you really want to exit? Y/n ")
    if (res == "y") or (res == "Y") or (res == ""):
        exit(1)


def main():
    signal.signal(signal.SIGINT, handler)
    parser = argparse.ArgumentParser(
        prog="get_udev",
        description="Run the command and plugin the USB device to create the udev rules.",
    )
    parser.add_argument(
        "name",
        nargs="?",
        default="ttyDevice",
        help='Give a name to your usb device. eg. "motor". Default is "ttyDevice".',
    )
    parser.add_argument(
        "-f", "--file", default="rule.rules", help='Path to the "rule.rules" file.'
    )
    parser.add_argument("-v", "--version", action="version", version="%(prog)s 0.0.1")

    args = parser.parse_args()
    data = detect_tty_usb_devices()
    write_to_file(data, args.file, args.name)
    print("File has been written to {}".format(args.file))


if __name__ == "__main__":
    main()
