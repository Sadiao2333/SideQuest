import os
import shutil
from pathlib import Path
import subprocess

# 一、 移动文件函数
def move_files(source_dir, target_dir):
    source_path = Path(source_dir)
    target_path = Path(target_dir)
    target_path.mkdir(parents=True, exist_ok=True) # 没找到目标文件夹就新建一个
    moved_count = 0 # 计数
    
    # 1. 复制所有文件
    for file_path in source_path.rglob("*"):
        if file_path.is_file():
            target_file = target_path / file_path.name
            
            """
            # 处理重名（可选）
            counter = 1
            original_target = target_file
            while target_file.exists():
                stem = original_target.stem
                suffix = original_target.suffix
                target_file = original_target.parent / f"{stem} ({counter}){suffix}"
                counter += 1
            """

            print(f"已复制: {file_path.name}")
            shutil.copy2(file_path, target_file)
    
    print("所有文件复制完成。")
    
    # 2. 删除原文件
    for file_path in source_path.rglob("*"):
        if file_path.is_file():
            try:
                # 正常删除
                file_path.unlink()
                print(f"已删除: {file_path.name}")
                moved_count += 1
                   
            except PermissionError:
                # 命令行强制删除
                # Windows版
                if os.name == "nt":  
                    subprocess.run(["del", "/F", "/Q", str(file_path)], 
                                    shell=True, check=True, capture_output=True)
                # MacOS/Linux版
                else:  
                    subprocess.run(["rm", "-f", str(file_path)], 
                                    check=True, capture_output=True)
                print(f"已强制删除: {file_path.name}")
                moved_count += 1

    print(f"\n已成功移动 {moved_count} 个文件。")

# 二、 配置和运行
# ❗更改配置(以及喜欢的自变量命名)
wechat_downloads = "" # 需清理的文件夹的绝对路径
targeted_folder = "" # 目标文件夹的绝对路径
# 运行
move_files(wechat_downloads, targeted_folder)