import os, subprocess, shutil, sys

# Fix Unicode encoding for Windows terminal
sys.stdout.reconfigure(encoding='utf-8')

DATA_DIR = "./dataset" # TRỎ VÀO THƯ MỤC CHỨA CÁC SCENE CỦA BẠN
MODELS_DIR, SUBMIT_DIR = "./models", "./submission"

def main():
    if not os.path.exists(DATA_DIR):
        print(f"❌ Không tìm thấy thư mục dữ liệu {DATA_DIR}!")
        return

    os.makedirs(MODELS_DIR, exist_ok=True)
    os.makedirs(SUBMIT_DIR, exist_ok=True)
    
    # Ví dụ danh sách các scene: scene_001, scene_002,...
    scenes = [d for d in os.listdir(DATA_DIR) if os.path.isdir(os.path.join(DATA_DIR, d))]
    
    for scene in scenes:
        print(f"\n🚀 ĐANG XỬ LÝ SCENE: {scene}")
        
        scene_train_path = os.path.join(DATA_DIR, scene, "train")
        scene_test_csv = os.path.join(DATA_DIR, scene, "test", "test_poses.csv")
        model_path = os.path.join(MODELS_DIR, scene)
        output_imgs_dir = os.path.join(SUBMIT_DIR, scene)
        
        # 1. TRAINING (Tiêu chuẩn SOTA 30,000 vòng lặp)
        if not os.path.exists(os.path.join(model_path, "point_cloud", "iteration_30000")):
            # Đếm số lượng ảnh để xác định độ nặng của scene
            images_dir = os.path.join(scene_train_path, "images")
            scene_size = len(os.listdir(images_dir)) if os.path.exists(images_dir) else 0
            
            # Dùng resolution = -r 2 (Điểm ngọt 480x270px: Nét gấp 4 lần -r 4 cũ, tốc độ 15p/scene, không tràn RAM)
            resolution = 2
            print(f"Scene {scene} có {scene_size} ảnh -> Dùng resolution = -r {resolution} (Điểm ngọt SOTA)")
            
            train_cmd = f'"{sys.executable}" train.py -s {scene_train_path} -m {model_path} -r {resolution} --iterations 30000 --densify_grad_threshold 0.0006'
            print(f"Chạy lệnh train: {train_cmd}")
            subprocess.run(train_cmd, shell=True, check=True)
        else:
            print(f"Bỏ qua train cho {scene}, mô hình đã được huấn luyện xong.")
        
        # 2. RENDERING
        render_cmd = f'"{sys.executable}" render_csv.py {model_path} {scene_test_csv} {output_imgs_dir} {scene_train_path}'
        print(f"Chạy lệnh render: {render_cmd}")
        subprocess.run(render_cmd, shell=True, check=True)
        
    # 3. ĐÓNG GÓI SUBMISSION THEO FORMAT
    print("\n📦 Đang nén file submission.zip...")
    # Nén đúng format bên trong thư mục chứ không nén bọc thư mục cha
    shutil.make_archive('submission', 'zip', SUBMIT_DIR)
    print("🎉 Hoàn tất! File submission.zip đã sẵn sàng để nộp!")

if __name__ == "__main__":
    main()
