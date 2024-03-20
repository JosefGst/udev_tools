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
                return (udev_info, vendor_id, product_id, kernel_info)
    return None


def write_to_file(line, file_path):
    file = open(file_path, "a")
    file.write(line + "\n")


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
        "-o", "--output", type=str, help='Outputs to the specified file path eg."my.rules".'
    )
    parser.add_argument("-v", "--version", action="version", version="%(prog)s 0.1.0")

    args = parser.parse_args()

    data = detect_tty_usb_devices()
    line = 'KERNEL=="{}*", ATTRS{{idVendor}}=="{}", ATTRS{{idProduct}}=="{}", KERNELS=="{}", SYMLINK+="{}"'.format(
        data[0].rstrip(data[0][-1]), data[1], data[2], data[3], args.name
    )
    print(line)

    if args.output:
        write_to_file(line, args.output)
        print("File has been written to {}".format(args.output))


if __name__ == "__main__":
    main()
