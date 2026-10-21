import os, torch, math
import numpy as np, pandas as pd
from PIL import Image
from argparse import ArgumentParser
import torch.nn.functional as F
from gaussian_renderer import render
from scene import Scene, GaussianModel
from scene.cameras import Camera
from arguments import ModelParams, PipelineParams

def qvec2rotmat(qvec):
    return np.array([
        [1 - 2*qvec[2]**2 - 2*qvec[3]**2, 2*qvec[1]*qvec[2] - 2*qvec[0]*qvec[3], 2*qvec[3]*qvec[1] + 2*qvec[0]*qvec[2]],
        [2*qvec[1]*qvec[2] + 2*qvec[0]*qvec[3], 1 - 2*qvec[1]**2 - 2*qvec[3]**2, 2*qvec[2]*qvec[3] - 2*qvec[0]*qvec[1]],
        [2*qvec[3]*qvec[1] - 2*qvec[0]*qvec[2], 2*qvec[2]*qvec[3] + 2*qvec[0]*qvec[1], 1 - 2*qvec[1]**2 - 2*qvec[2]**2]
    ])

def focal2fov(focal, pixels): 
    return 2 * math.atan(pixels / (2 * focal))

def main(model_path, csv_path, output_dir, source_path):
    try:
        import sys
        if hasattr(sys.stdout, 'reconfigure'):
            sys.stdout.reconfigure(encoding='utf-8')
        parser = ArgumentParser()
        model, pipeline = ModelParams(parser), PipelineParams(parser)
        args = parser.parse_args([])
        args.model_path = model_path
        args.source_path = source_path
        
        gaussians = GaussianModel(3, "sparse_adam") # sh_degree mặc định là 3
        ply_path = os.path.join(model_path, "point_cloud", "iteration_30000", "point_cloud.ply")
        gaussians.load_ply(ply_path)
        background = torch.tensor([0,0,0], dtype=torch.float32, device="cuda")
        
        os.makedirs(output_dir, exist_ok=True)
        df = pd.read_csv(csv_path)

        for _, row in df.iterrows():
            # --- NO SUPERSAMPLING TO AVOID OOM ---
            scale = 1
            w, h = int(row['width']) * scale, int(row['height']) * scale
            fx, fy = float(row['fx']) * scale, float(row['fy']) * scale
            cx, cy = float(row['cx']) * scale, float(row['cy']) * scale
            
            qvec = np.array([row['qw'], row['qx'], row['qy'], row['qz']])
            tvec = np.array([row['tx'], row['ty'], row['tz']])
            
            cam = Camera(resolution=(w, h), colmap_id=0, R=np.transpose(qvec2rotmat(qvec)), T=tvec, 
                         FoVx=focal2fov(fx, w), FoVy=focal2fov(fy, h), depth_params=None,
                         image=Image.new('RGB', (w, h)), invdepthmap=None, 
                         image_name=row['image_name'], uid=0, data_device="cuda",
                         cx=cx, cy=cy)
            
            with torch.no_grad():
                img = render(cam, gaussians, pipeline.extract(args), background)["render"]
                # Nén lại kích thước chuẩn bằng Area (chuyên trị Anti-aliasing dây cáp)
                img = F.interpolate(img.unsqueeze(0), size=(int(row['height']), int(row['width'])), mode='area').squeeze(0)
                
            img_np = (img.permute(1, 2, 0).clamp(0.0, 1.0).cpu().numpy() * 255).astype(np.uint8)
            Image.fromarray(img_np).save(os.path.join(output_dir, row['image_name']))
            print(f"✅ Rendered [SuperSampled]: {row['image_name']}")
    except Exception as e:
        import traceback
        with open("C:/Users/THIS PC/.gemini/antigravity-ide/scratch/viettel-ai-3dgs/render_crash.txt", "w") as f:
            traceback.print_exc(file=f)
        raise

if __name__ == "__main__":
    import sys
    main(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])
