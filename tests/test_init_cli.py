import unittest
from udev_tools.get_udev import init_cli


class TestInitCli(unittest.TestCase):

    def test_default_name(self):
        args = init_cli("")
        self.assertEqual(args.name, "ttyDevice")

    def test_custom_name(self):
        args = init_cli(["motor"])
        self.assertEqual(args.name, "motor")

    def test_output_file(self):
        args = init_cli(["-o", "rules.txt"])
        self.assertEqual(args.output, "rules.txt")

        args = init_cli(["--output", "my.rules"])
        self.assertEqual(args.output, "my.rules")

    def test_kernels_flag(self):
        args = init_cli(["-k"])
        self.assertTrue(args.kernels)

        args = init_cli(["--kernels"])
        self.assertTrue(args.kernels)

    def test_help_flag(self):
        with self.assertRaises(SystemExit):
            init_cli(["-h"])


if __name__ == "__main__":
    unittest.main()
