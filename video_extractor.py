import cv2
import os
from pathlib import Path

class VideoFrameExtractor:
    def __init__(self, video_path, output_folder="extracted_frames"):
        """
        初始化影片幀提取器
        
        參數:
        video_path: 影片檔案路徑
        output_folder: 輸出資料夾名稱
        """
        self.video_path = video_path
        self.output_folder = output_folder
        
        # 確保輸出資料夾存在
        Path(self.output_folder).mkdir(parents=True, exist_ok=True)
    
    def extract_all_frames(self, image_format="jpg"):
        """
        提取影片中的所有幀
        
        參數:
        image_format: 圖片格式 (jpg, png, bmp等)
        """
        cap = cv2.VideoCapture(self.video_path)
        
        if not cap.isOpened():
            print("錯誤：無法開啟影片檔案")
            return False
        
        frame_count = 0
        success = True

        # 獲取影片名稱（不含路徑和副檔名）
        video_name = os.path.splitext(os.path.basename(self.video_path))[0]
        
        print(f"開始提取幀到資料夾: {self.output_folder}")
        
        while success:
            success, frame = cap.read()
            
            if success:
                # 生成檔案名稱
                filename = f"{video_name}_frame_{frame_count:06d}.{image_format}"
                filepath = os.path.join(self.output_folder, filename)
                
                # 保存幀
                cv2.imwrite(filepath, frame)
                frame_count += 1
                
                # 每100幀顯示進度
                if frame_count % 100 == 0:
                    print(f"已提取 {frame_count} 幀...")
        
        cap.release()
        print(f"完成！總共提取了 {frame_count} 幀")
        return True
    
    def extract_frames_by_interval(self, interval_seconds=1, image_format="jpg"):
        """
        按時間間隔提取幀
        
        參數:
        interval_seconds: 提取間隔（秒）
        image_format: 圖片格式 ("jpg", "png", "bmp" 等)
        """
        cap = cv2.VideoCapture(self.video_path)
        
        if not cap.isOpened():
            print("錯誤：無法開啟影片檔案")
            return False
        
        try:
            # 獲取影片資訊
            fps = cap.get(cv2.CAP_PROP_FPS)
            total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
            
            # 檢查 FPS 是否有效
            if fps <= 0:
                print("錯誤：無法獲取有效的幀率")
                return False
                
            duration = total_frames / fps
            
            print(f"影片資訊：")
            print(f"- 總幀數: {total_frames}")
            print(f"- 幀率: {fps:.2f} FPS")
            print(f"- 總時長: {duration:.2f} 秒")
            print(f"- 提取間隔: {interval_seconds} 秒")
            
            # 確保輸出目錄存在
            os.makedirs(self.output_folder, exist_ok=True)
            
            frame_interval = int(fps * interval_seconds)
            extracted_count = 0
            current_frame = 0
            
            # 獲取影片名稱（不含路徑和副檔名）
            video_name = os.path.splitext(os.path.basename(self.video_path))[0]
            
            while current_frame < total_frames:
                # 跳到指定幀
                cap.set(cv2.CAP_PROP_POS_FRAMES, current_frame)
                success, frame = cap.read()
                
                if success:
                    # 計算時間戳
                    timestamp = current_frame / fps
                    
                    # 生成檔案名稱 - 更完整的命名格式
                    filename = f"{video_name}_frame_{extracted_count:04d}.{image_format}"
                    filepath = os.path.join(self.output_folder, filename)
                    
                    # 保存幀
                    if cv2.imwrite(filepath, frame):
                        extracted_count += 1
                        print(f"提取第 {extracted_count} 幀 (時間: {timestamp:.2f}s) -> {filename}")
                    else:
                        print(f"警告：無法保存幀到 {filepath}")
                else:
                    print(f"警告：無法讀取第 {current_frame} 幀")
                
                current_frame += frame_interval
        
        except Exception as e:
            print(f"錯誤：處理過程中發生異常 - {str(e)}")
            return False
        
        finally:
            cap.release()
        
        print(f"完成！總共提取了 {extracted_count} 幀")
        return extracted_count > 0  # 返回是否成功提取了至少一幀

# 使用範例
if __name__ == "__main__":
    # 設定輸入/出路徑
    print("\n輸入/出路徑範例:")
    print("- 絕對路徑: C:\\Users\\Username\\Desktop\\frames")
    print("- 絕對路徑: /home/username/videos/frames")  
    print("- 相對路徑: ./output_frames")
    print("- 相對路徑: ../frames")

    # 設定影片路徑
    video_path = input("請輸入影片檔案路徑: ").strip('"')  # 去除可能的引號
   
    output_path = input("\n請輸入輸出資料夾路徑 (直接按Enter使用預設路徑): ").strip('"')
    if not output_path:
        output_path = "extracted_frames"
    
    # 創建提取器
    try:
        extractor = VideoFrameExtractor(video_path, output_path)
    except Exception as e:
        print(f"錯誤: {e}")
        exit(1)
    
    print("\n選擇提取模式：")
    print("1. 提取所有幀")
    print("2. 按時間間隔提取")
    
    choice = input("請輸入選項 (1-2): ")
    
    if choice == "1":
        format_choice = input("圖片格式 (jpg/png/bmp, 預設jpg): ").lower() or "jpg"
        extractor.extract_all_frames(format_choice)
    
    elif choice == "2":
        try:
            interval = float(input("請輸入時間間隔（秒）: "))
            format_choice = input("圖片格式 (jpg/png/bmp, 預設jpg): ").lower() or "jpg"
            extractor.extract_frames_by_interval(interval, format_choice)
        except ValueError:
            print("錯誤：請輸入有效的數字")
    
    else:
        print("無效選項")