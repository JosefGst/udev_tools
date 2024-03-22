import unittest
from udev_tools.get_udev import create_rule


class TestCreateRule(unittest.TestCase):
    def test_create_rule_without_kernel(self):
        data = ["ttyUSB0", "1234", "5678", "1-1.2"]
        arg_kernel = False
        arg_name = "motor"
        expected = 'KERNEL=="ttyUSB*", ATTRS{idVendor}=="1234", ATTRS{idProduct}=="5678", SYMLINK+="motor"'

        result = create_rule(data, arg_kernel, arg_name)

        self.assertEqual(result, expected)

    def test_create_rule_with_kernel(self):
        data = ["ttyUSB0", "1234", "5678", "1-1.2"]
        arg_kernel = True
        arg_name = "motor"
        expected = 'KERNEL=="ttyUSB*", ATTRS{idVendor}=="1234", ATTRS{idProduct}=="5678", KERNELS=="1-1.2", SYMLINK+="motor"'

        result = create_rule(data, arg_kernel, arg_name)

        self.assertEqual(result, expected)

    def test_create_rule_name_default(self):
        data = ["ttyACM0", "1234", "5678", "1-1.2"]
        arg_kernel = False
        arg_name = None
        expected = 'KERNEL=="ttyACM*", ATTRS{idVendor}=="1234", ATTRS{idProduct}=="5678", SYMLINK+="None"'

        result = create_rule(data, arg_kernel, arg_name)

        self.assertEqual(result, expected)


if __name__ == "__main__":
    unittest.main()
