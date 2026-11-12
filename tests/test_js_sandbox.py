import unittest

# we should modify the subprocess imported from cwltool.sandboxjs
from cwltool.sandboxjs import (check_js_threshold_version,
                               minimum_node_version_str, subprocess, new_js_proc)
from mock import Mock, patch


class Javascript_Sanity_Checks(unittest.TestCase):

    def setUp(self):
        self.check_output = subprocess.check_output 

    def tearDown(self):
        subprocess.check_output = self.check_output

    def test_node_version(self):
        subprocess.check_output = Mock(return_value=b'v22.23.4\n')
        self.assertEqual(check_js_threshold_version('node'), False)

        subprocess.check_output = Mock(return_value=b'v26.13.0\n')
        self.assertEqual(check_js_threshold_version('node'), False)

        subprocess.check_output = Mock(return_value=b'v26.13.1\n')
        self.assertEqual(check_js_threshold_version('node'), True)

        subprocess.check_output = Mock(return_value=b'v26.14.0\n')
        self.assertEqual(check_js_threshold_version('node'), True)

        subprocess.check_output = Mock(return_value=b'v27.0.0\n')
        self.assertEqual(check_js_threshold_version('node'), True)

    def test_uses_safe_node_after_older_nodejs(self):
        # 古い別名を飛ばし、安全な Node.js を起動する。
        def output(args):
            if args[-1] == '-v':
                return b'v24.22.3\n' if args[0] == 'nodejs' else b'v26.13.1\n'
            return 't'
        with patch.object(subprocess, 'check_output', side_effect=output):
            with patch.object(subprocess, 'Popen') as popen:
                self.assertIs(new_js_proc(), popen.return_value)
                self.assertEqual(popen.call_count, 1)
                self.assertEqual(popen.call_args[0][0][0], 'node')

    def test_is_javascript_installed(self):
            pass
