"""Event Bridge v0.1 离线演示。无网络、无真实 Agent、无生产写入。"""
import hashlib
import json
from dataclasses import dataclass, field

WORKERS = {"content": "mock-muse", "code_review": "mock-codex"}
STATES = {"queued", "leased", "succeeded", "failed", "approval_required", "expired"}

@dataclass
class Bridge:
    seen: set = field(default_factory=set)
    tasks: dict = field(default_factory=dict)
    receipts: list = field(default_factory=list)
    side_effects: int = 0

    def submit(self, task_id, kind, revision, objective, *, approval_required=False):
        if kind not in WORKERS:
            raise ValueError("unavailable worker adapter")
        if not task_id or not objective or not revision:
            raise ValueError("missing task fields")
        key = (task_id, "submit", revision)
        if key in self.seen:
            return False
        if task_id in self.tasks:
            raise ValueError("task_id reused with different revision")
        self.seen.add(key)
        self.tasks[task_id] = dict(task_id=task_id, kind=kind, revision=revision,
                                   objective=objective, approval_required=approval_required,
                                   state="queued")
        return True

    def process(self, task_id, *, simulate_failure=False):
        task = self.tasks[task_id]
        if task["state"] != "queued":
            return None
        task["state"] = "leased"
        worker = WORKERS[task["kind"]]
        if simulate_failure:
            task["state"] = "failed"
            status, error = "failed", "SIMULATED_FAILURE"
        elif task["approval_required"]:
            task["state"] = "approval_required"
            status, error = "approval_required", "HUMAN_GATE"
        else:
            # 仅生成内存回执；不调用外部工具，不写文件
            self.side_effects += 1
            task["state"] = "succeeded"
            status, error = "succeeded", None
        fingerprint = hashlib.sha256(task["revision"].encode()).hexdigest()
        receipt = dict(task_id=task_id, worker=worker, status=status,
                       input_sha256=fingerprint, output_ref="memory://mock/"+task_id
                       if status == "succeeded" else None, error_code=error)
        self.receipts.append(receipt)
        return receipt

    def watchdog(self):
        return [dict(task_id=k, state=t["state"]) for k, t in self.tasks.items()
                if t["state"] in ("failed", "expired", "approval_required")]

if __name__ == "__main__":
    bridge = Bridge()
    bridge.submit("demo-001", "content", "rev-1", "生成脱敏内容任务包")
    bridge.submit("demo-002", "code_review", "commit-abc", "检查模拟 PR")
    print(json.dumps([bridge.process("demo-001"), bridge.process("demo-002")],
                     ensure_ascii=False, indent=2))
