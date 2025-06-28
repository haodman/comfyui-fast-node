import os
import json
from PIL import Image
import torch
import numpy as np

NODE_CLASS_MAPPINGS = {}
NODE_DISPLAY_NAME_MAPPINGS = {}

class CustomNamingSaver:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "output_image": ("IMAGE",),
                "output_dir": ("STRING", {"default": "./custom_output"}),
                "start_index": ("STRING", {"default": "1", "multiline": False}),
            },
            "optional": {
                "input_image": ("IMAGE",),
                "canny_image": ("IMAGE",),
                "depth_image": ("IMAGE",),
                "openpose_image": ("IMAGE",),
                "prompt_text": ("STRING", {"multiline": True, "default": ""}),
                "negative_prompt": ("STRING", {"multiline": True, "default": ""}),
                "save_input": ("BOOLEAN", {"default": True}),
                "save_canny": ("BOOLEAN", {"default": False}),
                "save_depth": ("BOOLEAN", {"default": False}),
                "save_openpose": ("BOOLEAN", {"default": False}),
                "save_prompt": ("BOOLEAN", {"default": True}),
                "save_metadata": ("BOOLEAN", {"default": True}),
            }
        }

    RETURN_TYPES = ("IMAGE", "STRING")
    FUNCTION = "save_with_custom_naming"
    OUTPUT_NODE = True
    CATEGORY = "🐙FastNode/Saver"
    OUTPUT_IS_LIST = (False, False)
    OUTPUT_IS_OPTIONAL = (False, False)

    def save_with_custom_naming(
        self, output_image, output_dir, start_index="1",
        input_image=None, canny_image=None, depth_image=None, openpose_image=None,
        prompt_text="", negative_prompt="", save_input=True, save_canny=False,
        save_depth=False, save_openpose=False, save_prompt=True, save_metadata=True
    ):
        os.makedirs(output_dir, exist_ok=True)
        saved_files = []
        def to_list(img):
            if isinstance(img, torch.Tensor) and img.dim() == 4:
                return [img[i] for i in range(img.shape[0])]
            elif isinstance(img, list):
                return img
            elif img is not None:
                return [img]
            else:
                return []
        try:
            idx_start = int(str(start_index).lstrip("0") or "0")
        except Exception:
            idx_start = 1
        out_imgs = to_list(output_image)
        in_imgs = to_list(input_image)
        canny_imgs = to_list(canny_image)
        depth_imgs = to_list(depth_image)
        openpose_imgs = to_list(openpose_image)
        for i, img in enumerate(out_imgs):
            idx = idx_start + i
            base_name = f"{idx:05d}"
            output_path = os.path.join(output_dir, f"{base_name}_output.png")
            self._save_image_tensor(img, output_path)
            saved_files.append(f"{base_name}_output.png")
            pt = prompt_text
            nt = negative_prompt
            if isinstance(prompt_text, list):
                pt = prompt_text[i] if i < len(prompt_text) else ""
            if isinstance(negative_prompt, list):
                nt = negative_prompt[i] if i < len(negative_prompt) else ""
            if save_prompt and pt and isinstance(pt, str) and pt.strip():
                prompt_path = os.path.join(output_dir, f"{base_name}_prompt.txt")
                with open(prompt_path, "w", encoding="utf-8") as f:
                    f.write(pt.strip())
                saved_files.append(f"{base_name}_prompt.txt")
            if save_prompt and nt and isinstance(nt, str) and nt.strip():
                neg_prompt_path = os.path.join(output_dir, f"{base_name}_negative_prompt.txt")
                with open(neg_prompt_path, "w", encoding="utf-8") as f:
                    f.write(nt.strip())
                saved_files.append(f"{base_name}_negative_prompt.txt")
            if save_metadata:
                metadata = {
                    "base_name": base_name,
                    "saved_files": saved_files,
                    "prompt": pt.strip() if isinstance(pt, str) else "",
                    "negative_prompt": nt.strip() if isinstance(nt, str) else "",
                    "timestamp": self._get_timestamp()
                }
                metadata_path = os.path.join(output_dir, f"{base_name}_metadata.json")
                with open(metadata_path, "w", encoding="utf-8") as f:
                    json.dump(metadata, f, ensure_ascii=False, indent=2)
                saved_files.append(f"{base_name}_metadata.json")
        def save_type_imgs(imgs, suffix):
            for i, img in enumerate(imgs):
                idx = idx_start + i
                base_name = f"{idx:05d}"
                path = os.path.join(output_dir, f"{base_name}_{suffix}.png")
                self._save_image_tensor(img, path)
                saved_files.append(f"{base_name}_{suffix}.png")
        if save_input:
            save_type_imgs(in_imgs, "input")
        if save_canny:
            save_type_imgs(canny_imgs, "canny")
        if save_depth:
            save_type_imgs(depth_imgs, "depth")
        if save_openpose:
            save_type_imgs(openpose_imgs, "openpose")
        files_summary = ", ".join(saved_files) if saved_files else "No files saved"
        return (out_imgs[0] if out_imgs else None, files_summary)
    
    def _save_image_tensor(self, image_tensor, filepath):
        if not (isinstance(image_tensor, torch.Tensor) or isinstance(image_tensor, Image.Image)):
            raise TypeError(f"Input is not an image, got {type(image_tensor)}. Expected torch.Tensor or PIL.Image.Image")
        if isinstance(image_tensor, torch.Tensor):
            if image_tensor.dim() == 4:
                image_tensor = image_tensor[0]
            elif image_tensor.dim() == 3:
                pass
            else:
                raise ValueError(f"Unexpected tensor shape: {image_tensor.shape}")
            image_array = image_tensor.cpu().numpy()
            if image_array.max() <= 1.0:
                image_array = (image_array * 255).astype(np.uint8)
            else:
                image_array = image_array.astype(np.uint8)
            image = Image.fromarray(image_array)
        else:
            image = image_tensor
        if image.mode != 'RGB':
            image = image.convert('RGB')
        image.save(filepath, "PNG", optimize=True)
        print(f"已保存: {filepath}")
    def _get_timestamp(self):
        from datetime import datetime
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

class SeedToTextNode:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "seed": ("INT", {"default": 0, "min": -999999999, "max": 999999999}),
                "format": (["纯数字", "无前缀"], {"default": "纯数字"}),
                "padding": ("INT", {"default": 5, "min": 1, "max": 10}),
            }
        }
    RETURN_TYPES = ("STRING",)
    FUNCTION = "convert_seed_to_text"
    CATEGORY = "🐙FastNode/Type Conversion"
    OUTPUT_NODE = True
    def convert_seed_to_text(self, seed, format, padding):
        if format == "纯数字":
            result = str(seed).zfill(padding)
        elif format == "无前缀":
            result = str(seed)
        else:
            result = str(seed)
        return (result,)

class TextConcatenatorNode:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "separator": ("STRING", {"default": "_", "multiline": False}),
            },
            "optional": {
                "text1": ("STRING", {"default": "", "multiline": False}),
                "text2": ("STRING", {"default": "", "multiline": False}),
                "text3": ("STRING", {"default": "", "multiline": False}),
                "text4": ("STRING", {"default": "", "multiline": False}),
                "text5": ("STRING", {"default": "", "multiline": False}),
            }
        }
    RETURN_TYPES = ("STRING",)
    FUNCTION = "concatenate_texts"
    CATEGORY = "🐙FastNode/Text Processing"
    OUTPUT_NODE = True
    def concatenate_texts(self, separator, text1="", text2="", text3="", text4="", text5=""):
        texts = []
        for t in [text1, text2, text3, text4, text5]:
            if t is not None and str(t).strip() != "":
                texts.append(str(t))
        result = separator.join(texts)
        return (result,)

class LoadingImageListNode:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "folder_path": ("STRING", {"default": "./images", "multiline": False}),
            },
            "optional": {
                "start": ("INT", {"default": 0, "min": 0, "max": 9999}),
                "sort_by": (["name", "mtime"], {"default": "name"}),
                "reverse": ("BOOLEAN", {"default": False}),
                "max_count": ("INT", {"default": 0, "min": 0, "max": 9999}),
            }
        }
    RETURN_TYPES = ("IMAGE",)
    OUTPUT_IS_LIST = (True,)
    FUNCTION = "load_image_list"
    CATEGORY = "🐙FastNode/Loader"
    OUTPUT_NODE = True
    def load_image_list(self, folder_path, start=0, sort_by="name", reverse=False, max_count=0):
        exts = [".jpg", ".jpeg", ".png", ".bmp", ".webp"]
        files = [f for f in os.listdir(folder_path) if os.path.splitext(f)[1].lower() in exts]
        if sort_by == "name":
            files.sort(reverse=reverse)
        elif sort_by == "mtime":
            files.sort(key=lambda x: os.path.getmtime(os.path.join(folder_path, x)), reverse=reverse)
        if start > 0:
            files = files[start:]
        if max_count > 0:
            files = files[:max_count]
        images = []
        for fname in files:
            path = os.path.join(folder_path, fname)
            try:
                img = Image.open(path).convert("RGB")
                arr = np.array(img).astype(np.float32) / 255.0
                tensor = torch.from_numpy(arr)
                if tensor.ndim == 3:
                    tensor = tensor.unsqueeze(0)
                images.append(tensor)
            except Exception as e:
                print(f"加载图片失败: {path}，原因: {e}")
        return (images,)

class IntToFloatSimpleNode:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "value": ("INT", {"default": 0}),
            }
        }
    RETURN_TYPES = ("FLOAT",)
    FUNCTION = "int_to_float"
    CATEGORY = "🐙FastNode/Type Conversion"
    OUTPUT_NODE = True
    def int_to_float(self, value):
        return (float(value),)

class FloatToIntSimpleNode:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "value": ("FLOAT", {"default": 0.0}),
            }
        }
    RETURN_TYPES = ("INT",)
    FUNCTION = "float_to_int"
    CATEGORY = "🐙FastNode/Type Conversion"
    OUTPUT_NODE = True
    def float_to_int(self, value):
        return (int(round(value)),)

class IntToTextSimpleNode:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "value": ("INT", {"default": 0}),
            }
        }
    RETURN_TYPES = ("STRING",)
    FUNCTION = "int_to_text"
    CATEGORY = "🐙FastNode/Type Conversion"
    OUTPUT_NODE = True
    def int_to_text(self, value):
        return (str(value),)

class FloatToTextSimpleNode:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "value": ("FLOAT", {"default": 0.0}),
            },
            "optional": {
                "decimal_places": ("INT", {"default": 2, "min": 0, "max": 10}),
            }
        }
    RETURN_TYPES = ("STRING",)
    FUNCTION = "float_to_text"
    CATEGORY = "🐙FastNode/Type Conversion"
    OUTPUT_NODE = True
    def float_to_text(self, value, decimal_places=2):
        return (f"{value:.{decimal_places}f}",)

class ImageListRangeNode:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "folder_path": ("STRING", {"default": "./images"}),
                "start": ("INT", {"default": 0, "min": 0}),
                "end": ("INT", {"default": 0, "min": 0}),
                "sort_by": (["name", "mtime"], {"default": "name"}),
                "reverse": ("BOOLEAN", {"default": False}),
            }
        }
    RETURN_TYPES = ("IMAGE",)
    OUTPUT_IS_LIST = (True,)
    FUNCTION = "load_image_range"
    CATEGORY = "🐙FastNode/Loader"
    OUTPUT_NODE = True
    def load_image_range(self, folder_path, start=0, end=0, sort_by="name", reverse=False):
        exts = [".jpg", ".jpeg", ".png", ".bmp", ".webp"]
        files = [f for f in os.listdir(folder_path) if os.path.splitext(f)[1].lower() in exts]
        if sort_by == "name":
            files.sort(reverse=reverse)
        elif sort_by == "mtime":
            files.sort(key=lambda x: os.path.getmtime(os.path.join(folder_path, x)), reverse=reverse)
        total = len(files)
        if end <= 0 or end > total:
            end = total
        if start < 0:
            start = 0
        if start >= end:
            return ([],)
        files = files[start:end]
        images = []
        for fname in files:
            path = os.path.join(folder_path, fname)
            try:
                img = Image.open(path).convert("RGB")
                arr = np.array(img).astype(np.float32) / 255.0
                tensor = torch.from_numpy(arr)
                if tensor.ndim == 3:
                    tensor = tensor.unsqueeze(0)
                images.append(tensor)
            except Exception as e:
                print(f"加载图片失败: {path}，原因: {e}")
        return (images,)

class LoadingTextListNode:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "folder_path": ("STRING", {"default": "./texts", "multiline": False}),
            },
            "optional": {
                "start": ("INT", {"default": 0, "min": 0, "max": 9999}),
                "sort_by": (["name", "mtime"], {"default": "name"}),
                "reverse": ("BOOLEAN", {"default": False}),
                "max_count": ("INT", {"default": 0, "min": 0, "max": 9999}),
            }
        }
    RETURN_TYPES = ("STRING",)
    OUTPUT_IS_LIST = (True,)
    FUNCTION = "load_text_list"
    CATEGORY = "🐙FastNode/Loader"
    OUTPUT_NODE = True
    def load_text_list(self, folder_path, start=0, sort_by="name", reverse=False, max_count=0):
        exts = [".txt", ".json", ".csv"]
        files = [f for f in os.listdir(folder_path) if os.path.splitext(f)[1].lower() in exts]
        if sort_by == "name":
            files.sort(reverse=reverse)
        elif sort_by == "mtime":
            files.sort(key=lambda x: os.path.getmtime(os.path.join(folder_path, x)), reverse=reverse)
        if start > 0:
            files = files[start:]
        if max_count > 0:
            files = files[:max_count]
        texts = []
        for fname in files:
            path = os.path.join(folder_path, fname)
            try:
                with open(path, "r", encoding="utf-8") as f:
                    content = f.read()
                texts.append(content)
            except Exception as e:
                print(f"加载文本失败: {path}，原因: {e}")
        return (texts,)

NODE_CLASS_MAPPINGS["CustomNamingSaver"] = CustomNamingSaver
NODE_CLASS_MAPPINGS["SeedToTextNode"] = SeedToTextNode
NODE_CLASS_MAPPINGS["TextConcatenatorNode"] = TextConcatenatorNode
NODE_CLASS_MAPPINGS["LoadingImageListNode"] = LoadingImageListNode
NODE_CLASS_MAPPINGS["IntToFloatSimpleNode"] = IntToFloatSimpleNode
NODE_CLASS_MAPPINGS["FloatToIntSimpleNode"] = FloatToIntSimpleNode
NODE_CLASS_MAPPINGS["IntToTextSimpleNode"] = IntToTextSimpleNode
NODE_CLASS_MAPPINGS["FloatToTextSimpleNode"] = FloatToTextSimpleNode
NODE_CLASS_MAPPINGS["ImageListRangeNode"] = ImageListRangeNode
NODE_CLASS_MAPPINGS["LoadingTextListNode"] = LoadingTextListNode

NODE_DISPLAY_NAME_MAPPINGS["CustomNamingSaver"] = "📝 Custom Naming Saver"
NODE_DISPLAY_NAME_MAPPINGS["SeedToTextNode"] = "🎲 Seed To Text"
NODE_DISPLAY_NAME_MAPPINGS["TextConcatenatorNode"] = "🔗 Text Concatenator"
NODE_DISPLAY_NAME_MAPPINGS["LoadingImageListNode"] = "🖼️ Loading Image List"
NODE_DISPLAY_NAME_MAPPINGS["IntToFloatSimpleNode"] = "🔢 Int To Float (Simple)"
NODE_DISPLAY_NAME_MAPPINGS["FloatToIntSimpleNode"] = "🔢 Float To Int (Simple)"
NODE_DISPLAY_NAME_MAPPINGS["IntToTextSimpleNode"] = "🔤 Int To Text (Simple)"
NODE_DISPLAY_NAME_MAPPINGS["FloatToTextSimpleNode"] = "🔤 Float To Text (Simple)"
NODE_DISPLAY_NAME_MAPPINGS["ImageListRangeNode"] = "📐 Image List Range Node"
NODE_DISPLAY_NAME_MAPPINGS["LoadingTextListNode"] = "�� Loading Text List" 