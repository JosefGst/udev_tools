# ls.py v1

import argparse
import pyudev
import signal
import sys


def detect_tty_usb_devices():
    context = pyudev.Context()
    monitor = pyudev.Monitor.from_netlink(context)
    print("Please plugin the USB device...")

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


def ctrlc_handler(signum, frame):
    res = input("Ctrl-c was pressed. Do you really want to exit? Y/n ")
    if (res == "y") or (res == "Y") or (res == ""):
        exit(1)


def create_rule(data, arg_kernel, arg_name):
    if arg_kernel:
        line = 'KERNEL=="{}*", ATTRS{{idVendor}}=="{}", ATTRS{{idProduct}}=="{}", KERNELS=="{}", SYMLINK+="{}"'.format(
            data[0].rstrip(data[0][-1]), data[1], data[2], data[3], arg_name
        )
    else:
        line = 'KERNEL=="{}*", ATTRS{{idVendor}}=="{}", ATTRS{{idProduct}}=="{}", SYMLINK+="{}"'.format(
            data[0].rstrip(data[0][-1]), data[1], data[2], arg_name
        )
    print(line)
    return line


def init_cli(args):
    parser = argparse.ArgumentParser(
        prog="get_udev",
        description="Run the command and plugin the USB device to create the udev rules.",
    )
    parser.add_argument(
        "name",
        nargs="?",
        default="ttyDevice",
        help='Name the usb device. eg. "motor". Default is "ttyDevice".',
    )
    parser.add_argument(
        "-o",
        "--output",
        type=str,
        help='Outputs to the specified file path eg."my.rules".',
    )
    parser.add_argument(
        "-k",
        "--kernels",
        action="store_true",
        help="Include the KERNELS information, so the rule applies only on the specified port.",
    )
    parser.add_argument("-v", "--version", action="version", version="%(prog)s 0.1.0")

    return parser.parse_args(args)


def main():
    signal.signal(signal.SIGINT, ctrlc_handler)
    args = init_cli(sys.argv[1:])

    data = detect_tty_usb_devices()
    line = create_rule(data, args.kernels, args.name)

    if args.output:
        write_to_file(line, args.output)
        print("File has been written to {}".format(args.output))


if __name__ == "__main__":
    main()
