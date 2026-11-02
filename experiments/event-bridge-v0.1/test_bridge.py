"""运行：python -m unittest discover -s experiments/event-bridge-v0.1 -p 'test_*.py'"""
import hashlib
import unittest
from bridge import Bridge

class BridgeTests(unittest.TestCase):
    def test_t1_content_and_duplicate(self):
        b = Bridge()
        self.assertTrue(b.submit("t1", "content", "r1", "写出草稿"))
        self.assertFalse(b.submit("t1", "content", "r1", "写出草稿"))
        a = b.process("t1")
        self.assertEqual(a["worker"], "mock-muse")
        self.assertEqual(a["status"], "succeeded")
        self.assertIsNone(b.process("t1"))
        self.assertEqual(b.side_effects, 1)

    def test_t2_review_sha(self):
        b = Bridge()
        b.submit("t2", "code_review", "commit-abc", "代码审核")
        a = b.process("t2")
        self.assertEqual(a["worker"], "mock-codex")
        self.assertEqual(a["input_sha256"], hashlib.sha256(b"commit-abc").hexdigest())

    def test_t3_failure_gate_and_unavailable(self):
        b = Bridge()
        b.submit("f", "content", "v1", "模拟失败")
        b.submit("g", "content", "v1", "需要审批", approval_required=True)
        self.assertEqual(b.process("f", simulate_failure=True)["status"], "failed")
        self.assertEqual(b.process("g")["status"], "approval_required")
        self.assertEqual(b.side_effects, 0)
        self.assertEqual(len(b.watchdog()), 2)
        self.assertIsNone(b.process("f"))
        with self.assertRaises(ValueError):
            b.submit("z", "unavailable", "v1", "不能调用的外部平台")
        with self.assertRaises(ValueError):
            b.submit("f", "content", "v2", "换版本重跑")

if __name__ == "__main__":
    unittest.main()
