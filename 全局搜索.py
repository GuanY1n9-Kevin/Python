import os
import json
import ctypes
import tkinter as tk
from tkinter import filedialog
import customtkinter as ctk

# ==========================================
# 核心魔法：强制开启 Windows 高 DPI 缩放，彻底解决界面模糊、像素低的问题
# ==========================================
try:
    ctypes.windll.shcore.SetProcessDpiAwareness(1)
except Exception:
    pass

# ==========================================
# 全局主题设置
# ==========================================
ctk.set_appearance_mode("System")  # 自动跟随系统的深色/浅色模式
ctk.set_default_color_theme("blue")  # 主题强调色：科技蓝


class ModernFileSearch:
    def __init__(self, root):
        self.root = root
        self.root.title("全局搜索")
        self.root.geometry("850x650")

        # 配置文件名称
        self.config_file = "search_config.json"
        self.all_files = []

        # --- 第一部分：顶部控制台 (圆角卡片设计) ---
        self.frame_top = ctk.CTkFrame(self.root, corner_radius=12)
        self.frame_top.pack(pady=(20, 10), padx=25, fill="x")

        self.btn_select = ctk.CTkButton(
            self.frame_top,
            text="📂 更改搜索目录",
            command=self.select_folder,
            font=("微软雅黑", 14, "bold"),
            height=40,
            corner_radius=8
        )
        self.btn_select.pack(side="left", padx=20, pady=15)

        self.lbl_folder = ctk.CTkLabel(
            self.frame_top,
            text="正在加载历史目录...",
            font=("微软雅黑", 13),
            text_color="gray"
        )
        self.lbl_folder.pack(side="left", padx=10)

        # --- 第二部分：沉浸式搜索框 ---
        self.frame_middle = ctk.CTkFrame(self.root, fg_color="transparent")
        self.frame_middle.pack(pady=10, padx=25, fill="x")

        self.search_var = tk.StringVar()
        self.search_var.trace_add("write", self.update_suggestions)

        self.entry_search = ctk.CTkEntry(
            self.frame_middle,
            textvariable=self.search_var,
            placeholder_text="🔍 在此输入要查找的文件名...",
            font=("微软雅黑", 16),
            height=50,
            corner_radius=25,  # 大圆角搜索框
            border_width=2
        )
        self.entry_search.pack(fill="x")

        # --- 第三部分：结果展示区 (无缝融合设计) ---
        self.frame_bottom = ctk.CTkFrame(self.root, corner_radius=12)
        self.frame_bottom.pack(pady=(10, 20), padx=25, fill="both", expand=True)

        self.lbl_tip = ctk.CTkLabel(
            self.frame_bottom,
            text="备选文件 (双击行即可在文件夹中定位):",
            font=("微软雅黑", 13, "bold")
        )
        self.lbl_tip.pack(anchor="w", padx=20, pady=(15, 5))

        # 列表容器
        self.list_container = ctk.CTkFrame(self.frame_bottom, fg_color="transparent")
        self.list_container.pack(fill="both", expand=True, padx=15, pady=(0, 15))

        self.scrollbar = ctk.CTkScrollbar(self.list_container)
        self.scrollbar.pack(side="right", fill="y")

        # 动态适配系统深浅色的列表框
        bg_color = "#2b2b2b" if ctk.get_appearance_mode() == "Dark" else "#f2f2f2"
        fg_color = "#ffffff" if ctk.get_appearance_mode() == "Dark" else "#000000"

        self.listbox = tk.Listbox(
            self.list_container,
            yscrollcommand=self.scrollbar.set,
            font=("微软雅黑", 11),
            bg=bg_color,
            fg=fg_color,
            selectbackground="#1f538d",
            selectforeground="white",
            borderwidth=0,
            highlightthickness=0,
            activestyle="none",  # 去除传统的丑陋虚线框
            relief="flat"
        )
        self.listbox.pack(side="left", fill="both", expand=True, padx=5)
        self.scrollbar.configure(command=self.listbox.yview)

        self.listbox.bind("<Double-1>", self.open_file_location)

        # --- 启动时加载历史记录 ---
        self.load_history_config()

    def load_history_config(self):
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    config = json.load(f)
                    last_path = config.get("last_path", "")
                    if os.path.exists(last_path):
                        self.lbl_folder.configure(text=last_path, text_color=("black", "white"))
                        self.scan_files(last_path)
                    else:
                        self.lbl_folder.configure(text="上次的路径已失效，请重新选择", text_color="#d65151")
            except Exception:
                self.lbl_folder.configure(text="请选择你要搜索的目录 ➔", text_color="gray")
        else:
            self.lbl_folder.configure(text="请先选择你要搜索的目录 ➔", text_color="gray")

    def save_config(self, path):
        try:
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump({"last_path": path}, f, ensure_ascii=False)
        except Exception as e:
            print(f"保存配置失败: {e}")

    def select_folder(self):
        folder = filedialog.askdirectory(title="请选择要扫描的文件夹")
        if folder:
            self.lbl_folder.configure(text=folder, text_color=("black", "white"))
            self.save_config(folder)
            self.scan_files(folder)

    def scan_files(self, folder_path):
        self.all_files = []
        self.listbox.delete(0, tk.END)
        self.listbox.insert(tk.END, " ⏳ 正在高速索引文件，请稍候...")
        self.root.update()

        count = 0
        try:
            for root_dir, _, files in os.walk(folder_path):
                for file in files:
                    self.all_files.append({
                        "name": file,
                        "path": os.path.join(root_dir, file)
                    })
                    count += 1
            self.listbox.delete(0, tk.END)
            self.listbox.insert(tk.END, f" ✅ 索引完成！共收录 {count} 个文件。直接在上方打字即可搜索。")
        except Exception as e:
            self.listbox.insert(tk.END, f" ❌ 扫描出错: {e}")

    def update_suggestions(self, *args):
        keyword = self.search_var.get().lower()
        self.listbox.delete(0, tk.END)

        if not self.all_files:
            self.listbox.insert(tk.END, "请先选择文件夹")
            return

        if not keyword:
            self.listbox.insert(tk.END, "等待输入...")
            return

        matches = 0
        for file in self.all_files:
            if keyword in file["name"].lower():
                self.listbox.insert(tk.END, f" 📄 {file['name']}    |    {file['path']}")
                matches += 1
                if matches >= 150:
                    self.listbox.insert(tk.END, "  ...(结果超过150条，请继续输入关键字以精准筛选)...")
                    break

        if matches == 0:
            self.listbox.insert(tk.END, " 👻 没找到匹配的文件")

    def open_file_location(self, event):
        selection = self.listbox.curselection()
        if not selection: return
        text = self.listbox.get(selection[0])
        if "    |    " in text:
            file_path = text.split("    |    ")[1]
            windows_path = file_path.replace("/", "\\")
            os.system(f'explorer /select,"{windows_path}"')


if __name__ == "__main__":
    # 创建现代化窗口引擎
    root = ctk.CTk()
    app = ModernFileSearch(root)
    root.mainloop()