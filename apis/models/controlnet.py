# apis/models/controlnet.py
from pydantic import BaseModel, Field, validator
from typing import List
from enum import Enum
from .base import ControlNetType, ImagePrompt

class ControlNetInput(ImagePrompt):
    """ControlNet input parameters"""
    cn_img: str = Field(..., description="ControlNet image path/string")
    cn_stop: float = Field(default=0.6, ge=0, le=1, description="ControlNet stop")
    cn_weight: float = Field(default=0.5, ge=0, le=2, description="ControlNet weight")
    cn_type: ControlNetType = Field(default=ControlNetType.cn_ip, description="ControlNet type")

class ControlNetRequest(BaseModel):
    """Request model for ControlNet processing"""
    control_inputs: List[ControlNetInput] = Field(..., max_items=4, min_items=1)

    @validator('control_inputs')
    def validate_inputs(cls, v):
        if not 1 <= len(v) <= 4:
            raise ValueError("Must provide 1-4 control images")
        return v