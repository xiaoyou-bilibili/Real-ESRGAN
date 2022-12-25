import cv2
from basicsr.archs.rrdbnet_arch import RRDBNet

from realesrgan import RealESRGANer
from gfpgan import GFPGANer
import numpy as np

# restorer
upsampler = RealESRGANer(
    scale=4,
    model_path="weights/RealESRGAN_x4plus_anime_6B.pth",
    dni_weight=None,
    model=RRDBNet(num_in_ch=3, num_out_ch=3, num_feat=64, num_block=6, num_grow_ch=32, scale=4),
    tile=0,
    tile_pad=10,
    pre_pad=0,
    half=True,
    gpu_id=0)

face_enhancer = GFPGANer(
    model_path='weights/GFPGANv1.3.pth',
    upscale=4,
    arch='clean',
    channel_multiplier=2,
    bg_upsampler=upsampler)


def convert_img(path: str, origin: str, face_enhance_open):
    img = cv2.imread("{}/{}".format(path, origin), cv2.IMREAD_UNCHANGED)
    try:
        if face_enhance_open:
            _, _, output = face_enhancer.enhance(img, has_aligned=False, only_center_face=False, paste_back=True)
        else:
            output, _ = upsampler.enhance(img, outscale=4)
    except RuntimeError as error:
        print('Error', error)
        print('If you encounter CUDA out of memory, try to set --tile with a smaller number.')
    else:
        cv2.imwrite("{}/scale_res.jpg".format(path), output)


def convert_img_row(data: bytes, face_enhance_open:bool):
    img = cv2.imdecode(np.fromstring(data, np.uint8), cv2.IMREAD_UNCHANGED)
    try:
        if face_enhance_open:
            _, _, output = face_enhancer.enhance(img, has_aligned=False, only_center_face=False, paste_back=True)
        else:
            output, _ = upsampler.enhance(img, outscale=4)
    except RuntimeError as error:
        print('Error', error)
        print('If you encounter CUDA out of memory, try to set --tile with a smaller number.')
    else:
        return cv2.imencode('.jpg', output)[1].tobytes()
