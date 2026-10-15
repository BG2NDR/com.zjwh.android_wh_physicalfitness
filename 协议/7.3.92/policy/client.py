# -*- coding: utf-8 -*-
import os
import sys
from typing import Optional, Dict, Any, Union, List

cur_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(cur_dir)
for p in [cur_dir, parent_dir]:
    if p not in sys.path:
        sys.path.insert(0, p)

from core.client import BaseNetSecClient
from .config import (
    URL_RUN_POLICY,
    URL_INDOOR_POLICY,
    URL_GEO_FENCE,
    URL_SEMESTER_INFO,
    URL_SEMESTER_SUMMARY,
    URL_RUN_GOALS
)
from .models import RunRule, GeoFenceArea, SemesterInfo


class PolicyClient(BaseNetSecClient):
    """运动世界校园 7.3.92 跑步规则与地理围栏客户端"""

    def __init__(self,
                 uid: Optional[Union[int, str]] = None,
                 token: Optional[str] = None,
                 unid: Optional[Union[int, str]] = None,
                 device_config: Optional[Dict[str, Any]] = None):
        super().__init__(uid=uid, token=token, unid=unid, device_config=device_config)

    def get_run_policy(self, run_mode: int = 1, unid: Optional[Union[int, str]] = None) -> Optional[RunRule]:
        """获取指定运动模式的跑步规则（配速、步频、单次/单日里程、有效时段等）"""
        url = URL_INDOOR_POLICY if run_mode == 5 else URL_RUN_POLICY
        unid_val = int(unid or self.unid or 0)
        body = {
            "runMode": run_mode,
            "ruleUpdateTime": 0,
            "geoFenceUpdateTime": 0,
            "selectUnid": unid_val,
            "operateType": 0
        }
        res = self.execute_request("POST", url, body_plain=body)
        if isinstance(res, dict) and res.get("error") == 10000 and "data" in res and res["data"]:
            return RunRule.from_api_data(res["data"])
        return None

    def get_geo_fence(self, update_time: int = 0) -> List[GeoFenceArea]:
        """拉取学校电子围栏边界多边形与随机打卡点集"""
        body = {
            "geoFenceUpdateTime": update_time
        }
        res = self.execute_request("POST", URL_GEO_FENCE, body_plain=body)
        fences = []
        if isinstance(res, dict) and res.get("error") == 10000 and "data" in res and res["data"]:
            d = res["data"]
            raw_list = d.get("geoFences", []) or []
            for item in raw_list:
                fences.append(GeoFenceArea.from_api_data(item))
        return fences

    def get_semester_info(self, run_mode: int = 1) -> Optional[SemesterInfo]:
        """查询学生本学期已完成公里数与剩余目标"""
        body = {
            "runMode": run_mode
        }
        res = self.execute_request("POST", URL_SEMESTER_INFO, body_plain=body)
        if isinstance(res, dict) and res.get("error") == 10000 and "data" in res and res["data"]:
            return SemesterInfo.from_api_data(res["data"])
        return None

    def get_semester_summary(self, sid: int = 0) -> Dict[str, Any]:
        """查询学期总体结算汇总"""
        return self.execute_request("POST", URL_SEMESTER_SUMMARY, body_plain={"sid": sid})

    def get_run_goals(self) -> Dict[str, Any]:
        """查询本学期考核指标与目标"""
        return self.execute_request("POST", URL_RUN_GOALS, body_plain={})


    def get_distance_route_points(self, sport_type: int = 1, distance_m: int = 1000) -> dict:
        url = f"https://run.gxapp.iydsj.com/api/v560/get/{sport_type}/distance/{distance_m}"
        return self.execute_request("POST", url, body_plain={})

