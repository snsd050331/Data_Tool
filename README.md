# 🎬 影片拆分工具
## 安裝依賴項
```bash
pip install opencv-python
```
## 進行影片拆分
```bash
python video_extractor.py
```
### 輸入/出路徑  
=>可以使用絕對路徑/相對路徑  
=>輸出時可直接Enter，資料夾會自動生成extracted_frames資料夾，將資料處存進去
### 拆分模式
=> 1. 所有幀提取影像
=> 2. 按區間時間提取影像
### 時間間隔
基於秒數(S)去提取影像
### 圖片格式
支援 jpg / png / bmp 格式儲存
### 命名格式
以輸入影片名稱_frame_幀數進行命名  
=> 使用者可以照自我需求更改程式中filename的命名格式
