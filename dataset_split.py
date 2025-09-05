import os
import shutil
import random
from pathlib import Path

def split_dataset(image_dir, label_dir, output_dir, train_ratio=0.7, val_ratio=0.2, test_ratio=0.1):
    """
    將圖像和標籤資料夾按指定比例分割成train、validation、test
    
    參數:
    image_dir: 圖像資料夾路徑
    label_dir: 標籤資料夾路徑  
    output_dir: 輸出資料夾路徑
    train_ratio: 訓練集比例 (預設0.7)
    val_ratio: 驗證集比例 (預設0.2)
    test_ratio: 測試集比例 (預設0.1)
    """
    
    # 檢查比例是否等於1
    if abs(train_ratio + val_ratio + test_ratio - 1.0) > 1e-6:
        raise ValueError("比例總和必須等於1")
    
    # 創建輸出資料夾結構
    output_path = Path(output_dir)
    splits = ['train', 'validation', 'test']
    
    for split in splits:
        (output_path / split / 'images').mkdir(parents=True, exist_ok=True)
        (output_path / split / 'labels').mkdir(parents=True, exist_ok=True)
    
    # 獲取所有圖像檔案
    image_path = Path(image_dir)
    image_extensions = {'.jpg', '.jpeg', '.png', '.bmp', '.tiff', '.tif'}
    image_files = [f for f in image_path.iterdir() 
                   if f.is_file() and f.suffix.lower() in image_extensions]
    
    if not image_files:
        raise ValueError(f"在 {image_dir} 中找不到圖像檔案")
    
    # 隨機打亂檔案列表
    random.seed(42)  # 設定隨機種子以確保結果可重現
    random.shuffle(image_files)
    
    # 計算分割點
    total_files = len(image_files)
    train_end = int(total_files * train_ratio)
    val_end = train_end + int(total_files * val_ratio)
    
    # 分割檔案列表
    train_files = image_files[:train_end]
    val_files = image_files[train_end:val_end]
    test_files = image_files[val_end:]
    
    # 複製檔案到對應資料夾
    def copy_files(files, split_name):
        copied_images = 0
        copied_labels = 0
        
        for img_file in files:
            # 複製圖像檔案
            src_img = img_file
            dst_img = output_path / split_name / 'images' / img_file.name
            shutil.copy2(src_img, dst_img)
            copied_images += 1
            
            # 尋找對應的標籤檔案
            # 假設標籤檔案與圖像檔案同名但副檔名不同
            label_extensions = {'.txt', '.xml', '.json', '.csv'}
            img_stem = img_file.stem
            
            label_found = False
            for ext in label_extensions:
                label_file = Path(label_dir) / (img_stem + ext)
                if label_file.exists():
                    dst_label = output_path / split_name / 'labels' / label_file.name
                    shutil.copy2(label_file, dst_label)
                    copied_labels += 1
                    label_found = True
                    break
            
            if not label_found:
                print(f"警告: 找不到 {img_file.name} 對應的標籤檔案")
        
        return copied_images, copied_labels
    
    # 執行分割
    print("開始分割資料集...")
    print(f"總共 {total_files} 個圖像檔案")
    print(f"分割比例 - 訓練集: {train_ratio}, 驗證集: {val_ratio}, 測試集: {test_ratio}")
    print("-" * 50)
    
    train_img, train_lbl = copy_files(train_files, 'train')
    val_img, val_lbl = copy_files(val_files, 'validation')
    test_img, test_lbl = copy_files(test_files, 'test')
    
    # 輸出統計結果
    print(f"訓練集: {train_img} 張圖像, {train_lbl} 個標籤")
    print(f"驗證集: {val_img} 張圖像, {val_lbl} 個標籤")
    print(f"測試集: {test_img} 張圖像, {test_lbl} 個標籤")
    print("-" * 50)
    print(f"資料集分割完成！輸出路徑: {output_dir}")

# 使用範例
if __name__ == "__main__":
    # 設定您的路徑
    image_directory = "D:/ChengChung/End_face_measurement/images"        # 替換為您的圖像資料夾路徑
    label_directory = "D:/ChengChung/End_face_measurement/labels"        # 替換為您的標籤資料夾路徑
    output_directory = "D:/ChengChung/End_face_measurement/dataset"    # 替換為輸出資料夾路徑
    
    try:
        split_dataset(
            image_dir=image_directory,
            label_dir=label_directory,
            output_dir=output_directory,
            train_ratio=0.7,    # 70% 訓練集
            val_ratio=0.2,      # 20% 驗證集
            test_ratio=0.1      # 10% 測試集
        )
    except Exception as e:
        print(f"錯誤: {e}")