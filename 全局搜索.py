import os
import json
import ctypes
import tkinter as tk
from tkinter import filedialog, ttk
import customtkinter as ctk

# ==========================================
# 核心魔法：强制开启 Windows 高 DPI 缩放
# ==========================================
try:
    ctypes.windll.shcore.SetProcessDpiAwareness(1)
except Exception:
    pass

ctk.set_appearance_mode("System")  # 自动跟随系统
ctk.set_default_color_theme("blue")  # 科技蓝


class ModernFileSearch:
    def __init__(self, root):
        self.root = root
        self.root.title("全局搜索")

        # 1. 调大初始界面：保证一打开就宽敞舒适
        self.root.geometry("1050x700")
        self.root.minsize(800, 500)

        self.config_file = "search_config.json"
        self.all_files = []

        # 配置主窗口权重，让动态缩放完全丝滑、不掉帧
        self.root.rowconfigure(2, weight=1)
        self.root.columnconfigure(0, weight=1)

        # --- 第一部分：顶部控制台 ---
        self.frame_top = ctk.CTkFrame(self.root, corner_radius=12)
        self.frame_top.grid(row=0, column=0, padx=25, pady=(20, 10), sticky="ew")

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

        # --- 第二部分：搜索框 ---
        self.frame_middle = ctk.CTkFrame(self.root, fg_color="transparent")
        self.frame_middle.grid(row=1, column=0, padx=25, pady=10, sticky="ew")

        self.search_var = tk.StringVar()
        self.search_var.trace_add("write", self.update_suggestions)

        self.entry_search = ctk.CTkEntry(
            self.frame_middle,
            textvariable=self.search_var,
            placeholder_text="🔍 输入关键字，瞬间秒搜文件...",
            font=("微软雅黑", 16),
            height=50,
            corner_radius=25,
            border_width=2
        )
        self.entry_search.pack(fill="x")

        # --- 第三部分：结果展示区 (网格化弹性布局) ---
        self.frame_bottom = ctk.CTkFrame(self.root, corner_radius=12)
        self.frame_bottom.grid(row=2, column=0, padx=25, pady=(10, 25), sticky="nsew")

        # 让底部容器内部也具备缩放权重
        self.frame_bottom.rowconfigure(1, weight=1)
        self.frame_bottom.columnconfigure(0, weight=1)

        self.lbl_tip = ctk.CTkLabel(
            self.frame_bottom,
            text="备选文件 (可双击行在文件夹中定位，可拖动表头边缘调整宽度):",
            font=("微软雅黑", 13, "bold")
        )
        self.lbl_tip.grid(row=0, column=0, sticky="w", padx=20, pady=(15, 5))

        # 列表容器
        self.list_container = ctk.CTkFrame(self.frame_bottom, fg_color="transparent")
        self.list_container.grid(row=1, column=0, padx=15, pady=(0, 15), sticky="nsew")
        self.list_container.rowconfigure(0, weight=1)
        self.list_container.columnconfigure(0, weight=1)

        # 动态适配系统深浅色的 Treeview 样式定制
        self.setup_treeview_style()

        # 创建 Treeview
        self.tree = ttk.Treeview(
            self.list_container,
            columns=("name", "path"),
            show="headings",
            style="Modern.Treeview"
        )

        self.tree.heading("name", text="文件名 📄")
        self.tree.heading("path", text="文件位置 📍")

        # 初始分配更合理的列宽比例
        self.tree.column("name", width=350, minwidth=150, anchor="w")
        self.tree.column("path", width=600, minwidth=200, anchor="w")

        # 现代化的右侧滚动条
        self.scrollbar = ctk.CTkScrollbar(self.list_container, command=self.tree.yview)
        self.scrollbar.grid(row=0, column=1, sticky="ns")
        self.tree.configure(yscrollcommand=self.scrollbar.set)

        self.tree.grid(row=0, column=0, sticky="nsew")

        # 双击事件
        self.tree.bind("<Double-1>", self.open_file_location)

        # 加载历史记录
        self.load_history_config()

    def setup_treeview_style(self):
        """配置 Treeview 的外观与行高，彻底告别文字重叠挤压"""
        is_dark = ctk.get_appearance_mode() == "Dark"

        bg_color = "#2b2b2b" if is_dark else "#ffffff"
        fg_color = "#ffffff" if is_dark else "#000000"
        header_bg = "#212121" if is_dark else "#eaeaea"
        header_fg = "#ffffff" if is_dark else "#000000"
        select_bg = "#1f538d"  # 科技蓝高亮

        style = ttk.Style()
        style.theme_use("clam")

        # 【核心修复】 rowheight=40 彻底拉开行距，让中文字体完美呼吸
        style.configure(
            "Modern.Treeview",
            background=bg_color,
            foreground=fg_color,
            fieldbackground=bg_color,
            rowheight=40,
            font=("微软雅黑", 11),
            borderwidth=0
        )

        # 配置表头样式 (同样给予充足的高度和加粗)
        style.configure(
            "Modern.Treeview.Heading",
            background=header_bg,
            foreground=header_fg,
            font=("微软雅黑", 12, "bold"),
            borderwidth=1,
            relief="flat"
        )

        # 鼠标悬停在表头上的效果
        style.map("Modern.Treeview.Heading", background=[('active', select_bg)], foreground=[('active', 'white')])

        # 配置选中行时的颜色
        style.map(
            "Modern.Treeview",
            background=[("selected", select_bg)],
            foreground=[("selected", "white")]
        )

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
        for item in self.tree.get_children():
            self.tree.delete(item)

        self.tree.insert("", "end", values=(" ⏳ 正在高速索引文件...", "请稍候..."))
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

            for item in self.tree.get_children():
                self.tree.delete(item)
            self.tree.insert("", "end", values=(f" ✅ 索引完成！共收录 {count} 个文件。", "直接在上方打字即可搜索。"))
        except Exception as e:
            for item in self.tree.get_children():
                self.tree.delete(item)
            self.tree.insert("", "end", values=(f" ❌ 扫描出错", str(e)))

    def update_suggestions(self, *args):
        keyword = self.search_var.get().lower()

        for item in self.tree.get_children():
            self.tree.delete(item)

        if not self.all_files:
            self.tree.insert("", "end", values=("请先选择文件夹", ""))
            return

        if not keyword:
            self.tree.insert("", "end", values=("等待输入...", ""))
            return

        matches = 0
        for file in self.all_files:
            if keyword in file["name"].lower():
                self.tree.insert("", "end", values=(file['name'], file['path']))
                matches += 1
                if matches >= 150:
                    self.tree.insert("", "end", values=("...(结果超过150条)", "请继续输入关键字以精准筛选)..."))
                    break

        if matches == 0:
            self.tree.insert("", "end", values=(" 👻 没找到匹配的文件", ""))

    def open_file_location(self, event):
        selection = self.tree.selection()
        if not selection:
            return

        item_data = self.tree.item(selection[0], "values")
        if len(item_data) >= 2:
            file_path = item_data[1]
            if os.path.exists(file_path):
                windows_path = file_path.replace("/", "\\")
                os.system(f'explorer /select,"{windows_path}"')


if __name__ == "__main__":
    root = ctk.CTk()
    app = ModernFileSearch(root)
    root.mainloop()
