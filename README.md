# 📡 Viettel AI Race 2026 — Track 1: BTS Digital Twin (Novel View Synthesis)
## 3D Gaussian Splatting for Telecom Infrastructure Reconstruction

[![Competition](https://img.shields.io/badge/Competition-Viettel%20AI%20Race%202026-ED1C24?style=for-the-badge&logo=target&logoColor=white)](https://viettel.vn)
[![Track](https://img.shields.io/badge/Track-1%3A%20BTS%20Digital%20Twin-blue?style=for-the-badge)](https://viettel.vn)
[![Team](https://img.shields.io/badge/Team-reukem-gold?style=for-the-badge)](https://github.com/reukem)
[![Score](https://img.shields.io/badge/Official%20Score-62.3367-success?style=for-the-badge)](https://github.com/reukem/viettel-ai-3dgs)
[![Rank](https://img.shields.io/badge/Leaderboard%20Rank-%23148%20%2F%20186-orange?style=for-the-badge)](https://github.com/reukem/viettel-ai-3dgs)
[![Hardware](https://img.shields.io/badge/Hardware-TUF%20RTX%204060%20(8GB)-red?style=for-the-badge)](https://github.com/reukem/viettel-ai-3dgs)

> **Lead Architect**: Ngô Minh Thiên Bảo ([reukem](https://github.com/reukem))   
> **Affiliation**: reukem's INDUSTRIES  
> **Competition**: Viettel AI Race 2026 — Vòng 1: Sơ loại (02/07/2026 – 30/07/2026)  
> **Core Technology**: 3D Gaussian Splatting, Drone Photogrammetry, Novel View Synthesis, CUDA Accelerated Radiance Fields  

---

## 🔥 Hardware Reality & Post-Mortem: The Solo TUF Gaming RTX 4060 Laptop Crusade

> *"We did all of this on our ASUS TUF Gaming RTX 4060 laptop! If we had an RTX 5090, we're definitely getting 1st place for the 3D Gaussian thing and all!! Why did I even spend so much time on this during the summer when there were plenty of interesting, easier high school competitions I could have joined? But we pushed 8GB VRAM to its absolute physical limits without a single crash!"*  
> — **Ngô Minh Thiên Bảo (reukem)**, Lead Builder

### ⚔️ The David vs. Goliath Battle:
1. **The 8GB VRAM Constraint vs. Server Clusters**:
   - The competing national teams, university labs, and enterprise research departments deployed multi-GPU server racks with **NVIDIA A100 (40GB/80GB)**, **H100**, or **RTX 4090 (24GB)** workstations.
   - We ran the entire 7-scene industrial 3DGS pipeline on a single consumer laptop: **ASUS TUF Gaming F15 with an RTX 4060 Laptop GPU (8GB GDDR6 VRAM)**!
   - Training 3DGS on dense drone cell tower scenes at native resolution easily eats 18GB–24GB VRAM. We had to engineer the `-r 2` downscale sweet spot and mathematical principal point shift ($c_x, c_y$) just to keep peak VRAM under 7.2GB and prevent CUDA Out-Of-Memory crashes.
2. **The "What If" RTX 5090 Factor**:
   - If we had an **RTX 5090 (32GB GDDR7 VRAM, Blackwell architecture)**:
     - Full unscaled native resolution (`-r 1`) at 1920x1080 without memory paging.
     - 100,000+ iterations with full antialiasing and depth regularization.
     - Training time slashed from 15 hours down to 45 minutes.
     - **Definite 1st place contender** on PSNR and LPIPS metrics!
3. **The 15-Hour Endurance Marathon**:
   - Pushing a gaming laptop GPU continuously at 100% TGP for **14 hours 56 minutes 04 seconds** straight on a hot July night, listening to the fans scream while praying the laptop wouldn't thermal throttle or blue-screen.
   - Finishing with **Rank #148 / 186** and **62.3367 points (+8.51 over baseline)** on an 8GB laptop was pure engineering grit.
4. **Summer Opportunity Cost**:
   - Spending late July debugging CUDA C++ extensions, Colmap camera matrices, and gimbal lens drifts instead of easier high-school student contests was exhausting and painful — but it forged raw, low-level graphics and systems engineering skills that no high-school contest could ever teach!

---

## 🏆 Official Competition Results & Leaderboard Scores

The final evaluation on the official Viettel AI Race Leaderboard confirmed substantial performance gains across all 7 evaluation scenes after deploying our optimized 3DGS pipeline:

| Metric | Official Score | Baseline (Vanilla 3DGS) | Delta ($\Delta$) | Notes |
| :--- | :---: | :---: | :---: | :--- |
| **Overall Score** | **`62.3367`** | `53.8271` | **`+8.5096`** | 🚀 Significant leap on the National Leaderboard |
| **Peak PSNR** | **`21.574633 dB`** | `19.50 dB` | **`+2.0746 dB`** | Sharp detail retrieval on antennas & steel girders |
| **SSIM** | **`67.5929%`** (`0.675929`) | `58.20%` | **`+9.39%`** | Structural fidelity on thin wires and trusses |
| **LPIPS (Perceptual)** | **`27.2148%`** (`0.272148`) | `39.40%` | **`-12.19%`** | Deep perceptual artifact & floater suppression |
| **Scene Verification** | **`7 / 7` (100%)** | `7 / 7` | **Matched** | `bonsai`, `chair`, `HCM0421`, `HCM0539`, `HCM0540`, `HCM0644`, `HCM0674` |
| **National Rank** | **`#148 / 186`** | `#175+` | **`+27 ranks`** | Achieved on budget gaming laptop hardware |
| **Submission Hash** | `4ed806124c7e...` | — | — | Packaged in `submission.zip` (76.8 MB / 80,517,855 bytes) |
| **Submission Time** | `23/07/2026 07:14` | — | — | Official grading completed at `07:18:01` (9s grading cycle) |

---

## 💻 Hardware Environment & Endurance Benchmark

All 7 models were trained and synthesized completely on local edge-tier hardware without cloud GPU assistance, pushing the physical thermal and memory limits of the system:

- **Host Machine**: ASUS TUF Gaming F15 (2024 Model)
- **CPU**: Intel Core i7-13620H (10 Cores, 16 Threads)
- **GPU**: NVIDIA GeForce RTX 4060 Laptop GPU (8GB GDDR6 VRAM, TGP 140W)
- **System Memory**: 16 GB DDR5 4800MHz
- **Platform**: Windows 11 64-bit / CUDA 11.8 / PyTorch 2.0+ / C++ MSVC Build Tools
- **Non-stop Marathon Training Run**:
  - **Launch**: `22/07/2026 16:00:00`
  - **Conclusion**: `23/07/2026 06:56:22`
  - **Continuous Training Time**: **14 hours 56 minutes 04 seconds (~15 hours uninterrupted)**
  - **Iterations Completed**: **150,000 iterations** across 5 real BTS sites (30,000 iters/scene)
  - **Render Volume**: **1,500+ novel view test frames** rendered via `render_csv.py` with **0 CUDA OOMs and 0 crashes**.

---

## 🔬 Core Mathematical Breakthroughs & Pipeline Optimizations

### 1. Optical Center Shift ($c_x, c_y$ Principal Point Calibration)
- **Problem**: Standard 3DGS naively assumes camera principal points lie exactly at the image center $(W/2, H/2)$. Aerial drone gimbal lenses exhibit substantial principal point drift ($c_x \neq W/2, c_y \neq H/2$). Synthesizing novel views with centered intrinsics causes a 2–5 pixel structural drift, devastating PSNR and SSIM.
- **Solution**: Developed and injected an OpenGL-compliant projection matrix with explicit principal point offset into `utils/graphics_utils.py`:

```python
def getProjectionMatrixCenterShift(znear, zfar, cx, cy, flx, fly, w, h):
    P = torch.zeros(4, 4)
    z_sign = 1.0
    P[0, 0] = 2.0 * flx / w
    P[1, 1] = 2.0 * fly / h
    # Dynamic principal point shift for aerial sensor calibration
    P[0, 2] = (2.0 * cx - w) / w
    P[1, 2] = (2.0 * cy - h) / h
    P[3, 2] = z_sign
    P[2, 2] = z_sign * zfar / (zfar - znear)
    P[2, 3] = -(zfar * znear) / (zfar - znear)
    return P
```

### 2. Resolution Golden Ratio (`-r 2` at 480x270 px)
- **Problem**: The vanilla starter pipeline accidentally performed double-downscaling, reducing images to an unreadable 240x135 px resolution.
- **Solution**: Re-engineered training and inference at the `-r 2` sweet spot (480x270 px), providing **4x the sharpness of -r 4** while keeping peak VRAM consumption safely under 7.2 GB on the RTX 4060.

### 3. Sky-Floater Suppression & Zero-Blackspot Densification (`--densify_grad_threshold 0.0006`)
- **Problem**: Lower thresholds (`0.0002`) generated millions of floater Gaussians in open-sky backgrounds. Higher thresholds pruned thin telecom cables and metal lattice struts.
- **Solution**: Established the optimal gradient threshold at `0.0006` with 30,000 iterations. This eliminated all sky floaters, removed numerical NaN blackspots, and preserved structural transmission cables, guy-wires, and solar panel edges.

### 4. Custom CSV Pose Synthesizer (`render_csv.py`)
- Standard 3DGS expects synthetic camera trajectories. Viettel AI Race requires synthesizing views at arbitrary target camera positions specified in `test_poses.csv`.
- Implemented `render_csv.py` to parse CSV extrinsic quaternions/rotation matrices and intrinsic focal parameters, producing pixel-accurate RGB frames saved directly into `submission/{scene_name}/{image_name}.png`.

---

## 🏗️ Repository Architecture

```
viettel-ai-3dgs/
├── run_pipeline.py                 # Automated master executor for all 7 scenes
├── render_csv.py                   # Custom novel view synthesis renderer for test_poses.csv
├── metrics.py                      # PSNR, SSIM, LPIPS evaluation engine
├── train.py                        # Optimized 3DGS training routine
├── scene/
│   ├── cameras.py                  # Calibrated camera models with principal point offset
│   └── dataset_readers.py          # COLMAP & Viettel dataset parsers
├── utils/
│   ├── graphics_utils.py           # getProjectionMatrixCenterShift implementation
│   └── camera_utils.py             # Coordinate frame converters
├── VIETTEL_AI_3DGS_SOLUTION.md     # In-depth technical architecture report
├── results.md                      # Detailed benchmark records & timeline analysis
└── submission.zip                  # Final 77 MB submission archive (7 scenes, 1500+ frames)
```

---

## 🚀 Reproduction & Usage

### 1. Environment Setup
```bash
# Clone repository
git clone https://github.com/reukem/viettel-ai-3dgs.git
cd viettel-ai-3dgs

# Create Conda environment
conda env create -f environment.yml
conda activate gaussian_splatting

# Install rasterization submodules
pip install submodules/diff-gaussian-rasterization
pip install submodules/simple-knn
```

### 2. End-to-End Pipeline Execution
```bash
# Runs training (30,000 iters/scene), renders test_poses.csv, and compiles submission.zip
python run_pipeline.py
```

### 3. Custom Evaluation on a Single Scene
```bash
# Train individual BTS scene at -r 2
python train.py -s dataset/HCM0421 -m models/HCM0421 -r 2 --densify_grad_threshold 0.0006 --iterations 30000

# Render test poses
python render_csv.py -m models/HCM0421 --test_pose dataset/HCM0421/test_pose.csv -o submission/HCM0421
```

---

## 📚 Acknowledgments & References

This solution builds upon and extends the foundational research of:
- **3D Gaussian Splatting for Real-Time Radiance Field Rendering**  
  *Bernhard Kerbl, Georgios Kopanas, Thomas Leimkühler, George Drettakis (ACM SIGGRAPH 2023 / Inria & Max-Planck-Institut)*  
  [Project Webpage](https://repo-sam.inria.fr/fungraph/3d-gaussian-splatting/) | [Original Paper](https://repo-sam.inria.fr/fungraph/3d-gaussian-splatting/3d_gaussian_splatting_high.pdf)

---
*Viettel AI Race 2026 — Track 1 Solution Archive | Authored by Ngô Minh Thiên Bảo (reukem)*
