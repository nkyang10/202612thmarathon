#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Generate itinerary '曼谷食買玩' gallery images via remote z_image_turbo.
txt2img for experiences; img2img for the Grand Palace (regenerate official ref)."""
import os, sys, time, random, json, uuid, urllib.request, urllib.parse, io
from PIL import Image

SERVER = "http://192.168.1.162:8000"
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(os.path.dirname(HERE), "assets", "bkk_gallery")
os.makedirs(OUT, exist_ok=True)
REF = os.path.join(os.path.dirname(HERE), "assets", "bkk_ref", "bkk_10.jpg")

def post_json(url, body):
    req = urllib.request.Request(url, data=json.dumps(body).encode(),
                                 headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=60) as r:
        return json.loads(r.read().decode())
def get_json(url):
    req = urllib.request.Request(url, headers={"Accept": "application/json"})
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.loads(r.read().decode())
def upload_image(path, name="ref.png"):
    im = Image.open(path).convert("RGB")
    im = im.resize((1024, 1024), Image.LANCZOS)
    buf = io.BytesIO(); im.save(buf, "PNG"); data = buf.getvalue()
    b = "----ref" + os.urandom(8).hex()
    body = b""
    body += (f"--{b}\r\nContent-Disposition: form-data; name=\"image\"; filename=\"{name}\"\r\nContent-Type: image/png\r\n\r\n").encode() + data + b"\r\n"
    body += f"--{b}--\r\n".encode()
    req = urllib.request.Request(SERVER + "/upload/image", data=body,
        headers={"Content-Type": f"multipart/form-data; boundary={b}"})
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.loads(r.read().decode())["name"]

def graph_txt(prompt, seed):
    return {
      "1":{"class_type":"UNETLoader","inputs":{"unet_name":"z_image_turbo_bf16.safetensors","weight_dtype":"default"}},
      "2":{"class_type":"CLIPLoader","inputs":{"clip_name":"qwen_3_4b.safetensors","type":"lumina2","device":"default"}},
      "3":{"class_type":"VAELoader","inputs":{"vae_name":"ae.safetensors"}},
      "4":{"class_type":"CLIPTextEncode","inputs":{"text":prompt,"clip":["2",0]}},
      "5":{"class_type":"ConditioningZeroOut","inputs":{"conditioning":["4",0]}},
      "6":{"class_type":"EmptySD3LatentImage","inputs":{"width":1024,"height":1024,"batch_size":1}},
      "7":{"class_type":"ModelSamplingAuraFlow","inputs":{"shift":3,"model":["1",0]}},
      "8":{"class_type":"KSampler","inputs":{"seed":seed,"steps":8,"cfg":1.0,"sampler_name":"res_multistep","scheduler":"simple","denoise":1.0,"model":["7",0],"positive":["4",0],"negative":["5",0],"latent_image":["6",0]}},
      "9":{"class_type":"VAEDecode","inputs":{"samples":["8",0],"vae":["3",0]}},
     "10":{"class_type":"SaveImage","inputs":{"images":["9",0],"filename_prefix":"bkk_gallery"}},
    }

def graph_img2img(prompt, img_name, seed, denoise=0.55):
    return {
      "1":{"class_type":"UNETLoader","inputs":{"unet_name":"z_image_turbo_bf16.safetensors","weight_dtype":"default"}},
      "2":{"class_type":"CLIPLoader","inputs":{"clip_name":"qwen_3_4b.safetensors","type":"lumina2","device":"default"}},
      "3":{"class_type":"VAELoader","inputs":{"vae_name":"ae.safetensors"}},
      "4":{"class_type":"CLIPTextEncode","inputs":{"text":prompt,"clip":["2",0]}},
      "5":{"class_type":"ConditioningZeroOut","inputs":{"conditioning":["4",0]}},
     "20":{"class_type":"LoadImage","inputs":{"image":img_name}},
     "21":{"class_type":"VAEEncode","inputs":{"pixels":["20",0],"vae":["3",0]}},
      "7":{"class_type":"ModelSamplingAuraFlow","inputs":{"shift":3,"model":["1",0]}},
      "8":{"class_type":"KSampler","inputs":{"seed":seed,"steps":8,"cfg":1.0,"sampler_name":"res_multistep","scheduler":"simple","denoise":denoise,"model":["7",0],"positive":["4",0],"negative":["5",0],"latent_image":["21",0]}},
      "9":{"class_type":"VAEDecode","inputs":{"samples":["8",0],"vae":["3",0]}},
     "10":{"class_type":"SaveImage","inputs":{"images":["9",0],"filename_prefix":"bkk_gallery"}},
    }

def render_one(name, graph):
    pid = post_json(f"{SERVER}/prompt", {"prompt": graph, "client_id": uuid.uuid4().hex})["prompt_id"]
    while True:
        time.sleep(1)
        try:
            hist = get_json(f"{SERVER}/history/{pid}")
        except Exception:
            continue
        if pid in hist:
            node = hist[pid]["outputs"].get("10", {})
            if node.get("images"):
                fn = node["images"][0]["filename"]; sub = node["images"][0].get("subfolder","")
                url = f"{SERVER}/view?filename={urllib.parse.quote(fn)}&subfolder={urllib.parse.quote(sub)}&type=output"
                dest = os.path.join(OUT, name)
                urllib.request.urlretrieve(url, dest)
                print(f"{name} done", flush=True)
                return dest
            if hist[pid].get("status", {}).get("status_str") == "error":
                print(f"{name} ERROR:", json.dumps(hist[pid]["status"])[:500], flush=True)
                return None

# --- txt2img experiences ---
EXPS = {
 "food.png": "Vibrant spread of authentic Thai food on a table, tom yum goong hot and sour soup, pad thai noodles, green curry, fresh mango, warm inviting natural light, photorealistic food photography, appetizing, Bangkok restaurant, 1024x1024",
 "sticky_rice.png": "Close-up of Thai mango sticky rice dessert, sweet glutinous rice with slices of ripe golden mango and coconut cream drizzle, on a banana leaf, warm soft light, photorealistic food photography, delicious, 1024x1024",
 "night_market.png": "Lively Bangkok night market street at dusk, colorful food stalls with hanging lanterns, street food grills, crowds browsing, warm glow, photorealistic travel photography, vibrant, 1024x1024",
 "wat_arun.png": "Majestic Wat Arun temple of dawn in Bangkok at golden sunset, ornate Khmer-style prang tower silhouetted against warm orange-pink sky, reflection on the Chao Phraya river, photorealistic travel photography, 1024x1024",
 "river_cruise.png": "Scenic Chao Phraya river in Bangkok at golden hour, a long-tail boat cruising, Grand Palace and temple spires along the riverbank, warm golden light, photorealistic travel photography, 1024x1024",
 "massage.png": "Serene Thai massage spa interior, a guest relaxing on a mattress with a traditional Thai massage being given, warm wooden interior, orchid flowers, soft ambient light, photorealistic, 1024x1024",
 "shopping.png": "Colorful Chatuchak weekend market in Bangkok, stalls packed with handicrafts, ceramics and souvenirs, shoppers browsing, market umbrellas, bright daylight, photorealistic travel photography, 1024x1024",
}
# --- img2img: regenerate official Grand Palace ref ---
ref_name = None
try:
    ref_name = upload_image(REF, "grandpalace_ref.png")
except Exception as e:
    print("upload ref warn:", e)

for name, prompt in EXPS.items():
    render_one(name, graph_txt(prompt, random.randint(1,2**31)))

if ref_name:
    gp = "The golden spires and ornate roofs of the Grand Palace of Bangkok, majestic Thai temple architecture, warm golden light, clear blue sky, photorealistic, 1024x1024"
    render_one("grand_palace.png", graph_img2img(gp, ref_name, random.randint(1,2**31), denoise=0.6))

try: post_json(f"{SERVER}/free", {"unload_models": True, "free_memory": True})
except Exception as e: print("free warn:", e)
print("ALL BKK GALLERY IMAGES DONE")
