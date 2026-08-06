#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Generate 9 ATMBKK 2026 CM scene images via remote z_image_turbo (ComfyUI @192.168.1.162:8000)."""
import os, sys, json, time, random, urllib.request, urllib.parse, uuid

SERVER = "http://192.168.1.162:8000"
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "scenes_frames")
os.makedirs(OUT, exist_ok=True)

# scene prompts (z_image_turbo line of each scene)
SCENES = {
 1:"Warm cinematic shot of a happy family (parents and young child) at dawn in Bangkok, city skyline glowing golden behind them, they are stretching and smiling ready for a fun run, warm red-gold morning light, photorealistic, 1280x720",
 2:"Colorful family fun run start at Sanam Luang in Bangkok, families with kids at the start line, balloons and ribbons, cheerful festive morning, golden light, photorealistic, 1280x720",
 3:"A family running together along a Bangkok street past the golden Grand Palace spires, kids running happily, cheerful spectators cheering, warm golden morning light, photorealistic, 1280x720",
 4:"A family crossing the finish line together at Sanam Luang, confetti falling, parents and child celebrating with finisher medals, joyful smiles, bright warm tones, photorealistic, 1280x720",
 5:"A family enjoying a Thai food celebration after the run, mango sticky rice and fresh Thai dishes on the table, happy together, warm inviting light, photorealistic, 1280x720",
 6:"A relaxed family sightseeing at the Grand Palace and Bangkok riverside, golden afternoon light, light bokeh, happy casual holiday mood, photorealistic, 1280x720",
 7:"A family strolling through a lively Bangkok night market, colorful food stalls, warm lantern light, street food, joyful evening mood, photorealistic, 1280x720",
 8:"A group of families posing together at the race, kids and parents smiling, holding medals, warm sunset glow, candid joyful moments, photorealistic, 1280x720",
 9:"Hero shot of a family silhouette running together toward a golden finish arch, red and gold ribbons, dramatic backlight, cinematic, warm celebratory, photorealistic, 1280x720",
}

def post_json(url, body):
    req = urllib.request.Request(url, data=json.dumps(body).encode(),
                                 headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=60) as r:
        return json.loads(r.read().decode())

def get_json(url):
    req = urllib.request.Request(url, headers={"Accept": "application/json"})
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.loads(r.read().decode())

def build_graph(prompt, seed):
    return {
      "1":{"class_type":"UNETLoader","inputs":{"unet_name":"z_image_turbo_bf16.safetensors","weight_dtype":"default"}},
      "2":{"class_type":"CLIPLoader","inputs":{"clip_name":"qwen_3_4b.safetensors","type":"lumina2","device":"default"}},
      "3":{"class_type":"VAELoader","inputs":{"vae_name":"ae.safetensors"}},
      "4":{"class_type":"CLIPTextEncode","inputs":{"text":prompt,"clip":["2",0]}},
      "5":{"class_type":"ConditioningZeroOut","inputs":{"conditioning":["4",0]}},
      "6":{"class_type":"EmptySD3LatentImage","inputs":{"width":1280,"height":720,"batch_size":1}},
      "7":{"class_type":"ModelSamplingAuraFlow","inputs":{"shift":3,"model":["1",0]}},
      "8":{"class_type":"KSampler","inputs":{"seed":seed,"steps":8,"cfg":1.0,"sampler_name":"res_multistep","scheduler":"simple","denoise":1.0,"model":["7",0],"positive":["4",0],"negative":["5",0],"latent_image":["6",0]}},
      "9":{"class_type":"VAEDecode","inputs":{"samples":["8",0],"vae":["3",0]}},
     "10":{"class_type":"SaveImage","inputs":{"images":["9",0],"filename_prefix":"atmbkk_scene"}},
    }

def render_one(n, prompt):
    seed = random.randint(1, 2**31)
    pid = post_json(f"{SERVER}/prompt", {"prompt": build_graph(prompt, seed), "client_id": uuid.uuid4().hex})["prompt_id"]
    # poll
    while True:
        time.sleep(1)
        try:
            hist = get_json(f"{SERVER}/history/{pid}")
        except Exception:
            continue
        if pid in hist:
            node = hist[pid]["outputs"].get("10", {})
            if node.get("images"):
                fname = node["images"][0]["filename"]; sub = node["images"][0].get("subfolder","")
                url = f"{SERVER}/view?filename={urllib.parse.quote(fname)}&subfolder={urllib.parse.quote(sub)}&type=output"
                dest = os.path.join(OUT, f"s{n}.png")
                urllib.request.urlretrieve(url, dest)
                return dest, pid
            # maybe error
            st = hist[pid].get("status", {})
            print(f"  [s{n}] status={st}", file=sys.stderr)
        # safety timeout
        # (history present but not done → keep polling)

def main():
    start = time.time()
    for n in sorted(SCENES):
        dest, pid = render_one(n, SCENES[n])
        print(f"s{n} -> {dest} ({time.time()-start:.0f}s)")
    # release VRAM
    try: post_json(f"{SERVER}/free", {"unload_models": True, "free_memory": True})
    except Exception as e: print("free warn:", e)
    print("ALL 9 SCENES DONE")

if __name__ == "__main__":
    main()
