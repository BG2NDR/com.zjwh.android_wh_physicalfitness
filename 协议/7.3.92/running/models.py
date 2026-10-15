# -*- coding: utf-8 -*-
from dataclasses import dataclass, field
from typing import Optional, Dict, Any, List


@dataclass
class GpsPoint:
    """单个 GPS 运动轨迹采样点"""
    lat: float
    lon: float
    time: int
    speed: float = 2.5
    accuracy: float = 3.0
    isValid: bool = True

    def to_dict(self) -> dict:
        return {
            "lat": self.lat,
            "lon": self.lon,
            "time": self.time,
            "speed": self.speed,
            "accuracy": self.accuracy,
            "isValid": self.isValid
        }


@dataclass
class FivePoint:
    """必经打卡目标点"""
    lat: float
    lon: float
    isFixed: int = 1
    isPass: bool = True
    pointName: str = ""
    position: int = 0

    def to_dict(self) -> dict:
        return {
            "lat": self.lat,
            "lon": self.lon,
            "isFixed": self.isFixed,
            "isPass": self.isPass,
            "pointName": self.pointName,
            "position": self.position
        }


@dataclass
class StepBucket:
    """10秒步频分桶统计"""
    stepsNum: int
    beginTime: int
    endTime: int
    flag: int = 0
    maxDiff: float = 0.0
    minDiff: float = 0.0
    avgDiff: float = 0.0
    state: int = 0
    queueNum: int = 1

    def to_dict(self) -> dict:
        return {
            "stepsNum": self.stepsNum,
            "beginTime": self.beginTime,
            "endTime": self.endTime,
            "flag": self.flag,
            "maxDiff": self.maxDiff,
            "minDiff": self.minDiff,
            "avgDiff": self.avgDiff,
            "state": self.state,
            "queueNum": self.queueNum
        }


@dataclass
class SpeedBucket:
    """10秒速度分桶统计"""
    distance: float
    beginTime: int
    endTime: int
    flag: int = 0
    state: int = 0
    queueNum: int = 1

    def to_dict(self) -> dict:
        return {
            "distance": self.distance,
            "beginTime": self.beginTime,
            "endTime": self.endTime,
            "flag": self.flag,
            "state": self.state,
            "queueNum": self.queueNum
        }


@dataclass
class RunningSubmissionResult:
    """跑步提交结果模型"""
    success: bool
    rrid: Optional[int] = None
    error_code: int = -1
    message: str = ""
    total_distance: float = 0.0
    total_time: int = 0
    is_valid: bool = False
    raw: Dict[str, Any] = field(default_factory=dict)
