# -*- coding: utf-8 -*-
import json
import os
import subprocess
from typing import Optional

try:
    from .config import LOGIN_CAPTCHA_ID
    from .models import GeetestResult
except (ImportError, ValueError):
    from config import LOGIN_CAPTCHA_ID
    from models import GeetestResult


class GeetestV4Solver:
    """极验 4 代滑块求解封装器"""

    def __init__(self,
                 node_executable: str = r"D:/Program Files/nodejs/node.exe",
                 solver_script: Optional[str] = None):
        self.node_executable = node_executable
        if solver_script is None:
            cur_dir = os.path.dirname(os.path.abspath(__file__))
            solver_script = os.path.join(cur_dir, "geetest_solver.js")
        self.solver_script = solver_script

    def solve(self, captcha_id: str = LOGIN_CAPTCHA_ID, timeout_sec: int = 60) -> GeetestResult:
        """调用无头 Chromium 求解极验滑块并解析结果"""
        if not os.path.isfile(self.solver_script):
            raise FileNotFoundError(f"极验求解脚本不存在: {self.solver_script}")

        cmd = [self.node_executable, self.solver_script, captcha_id]
        proc = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            errors="replace",
            timeout=timeout_sec
        )

        for line in proc.stdout.splitlines():
            if line.startswith("FINAL_RESULT:"):
                raw_json = line[len("FINAL_RESULT:"):].strip()
                res = json.loads(raw_json)
                return GeetestResult(
                    captcha_id=res.get("captcha_id", captcha_id),
                    lot_number=res.get("lot_number", ""),
                    pass_token=res.get("pass_token", ""),
                    gen_time=res.get("gen_time", ""),
                    captcha_output=res.get("captcha_output", "")
                )

        raise RuntimeError(f"极验滑块识别失败 (退出码 {proc.returncode}):\nSTDOUT: {proc.stdout}\nSTDERR: {proc.stderr}")

