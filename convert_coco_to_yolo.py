import json
import os
from pathlib import Path

def coco_to_yolo_segmentation(coco_json_path, output_dir):
    """
    將COCO格式的分割標註轉換為YOLO格式
    
    Args:
        coco_json_path: COCO JSON文件路徑
        output_dir: 輸出目錄路徑
    """
    
    # 讀取COCO JSON文件
    with open(coco_json_path, 'r', encoding='utf-8') as f:
        coco_data = json.load(f)
    
    # 創建輸出目錄
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # 建立圖片ID到圖片信息的映射
    image_info = {}
    for img in coco_data['images']:
        image_info[img['id']] = {
            'width': img['width'],
            'height': img['height'],
            'file_name': img['file_name']
        }
    
    # 建立類別ID到類別索引的映射（YOLO從0開始）
    category_mapping = {}
    for i, cat in enumerate(coco_data['categories']):
        category_mapping[cat['id']] = i
    
    # 按圖片分組處理標註
    annotations_by_image = {}
    for ann in coco_data['annotations']:
        image_id = ann['image_id']
        if image_id not in annotations_by_image:
            annotations_by_image[image_id] = []
        annotations_by_image[image_id].append(ann)
    
    # 為每個圖片生成YOLO格式的標註文件
    for image_id, annotations in annotations_by_image.items():
        if image_id not in image_info:
            continue
            
        img_info = image_info[image_id]
        img_width = img_info['width']
        img_height = img_info['height']
        
        # 生成對應的txt文件名（去掉副檔名，加上.txt）
        base_name = Path(img_info['file_name']).stem
        txt_file_path = output_dir / f"{base_name}.txt"
        
        yolo_lines = []
        
        for ann in annotations:
            # 獲取類別索引
            class_id = category_mapping[ann['category_id']]
            
            # 處理分割點
            segmentation = ann['segmentation'][0]  # 取第一個分割多邊形
            
            # 將像素坐標轉換為歸一化坐標
            normalized_points = []
            for i in range(0, len(segmentation), 2):
                x = segmentation[i] / img_width
                y = segmentation[i + 1] / img_height
                normalized_points.extend([x, y])
            
            # 構建YOLO格式的行
            points_str = ' '.join([f"{coord:.6f}" for coord in normalized_points])
            yolo_line = f"{class_id} {points_str}"
            yolo_lines.append(yolo_line)
        
        # 寫入txt文件
        with open(txt_file_path, 'w', encoding='utf-8') as f:
            f.write('\n'.join(yolo_lines))
        
        print(f"已生成: {txt_file_path}")

def print_conversion_info(coco_json_path):
    """
    打印轉換信息，幫助理解數據結構
    """
    with open(coco_json_path, 'r', encoding='utf-8') as f:
        coco_data = json.load(f)
    
    print("=== COCO數據信息 ===")
    print(f"圖片數量: {len(coco_data['images'])}")
    print(f"標註數量: {len(coco_data['annotations'])}")
    print(f"類別數量: {len(coco_data['categories'])}")
    
    print("\n=== 類別信息 ===")
    for i, cat in enumerate(coco_data['categories']):
        print(f"COCO ID: {cat['id']} -> YOLO ID: {i}, 名稱: {cat['name']}")
    
    print("\n=== 圖片信息示例 ===")
    for i, img in enumerate(coco_data['images'][:3]):  # 只顯示前3個
        print(f"圖片 {i+1}: {img['file_name']} ({img['width']}x{img['height']})")
    
    print("\n=== 標註信息示例 ===")
    for i, ann in enumerate(coco_data['annotations'][:2]):  # 只顯示前2個
        seg_points = len(ann['segmentation'][0]) // 2
        print(f"標註 {i+1}: 圖片ID={ann['image_id']}, 類別ID={ann['category_id']}, 分割點數={seg_points}")

# 使用示例
if __name__ == "__main__":
    # 設置文件路徑
    coco_json_path = "D:/ChengChung/End_face_measurement/lab/labels_my-project-name_2025-09-04-04-43-38.json"  # 您的COCO JSON文件路徑
    output_dir = "D:/ChengChung/End_face_measurement/lab/my_lab"  # YOLO標註輸出目錄
    
    # 打印轉換信息
    print_conversion_info(coco_json_path)
    
    print("\n=== 開始轉換 ===")
    # 執行轉換
    coco_to_yolo_segmentation(coco_json_path, output_dir)
    
    print(f"\n轉換完成！YOLO格式標註文件已保存到: {output_dir}")
    
    print("\n=== YOLO格式說明 ===")
    print("YOLO分割格式: class_id x1 y1 x2 y2 x3 y3 ...")
    print("- class_id: 類別索引（從0開始）")
    print("- xi yi: 歸一化的多邊形頂點坐標（0-1之間）")
    print("- 坐標順序按照原始分割點的順序排列")