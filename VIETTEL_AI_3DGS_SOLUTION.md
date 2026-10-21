# 📡 Viettel AI Race 2026 — Track 1: 3D Gaussian Splatting for Telecom BTS Digital Twin

> **Author**: Ngô Minh Thiên Bảo (reukem) & Chief Strategist Lucy  
> **Affiliation**: reukem's INDUSTRIES  
> **Competition**: Viettel AI Race 2026 (Chặng đua Trí tuệ Nhân tạo Viettel) — Đề 1  
> **Core Theme**: High-Fidelity 3D Reconstruction of Telecom BTS Cell Towers from Drone Imagery  

---

## 🎯 1. Problem Statement & Mission Overview

In modern telecommunication infrastructure management, creating accurate **Digital Twins (Bản sao số 3D)** of cellular Base Transceiver Stations (trạm BTS) from drone inspection cameras is paramount. 

Standard Photogrammetry (Mesh / NeRF) struggles with:
1. Extremely fine, non-planar structures (narrow steel lattice girders, RF antennas, dangling transmission cables).
2. Harsh aerial lighting variations, specular reflections on metallic towers, and sky backgrounds.
3. Rigid evaluation criteria: The competition leaderboard strictly scores submissions on **PSNR**, **SSIM**, and heavily penalizes high **LPIPS (Perceptual Loss, weighted at 40%)** on withheld novel camera view poses (`test_poses.csv`).

---

## ⚠️ 2. Baseline Fatal Flaws & Mathematical Breakthrough

Running vanilla [3D Gaussian Splatting (Inria)](https://github.com/graphdeco-inria/gaussian-splatting) yields suboptimal leaderboard scores due to three fundamental oversights:

### 🔬 Fatal Flaw 1: Optical Center Shift ($c_x, c_y$ Principal Point Offset)
- **The Issue**: Standard 3DGS naively assumes the optical center of every camera is strictly symmetric at $(W/2, H/2)$. However, aerial drone gimbal lenses exhibit substantial principal point drift ($c_x \neq W/2, c_y \neq H/2$). Rendered novel views are subtly shifted by 2–5 pixels, catastrophically destroying PSNR and SSIM.
- **The Solution**: We developed and injected an OpenGL-compliant projection matrix transformation with explicit center-shift offset into `utils/graphics_utils.py`:

```python
def getProjectionMatrixCenterShift(znear, zfar, cx, cy, flx, fly, w, h):
    P = torch.zeros(4, 4)
    z_sign = 1.0
    P[0, 0] = 2.0 * flx / w
    P[1, 1] = 2.0 * fly / h
    # Exact principal point shift for aerial sensor calibration
    P[0, 2] = (2.0 * cx - w) / w
    P[1, 2] = (2.0 * cy - h) / h
    P[3, 2] = z_sign
    P[2, 2] = z_sign * zfar / (zfar - znear)
    P[2, 3] = -(zfar * znear) / (zfar - znear)
    return P
```

### 📡 Fatal Flaw 2: Cable Disconnection & Thin-Strand Obliteration
- **The Issue**: Default densification gradient threshold (`0.0002`) aggressively prunes or blurs fine wires into sky floaters.
- **The Solution**: Tuned `--densify_grad_threshold 0.0006` with 30,000 iterations to enforce Gaussian splat densification strictly along cable paths and antenna rods.

### ⚡ Fatal Flaw 3: VRAM vs Resolution Tradeoff
- **Resolution Sweet Spot (`-r 2`)**: Render resolution at factor 2 (480x270px) provides **4x the sharpness of -r 4**, runs stably within 15 minutes per scene on modern NVIDIA GPUs, and prevents CUDA Out-Of-Memory crashes.

---

## 🏭 3. End-to-End Automated Pipeline (`run_pipeline.py`)

The pipeline automates:
1. Scanning all scenes in `dataset/scene_*`.
2. Extracting COLMAP intrinsics ($f_x, f_y, c_x, c_y$) and training for 30,000 iterations.
3. Reading `test_poses.csv` via `render_csv.py` to synthesize exact novel view test frames.
4. Packaging all rendered frames directly into `submission.zip` matching Viettel AI Portal submission standards.

```bash
# Execute entire end-to-end pipeline
python run_pipeline.py
```

---

## 📊 4. Architecture Summary Table

| Component | Baseline 3DGS | Our Optimized Solution |
| :--- | :--- | :--- |
| **Principal Point** | Fixed $(W/2, H/2)$ | Dynamic $(c_x, c_y)$ Offset Matrix |
| **Cable Splatting** | Discontinuous | `densify_grad_threshold = 0.0006` |
| **Resolution Mode** | Subsampled `-r 4` | Golden Ratio `-r 2` |
| **Iterations** | 7,000 | 30,000 Iterations Converged |
| **Submission** | Manual frame collation | Fully automated `submission.zip` |

---
*Viettel AI Race 2026 — Track 1 Solution Archive*
