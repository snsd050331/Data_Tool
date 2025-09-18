import os
import glob
from pathlib import Path

def get_filenames_without_extension(folder_path):
    """取得資料夾中所有檔案的檔名（不含副檔名）"""
    files = glob.glob(os.path.join(folder_path, "*"))
    return {Path(f).stem for f in files if os.path.isfile(f)}

def sync_folders(reference_folder, target_folder, dry_run=True):
    """
    同步兩個資料夾，刪除target_folder中多出來的檔案
    
    Args:
        reference_folder: 參考資料夾（基準）
        target_folder: 目標資料夾（要清理的資料夾）
        dry_run: 是否為測試模式（True時不會真正刪除檔案）
    """
    
    if not os.path.exists(reference_folder):
        print(f"錯誤：參考資料夾不存在 - {reference_folder}")
        return
    
    if not os.path.exists(target_folder):
        print(f"錯誤：目標資料夾不存在 - {target_folder}")
        return
    
    # 取得兩個資料夾的檔名集合（不含副檔名）
    reference_files = get_filenames_without_extension(reference_folder)
    target_files = get_filenames_without_extension(target_folder)
    
    print(f"參考資料夾 ({reference_folder}) 有 {len(reference_files)} 個檔案")
    print(f"目標資料夾 ({target_folder}) 有 {len(target_files)} 個檔案")
    
    # 找出目標資料夾中多出來的檔案
    extra_files = target_files - reference_files
    
    if not extra_files:
        print("沒有需要刪除的檔案")
        return
    
    print(f"\n找到 {len(extra_files)} 個多出來的檔案：")
    
    deleted_count = 0
    for filename in extra_files:
        # 找到實際的檔案路徑（含副檔名）
        matching_files = glob.glob(os.path.join(target_folder, f"{filename}.*"))
        
        for file_path in matching_files:
            print(f"{'[測試模式] ' if dry_run else ''}準備刪除: {file_path}")
            
            if not dry_run:
                try:
                    os.remove(file_path)
                    print(f"✓ 已刪除: {file_path}")
                    deleted_count += 1
                except Exception as e:
                    print(f"✗ 刪除失敗: {file_path} - {e}")
    
    if dry_run:
        print(f"\n[測試模式] 共會刪除 {len(extra_files)} 個檔案")
        print("如要實際執行刪除，請將 dry_run=False")
    else:
        print(f"\n完成！共刪除了 {deleted_count} 個檔案")

def main():
    # 設定資料夾路徑
    txt_folder = "D:/ChengChung/End_face_measurement/labels"      # 請修改為您的txt資料夾路徑
    image_folder = "D:/ChengChung/End_face_measurement/images"  # 請修改為您的image資料夾路徑
    
    print("Image資料夾清理工具")
    print("=" * 40)
    print("功能：以txt資料夾為基準，刪除image資料夾中多出來的檔案")
    print("比對方式：忽略副檔名，只比對檔案名稱")
    print()
    
    # 檢查資料夾是否存在
    if not os.path.exists(txt_folder):
        print(f"錯誤：txt資料夾不存在 - {txt_folder}")
        return
    
    if not os.path.exists(image_folder):
        print(f"錯誤：image資料夾不存在 - {image_folder}")
        return
    
    print(f"基準資料夾（txt）：{txt_folder}")
    print(f"清理資料夾（image）：{image_folder}")
    print()
    
    # 先執行測試模式
    print("=== 測試模式 - 檢查會刪除哪些檔案 ===")
    sync_folders(txt_folder, image_folder, dry_run=True)
    
    # 確認是否執行實際刪除
    print()
    confirm = input("確定要執行刪除操作嗎？(輸入 'DELETE' 確認): ").strip()
    if confirm == 'DELETE':
        print("\n=== 執行刪除操作 ===")
        sync_folders(txt_folder, image_folder, dry_run=False)
    else:
        print("操作已取消，未刪除任何檔案")

if __name__ == "__main__":
    main()