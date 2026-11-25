import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import sync_vault


class PushVaultTests(unittest.TestCase):
    def test_refuses_to_sync_from_a_topic_branch(self):
        with tempfile.TemporaryDirectory() as folder:
            subprocess.run(["git", "init", "-q", "-b", "topic", folder], check=True)
            result = sync_vault.push_vault(Path(folder), "Record lesson")
            self.assertEqual(result, 1)


if __name__ == "__main__":
    unittest.main()
