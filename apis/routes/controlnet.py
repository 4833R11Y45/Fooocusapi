# apis/routes/controlnet.py
from fastapi import APIRouter, Depends
from ..models.controlnet import ControlNetRequest
from ..models.requests import CommonRequest
from ..utils.api_utils import api_key_auth
from ..utils.call_worker import async_worker

router = APIRouter(dependencies=[Depends(api_key_auth)])

DEFAULT_PARAMS = {
    "prompt": "",
    "negative_prompt": "",
    "image_number": 1,
    "image_seed": 0,
    "style_selections": ["Fooocus V2", "Fooocus Sharp", "Fooocus Enhance"],
    "performance_selection": "Quality",
    "aspect_ratios_selection": "704*1344",
    "output_format": "png",
    "save_metadata_to_images": True,
    "metadata_scheme": "fooocus",
    "base_model_name": "juggernautXL_v8Rundiffusion.safetensors",
    "refiner_model_name": "juggernautXL_v8Rundiffusion.safetensors",
    "refiner_switch": 0.5,
    "vae_name": "Default (model)",
    "sharpness": 2.0,
    "guidance_scale": 4.0,
    "adaptive_cfg": 7.0,
    "clip_skip": 2,
    "sampler_name": "dpmpp_2m_sde_gpu",
    "scheduler_name": "karras",
    "adm_scaler_positive": 1.5,
    "adm_scaler_negative": 0.8,
    "adm_scaler_end": 0.3,
    "freeu_enabled": False,
    "freeu_b1": 1.01,
    "freeu_b2": 1.02,
    "freeu_s1": 0.99,
    "freeu_s2": 0.95,
    "stream_output": False,
    "async_process": False,
    "webhook_url": "",
    "preset": "initial",
    "black_out_nsfw": True
}

@router.post("/v1/controlnet/generate")
async def generate_controlnet(request: ControlNetRequest):
    """Generate images using ControlNet"""
    # Create common request with default parameters
    common_request = CommonRequest(**DEFAULT_PARAMS)
    
    # Set ControlNet parameters
    common_request.controlnet_image = request.control_inputs
    
    # Process the request
    return await async_worker(request=common_request, wait_for_result=True)