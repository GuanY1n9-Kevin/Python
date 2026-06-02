import customtkinter as ctk
import math

# =======================================================
# 【全局设置】
# =======================================================
ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")


class FiberCalculatorApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("纺丝工艺参数计算器 v2.9")
        self.geometry("880x760")

        # =======================================================
        # 【左侧导航区】：包含 1 - 9 号所有按钮
        # =======================================================
        self.sidebar_frame = ctk.CTkFrame(self, width=190, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, rowspan=10, sticky="nsew")

        # 将第10行设为“弹簧”，把底部的密度参考面板牢牢压在最底下
        self.sidebar_frame.grid_rowconfigure(10, weight=1)

        self.logo_label = ctk.CTkLabel(self.sidebar_frame, text="纤维工艺计算",
                                       font=ctk.CTkFont(size=18, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))

        self.btn_denier = ctk.CTkButton(self.sidebar_frame, text="1. 纤度计算 (圈数)", command=self.show_denier_frame)
        self.btn_denier.grid(row=1, column=0, padx=15, pady=8)

        self.btn_capacity = ctk.CTkButton(self.sidebar_frame, text="2. 纺丝产能预估", command=self.show_capacity_frame)
        self.btn_capacity.grid(row=2, column=0, padx=15, pady=8)

        self.btn_len_wt = ctk.CTkButton(self.sidebar_frame, text="3. 长重双向转换", command=self.show_len_wt_frame)
        self.btn_len_wt.grid(row=3, column=0, padx=15, pady=8)

        self.btn_pump = ctk.CTkButton(self.sidebar_frame, text="4. 变频器比例换算", command=self.show_pump_freq_frame)
        self.btn_pump.grid(row=4, column=0, padx=15, pady=8)

        self.btn_tensile = ctk.CTkButton(self.sidebar_frame, text="5. 纱线拉力计算", command=self.show_tensile_frame)
        self.btn_tensile.grid(row=5, column=0, padx=15, pady=8)

        self.btn_oil = ctk.CTkButton(self.sidebar_frame, text="6. 纱线需油量计算", command=self.show_oil_frame)
        self.btn_oil.grid(row=6, column=0, padx=15, pady=8)

        self.btn_phy = ctk.CTkButton(self.sidebar_frame, text="7. 纱线物性与对比", command=self.show_physical_frame)
        self.btn_phy.grid(row=7, column=0, padx=15, pady=8)

        self.btn_extrusion = ctk.CTkButton(self.sidebar_frame, text="8. 挤出与纤度预测",
                                           command=self.show_extrusion_frame)
        self.btn_extrusion.grid(row=8, column=0, padx=15, pady=8)

        self.btn_strobe = ctk.CTkButton(self.sidebar_frame, text="9. 频闪仪线速度换算", command=self.show_strobe_frame)
        self.btn_strobe.grid(row=9, column=0, padx=15, pady=8)

        # =======================================================
        # 【左侧静态面板区】：补回之前误删的创建代码
        # =======================================================
        self.density_frame = ctk.CTkFrame(self.sidebar_frame, fg_color="transparent")
        self.density_frame.grid(row=11, column=0, padx=20, pady=25, sticky="sw")

        self.density_title = ctk.CTkLabel(self.density_frame, text="常用材质密度参考：",
                                          font=ctk.CTkFont(size=13, weight="bold"), text_color="gray")
        self.density_title.pack(anchor="w", pady=(0, 6))
        ctk.CTkLabel(self.density_frame, text="• PP纱(丙纶): 0.91 g/cm³", font=ctk.CTkFont(size=12),
                     text_color="gray").pack(anchor="w", pady=2)
        ctk.CTkLabel(self.density_frame, text="• 尼龙(锦纶): 1.14 g/cm³", font=ctk.CTkFont(size=12),
                     text_color="gray").pack(anchor="w", pady=2)
        ctk.CTkLabel(self.density_frame, text="• 特多(涤纶): 1.38 g/cm³", font=ctk.CTkFont(size=12),
                     text_color="gray").pack(anchor="w", pady=2)

        # =======================================================
        # 【右侧主界面容器】
        # =======================================================
        self.main_frame = ctk.CTkFrame(self, corner_radius=12)
        self.main_frame.grid(row=0, column=1, rowspan=12, padx=20, pady=20, sticky="nsew")
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # 默认开机展示9号双向换算功能
        self.show_strobe_frame()

    def clear_main_frame(self):
        for widget in self.main_frame.winfo_children():
            widget.destroy()

    # =======================================================
    # 【1号功能区】：纤度计算
    # =======================================================
    def show_denier_frame(self):
        self.clear_main_frame()
        title = ctk.CTkLabel(self.main_frame, text="纱线纤度计算", font=ctk.CTkFont(size=20, weight="bold"))
        title.pack(pady=(20, 5))
        formula_label = ctk.CTkLabel(self.main_frame, text="⚙️ 计算公式：\n丹尼数 (D) = (克重 ÷ 圈数) × 9000",
                                     font=ctk.CTkFont(size=13, slant="italic"), text_color="gray")
        formula_label.pack(pady=(0, 15))

        input_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        input_frame.pack(pady=5)
        ctk.CTkLabel(input_frame, text="测试圈数 (圈):", font=ctk.CTkFont(size=14)).grid(row=0, column=0, padx=10,
                                                                                         pady=12, sticky="e")
        self.entry_turns = ctk.CTkEntry(input_frame, width=180)
        self.entry_turns.insert(0, "90")
        self.entry_turns.grid(row=0, column=1, padx=10, pady=12)

        ctk.CTkLabel(input_frame, text="天平称重 (克, g):", font=ctk.CTkFont(size=14)).grid(row=1, column=0, padx=10,
                                                                                            pady=12, sticky="e")
        self.entry_weight = ctk.CTkEntry(input_frame, width=180)
        self.entry_weight.grid(row=1, column=1, padx=10, pady=12)

        btn_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        btn_frame.pack(pady=15)
        ctk.CTkButton(btn_frame, text="开始换算", font=ctk.CTkFont(size=15, weight="bold"), height=35,
                      command=self.calc_denier).pack(side="left", padx=10)
        ctk.CTkButton(btn_frame, text="一键清空", font=ctk.CTkFont(size=15), height=35, fg_color="#7f8c8d",
                      hover_color="#95a5a6", command=self.clear_denier_inputs).pack(side="left", padx=10)

        self.result_label_denier = ctk.CTkLabel(self.main_frame, text="", font=ctk.CTkFont(size=18, weight="bold"))
        self.result_label_denier.pack(pady=10)

    def calc_denier(self):
        try:
            t, w = float(self.entry_turns.get()), float(self.entry_weight.get())
            if t <= 0 or w <= 0: return
            self.result_label_denier.configure(
                text=f"旦尼尔数: {(w / t) * 9000:.2f} D\n分特克斯: {(w / t) * 10000:.2f} dtex", text_color="green")
        except ValueError:
            self.result_label_denier.configure(text="输入错误！", text_color="red")

    def clear_denier_inputs(self):
        self.entry_turns.delete(0, 'end')
        self.entry_turns.insert(0, "90")
        self.entry_weight.delete(0, 'end')
        self.result_label_denier.configure(text="")

    # =======================================================
    # 【2号功能区】：纺丝产能计算
    # =======================================================
    def show_capacity_frame(self):
        self.clear_main_frame()
        title = ctk.CTkLabel(self.main_frame, text="纺丝产能与产量预估", font=ctk.CTkFont(size=20, weight="bold"))
        title.pack(pady=(20, 5))

        formula_text = (
            "⚙️ 计算公式推导：\n"
            "每小时总长度 = 卷绕速度(m/min) × 60分钟\n"
            "单锭产能(kg/h) = (每小时总长度 × 丹尼数) ÷ (9000米 × 1000克)\n"
            "总产量(kg) = 单锭产能 × 锭数 × 工作时间"
        )
        ctk.CTkLabel(self.main_frame, text=formula_text, font=ctk.CTkFont(size=13, slant="italic"), text_color="gray",
                     justify="left").pack(pady=(0, 10))

        input_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        input_frame.pack(pady=5)

        ctk.CTkLabel(input_frame, text="卷绕速度 (m/min):", font=ctk.CTkFont(size=14)).grid(row=0, column=0, padx=10,
                                                                                            pady=8, sticky="e")
        self.entry_speed = ctk.CTkEntry(input_frame, width=150)
        self.entry_speed.grid(row=0, column=1, padx=10, pady=8)

        ctk.CTkLabel(input_frame, text="纱线纤度 (Denier):", font=ctk.CTkFont(size=14)).grid(row=1, column=0, padx=10,
                                                                                             pady=8, sticky="e")
        self.entry_den = ctk.CTkEntry(input_frame, width=150)
        self.entry_den.grid(row=1, column=1, padx=10, pady=8)

        ctk.CTkLabel(input_frame, text="卷绕头数 (锭):", font=ctk.CTkFont(size=14)).grid(row=2, column=0, padx=10,
                                                                                         pady=8, sticky="e")
        self.entry_ends = ctk.CTkEntry(input_frame, width=150)
        self.entry_ends.insert(0, "1")
        self.entry_ends.grid(row=2, column=1, padx=10, pady=8)

        ctk.CTkLabel(input_frame, text="工作时间 (小时):", font=ctk.CTkFont(size=14)).grid(row=3, column=0, padx=10,
                                                                                           pady=8, sticky="e")
        self.entry_hours = ctk.CTkEntry(input_frame, width=150)
        self.entry_hours.insert(0, "24")
        self.entry_hours.grid(row=3, column=1, padx=10, pady=8)

        btn_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        btn_frame.pack(pady=15)
        ctk.CTkButton(btn_frame, text="计算产能", font=ctk.CTkFont(size=15, weight="bold"), height=35,
                      command=self.calc_capacity).pack(side="left", padx=10)
        ctk.CTkButton(btn_frame, text="一键清空", font=ctk.CTkFont(size=15), height=35, fg_color="#7f8c8d",
                      hover_color="#95a5a6", command=self.clear_capacity_inputs).pack(side="left", padx=10)

        self.result_box_cap = ctk.CTkFrame(self.main_frame, width=380, height=100, corner_radius=8)
        self.result_box_cap.pack(pady=5)
        self.result_box_cap.pack_propagate(False)

        self.result_label_cap = ctk.CTkLabel(self.result_box_cap, text="请输入参数后计算", font=ctk.CTkFont(size=14),
                                             text_color="gray")
        self.result_label_cap.pack(expand=True, fill="both", padx=10, pady=10)

    def calc_capacity(self):
        try:
            speed = float(self.entry_speed.get())
            denier = float(self.entry_den.get())
            ends = float(self.entry_ends.get())
            hours = float(self.entry_hours.get())

            if speed <= 0 or denier <= 0 or ends <= 0 or hours <= 0: return

            hourly_kg_per_end = (speed * denier) / 150000
            hourly_kg_total = hourly_kg_per_end * ends
            total_production = hourly_kg_total * hours

            result_text = f"整机小时产能: {hourly_kg_total:.2f} kg/h\n\n" \
                          f"设定 {hours:g} 小时总产量预估: {total_production:.2f} kg"

            self.result_label_cap.configure(text=result_text, text_color="green",
                                            font=ctk.CTkFont(size=16, weight="bold"))
        except ValueError:
            self.result_label_cap.configure(text="输入错误！请确保所有框内都是数字。", text_color="red")

    def clear_capacity_inputs(self):
        self.entry_speed.delete(0, 'end')
        self.entry_den.delete(0, 'end')
        self.entry_ends.delete(0, 'end');
        self.entry_ends.insert(0, "1")
        self.entry_hours.delete(0, 'end');
        self.entry_hours.insert(0, "24")
        self.result_label_cap.configure(text="请输入参数后计算", text_color="gray")

    # =======================================================
    # 【3号功能区】：长重智能转换
    # =======================================================
    def show_len_wt_frame(self):
        self.clear_main_frame()

        title = ctk.CTkLabel(self.main_frame, text="长度与重量转换", font=ctk.CTkFont(size=20, weight="bold"))
        title.pack(pady=(20, 5))

        info_label = ctk.CTkLabel(self.main_frame, text="💡 必填规格。然后在 长度/千克/克 中【填入1个，留空2个】自动补全",
                                  font=ctk.CTkFont(size=13), text_color="gray")
        info_label.pack(pady=(0, 20))

        frame_lw = ctk.CTkFrame(self.main_frame, corner_radius=10)
        frame_lw.pack(fill="x", padx=40, pady=10)

        self.combo_unit = ctk.CTkComboBox(frame_lw, values=["丹尼数 (D)", "线密度 (dtex)"], width=130)
        self.combo_unit.grid(row=0, column=0, padx=10, pady=15, sticky="e")
        self.entry_spec = ctk.CTkEntry(frame_lw, width=150, placeholder_text="必填")
        self.entry_spec.grid(row=0, column=1, padx=10, pady=15)

        ctk.CTkLabel(frame_lw, text="长度 (米):", font=ctk.CTkFont(size=14)).grid(row=1, column=0, padx=10, pady=10,
                                                                                  sticky="e")
        self.entry_len = ctk.CTkEntry(frame_lw, width=150, placeholder_text="留空或输入")
        self.entry_len.grid(row=1, column=1, padx=10, pady=10)

        ctk.CTkLabel(frame_lw, text="重量 (千克/kg):", font=ctk.CTkFont(size=14)).grid(row=2, column=0, padx=10,
                                                                                       pady=10, sticky="e")
        self.entry_kg = ctk.CTkEntry(frame_lw, width=150, placeholder_text="留空或输入")
        self.entry_kg.grid(row=2, column=1, padx=10, pady=10)

        ctk.CTkLabel(frame_lw, text="重量 (克/g):", font=ctk.CTkFont(size=14)).grid(row=3, column=0, padx=10, pady=10,
                                                                                    sticky="e")
        self.entry_g = ctk.CTkEntry(frame_lw, width=150, placeholder_text="留空或输入")
        self.entry_g.grid(row=3, column=1, padx=10, pady=10)

        btn_frame = ctk.CTkFrame(frame_lw, fg_color="transparent")
        btn_frame.grid(row=1, column=2, rowspan=3, padx=20)
        ctk.CTkButton(btn_frame, text="智能联动计算", font=ctk.CTkFont(size=14, weight="bold"), height=35,
                      command=self.calc_len_wt).pack(pady=5)
        ctk.CTkButton(btn_frame, text="一键清空", font=ctk.CTkFont(size=14), height=35, fg_color="#7f8c8d",
                      hover_color="#95a5a6", command=self.clear_len_wt_inputs).pack(pady=5)

        self.result_lw = ctk.CTkLabel(self.main_frame, text="", font=ctk.CTkFont(size=16, weight="bold"))
        self.result_lw.pack(pady=20)

    def calc_len_wt(self):
        try:
            spec_val = float(self.entry_spec.get())
            factor = 9000 if (self.combo_unit.get() == "丹尼数 (D)") else 10000

            l_str, kg_str, g_str = self.entry_len.get().strip(), self.entry_kg.get().strip(), self.entry_g.get().strip()
            filled_count = sum([1 for x in [l_str, kg_str, g_str] if x != ""])
            if filled_count != 1:
                self.result_lw.configure(text="❌ 错误：在 长度、千克、克 中，只能填写【其中1个】！", text_color="red")
                return

            if l_str:
                L = float(l_str)
                W_g = (spec_val * L) / factor
                W_kg = W_g / 1000
                self.entry_g.delete(0, 'end');
                self.entry_g.insert(0, f"{W_g:.2f}")
                self.entry_kg.delete(0, 'end');
                self.entry_kg.insert(0, f"{W_kg:.4f}")
            elif kg_str:
                W_kg = float(kg_str)
                W_g = W_kg * 1000
                L = (W_g * factor) / spec_val
                self.entry_len.delete(0, 'end');
                self.entry_len.insert(0, f"{L:.2f}")
                self.entry_g.delete(0, 'end');
                self.entry_g.insert(0, f"{W_g:.2f}")
            elif g_str:
                W_g = float(g_str)
                W_kg = W_g / 1000
                L = (W_g * factor) / spec_val
                self.entry_len.delete(0, 'end');
                self.entry_len.insert(0, f"{L:.2f}")
                self.entry_kg.delete(0, 'end');
                self.entry_kg.insert(0, f"{W_kg:.4f}")

            self.result_lw.configure(text="✅ 自动补全计算完成！", text_color="green")
        except ValueError:
            self.result_lw.configure(text="输入格式错误！请确保填入的是纯数字。", text_color="red")

    def clear_len_wt_inputs(self):
        self.entry_spec.delete(0, 'end')
        self.entry_len.delete(0, 'end')
        self.entry_kg.delete(0, 'end')
        self.entry_g.delete(0, 'end')
        self.result_lw.configure(text="")

    # =======================================================
    # 【4号功能区】：计量泵变频比例换算
    # =======================================================
    def show_pump_freq_frame(self):
        self.clear_main_frame()
        title = ctk.CTkLabel(self.main_frame, text="变频器比例换算", font=ctk.CTkFont(size=20, weight="bold"))
        title.pack(pady=(20, 5))
        formula_label = ctk.CTkLabel(self.main_frame, text="⚙️ 所需变频器 = ( 目标丹尼数 × 现有变频器 ) ÷ 现有丹尼数",
                                     font=ctk.CTkFont(size=14, slant="italic"), text_color="gray")
        formula_label.pack(pady=(0, 20))

        input_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        input_frame.pack(pady=5)

        ctk.CTkLabel(input_frame, text="现有丹尼数 (D1):", font=ctk.CTkFont(size=15)).grid(row=0, column=0, padx=10,
                                                                                           pady=10, sticky="e")
        self.entry_p_D1 = ctk.CTkEntry(input_frame, width=150)
        self.entry_p_D1.grid(row=0, column=1, padx=10, pady=10)

        ctk.CTkLabel(input_frame, text="现有变频器 (g1):", font=ctk.CTkFont(size=15)).grid(row=1, column=0, padx=10,
                                                                                           pady=10, sticky="e")
        self.entry_p_g1 = ctk.CTkEntry(input_frame, width=150)
        self.entry_p_g1.grid(row=1, column=1, padx=10, pady=10)

        ctk.CTkLabel(input_frame, text="目标丹尼数 (D2):", font=ctk.CTkFont(size=15)).grid(row=2, column=0, padx=10,
                                                                                           pady=10, sticky="e")
        self.entry_p_D2 = ctk.CTkEntry(input_frame, width=150)
        self.entry_p_D2.grid(row=2, column=1, padx=10, pady=10)

        btn_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        btn_frame.pack(pady=20)
        ctk.CTkButton(btn_frame, text="立即换算", font=ctk.CTkFont(size=15, weight="bold"), height=35,
                      command=self.calc_pump_freq).pack(side="left", padx=10)
        ctk.CTkButton(btn_frame, text="一键清空", font=ctk.CTkFont(size=15), height=35, fg_color="#7f8c8d",
                      hover_color="#95a5a6", command=self.clear_pump_inputs).pack(side="left", padx=10)

        self.result_label_pump = ctk.CTkLabel(self.main_frame, text="", font=ctk.CTkFont(size=18, weight="bold"))
        self.result_label_pump.pack(pady=10)

    def calc_pump_freq(self):
        try:
            D1, g1, D2 = float(self.entry_p_D1.get()), float(self.entry_p_g1.get()), float(self.entry_p_D2.get())
            if D1 <= 0: return
            self.result_label_pump.configure(text=f"🎯 目标变频器 (g2) 应调整为：\n\n {((D2 * g1) / D1):.2f} ",
                                             text_color="green")
        except ValueError:
            self.result_label_pump.configure(text="输入错误！", text_color="red")

    def clear_pump_inputs(self):
        self.entry_p_D1.delete(0, 'end')
        self.entry_p_g1.delete(0, 'end')
        self.entry_p_D2.delete(0, 'end')
        self.result_label_pump.configure(text="")

    # =======================================================
    # 【5号功能区】：纱线承受拉力计算
    # =======================================================
    def show_tensile_frame(self):
        self.clear_main_frame()
        title = ctk.CTkLabel(self.main_frame, text="纱线承受拉力计算", font=ctk.CTkFont(size=20, weight="bold"))
        title.pack(pady=(20, 5))

        formula_label = ctk.CTkLabel(self.main_frame, text="⚙️ 计算公式：\n承受拉力 (kg) = (丹尼数 × 断裂强度) ÷ 1000",
                                     font=ctk.CTkFont(size=13, slant="italic"), text_color="gray")
        formula_label.pack(pady=(0, 20))

        input_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        input_frame.pack(pady=5)

        ctk.CTkLabel(input_frame, text="纱线纤度 (Denier):", font=ctk.CTkFont(size=14)).grid(row=0, column=0, padx=10,
                                                                                             pady=10, sticky="e")
        self.entry_t_den = ctk.CTkEntry(input_frame, width=150)
        self.entry_t_den.grid(row=0, column=1, padx=10, pady=10)

        ctk.CTkLabel(input_frame, text="断裂强度 (g/D):", font=ctk.CTkFont(size=14)).grid(row=1, column=0, padx=10,
                                                                                          pady=10, sticky="e")
        self.entry_t_str = ctk.CTkEntry(input_frame, width=150, placeholder_text="例如: 7.5")
        self.entry_t_str.grid(row=1, column=1, padx=10, pady=10)

        btn_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        btn_frame.pack(pady=20)
        ctk.CTkButton(btn_frame, text="计算拉力", font=ctk.CTkFont(size=15, weight="bold"), height=35,
                      command=self.calc_tensile).pack(side="left", padx=10)
        ctk.CTkButton(btn_frame, text="一键清空", font=ctk.CTkFont(size=15), height=35, fg_color="#7f8c8d",
                      hover_color="#95a5a6", command=self.clear_tensile_inputs).pack(side="left", padx=10)

        self.result_label_tensile = ctk.CTkLabel(self.main_frame, text="", font=ctk.CTkFont(size=18, weight="bold"))
        self.result_label_tensile.pack(pady=10)

    def calc_tensile(self):
        try:
            den = float(self.entry_t_den.get())
            strength = float(self.entry_t_str.get())
            if den <= 0 or strength <= 0: return
            self.result_label_tensile.configure(text=f"💪 该纱线可承受绝对拉力: {(den * strength) / 1000:.2f} kg",
                                                text_color="green")
        except ValueError:
            self.result_label_tensile.configure(text="输入错误！请确保填入的是数字。", text_color="red")

    def clear_tensile_inputs(self):
        self.entry_t_den.delete(0, 'end')
        self.entry_t_str.delete(0, 'end')
        self.result_label_tensile.configure(text="")

    # =======================================================
    # 【6号功能区】：纱线上油量计算
    # =======================================================
    def show_oil_frame(self):
        self.clear_main_frame()
        title = ctk.CTkLabel(self.main_frame, text="纱线需油量计算", font=ctk.CTkFont(size=20, weight="bold"))
        title.pack(pady=(20, 5))

        formula_text = (
            "⚙️ 计算公式推导：\n"
            "每分钟出丝重量 (g) = (第一冷辊速度 × 丹尼数) ÷ 9000\n"
            "需油量 (g/min) = 每分钟出丝重量 × 含油量%"
        )
        formula_label = ctk.CTkLabel(self.main_frame, text=formula_text, font=ctk.CTkFont(size=13, slant="italic"),
                                     text_color="gray", justify="left")
        formula_label.pack(pady=(0, 20))

        input_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        input_frame.pack(pady=5)

        ctk.CTkLabel(input_frame, text="第一冷辊速度 (m/min):", font=ctk.CTkFont(size=14)).grid(row=0, column=0,
                                                                                                padx=10, pady=10,
                                                                                                sticky="e")
        self.entry_o_speed = ctk.CTkEntry(input_frame, width=150, placeholder_text="例如: 2500")
        self.entry_o_speed.grid(row=0, column=1, padx=10, pady=10)

        ctk.CTkLabel(input_frame, text="纱线纤度 (Denier):", font=ctk.CTkFont(size=14)).grid(row=1, column=0, padx=10,
                                                                                             pady=10, sticky="e")
        self.entry_o_den = ctk.CTkEntry(input_frame, width=150, placeholder_text="例如: 900")
        self.entry_o_den.grid(row=1, column=1, padx=10, pady=10)

        ctk.CTkLabel(input_frame, text="目标含油量 (%):", font=ctk.CTkFont(size=14)).grid(row=2, column=0, padx=10,
                                                                                          pady=10, sticky="e")
        self.entry_o_pct = ctk.CTkEntry(input_frame, width=150, placeholder_text="例如: 2")
        self.entry_o_pct.grid(row=2, column=1, padx=10, pady=10)

        btn_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        btn_frame.pack(pady=20)
        ctk.CTkButton(btn_frame, text="计算需油量", font=ctk.CTkFont(size=15, weight="bold"), height=35,
                      command=self.calc_oil).pack(side="left", padx=10)
        ctk.CTkButton(btn_frame, text="一键清空", font=ctk.CTkFont(size=15), height=35, fg_color="#7f8c8d",
                      hover_color="#95a5a6", command=self.clear_oil_inputs).pack(side="left", padx=10)

        self.result_label_oil = ctk.CTkLabel(self.main_frame, text="", font=ctk.CTkFont(size=18, weight="bold"))
        self.result_label_oil.pack(pady=10)

    def calc_oil(self):
        try:
            speed = float(self.entry_o_speed.get())
            den = float(self.entry_o_den.get())
            pct = float(self.entry_o_pct.get())

            if speed <= 0 or den <= 0 or pct <= 0: return

            yarn_g_per_min = (speed * den) / 9000
            oil_req = yarn_g_per_min * (pct / 100)

            res_text = f"出丝速度: {yarn_g_per_min:.2f} g/min\n\n💧 目标需油量: {oil_req:.2f} g/min"
            self.result_label_oil.configure(text=res_text, text_color="green")
        except ValueError:
            self.result_label_oil.configure(text="输入错误！请确保填入的是数字。", text_color="red")

    def clear_oil_inputs(self):
        self.entry_o_speed.delete(0, 'end')
        self.entry_o_den.delete(0, 'end')
        self.entry_o_pct.delete(0, 'end')
        self.result_label_oil.configure(text="")

    # =======================================================
    # 【7号功能区】：纱线物性与对比
    # =======================================================
    def show_physical_frame(self):
        self.clear_main_frame()
        title = ctk.CTkLabel(self.main_frame, text="纱线物性与对比 (I值计算)", font=ctk.CTkFont(size=20, weight="bold"))
        title.pack(pady=(20, 5))

        formula_label = ctk.CTkLabel(self.main_frame, text="⚙️ 计算公式：I = √(深度/伸度 %) × 断裂强度(g/D)",
                                     font=ctk.CTkFont(size=14, slant="italic"), text_color="gray")
        formula_label.pack(pady=(0, 20))

        compare_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        compare_frame.pack(pady=5)

        ctk.CTkLabel(compare_frame, text="【样品 1】 (必填)", font=ctk.CTkFont(size=16, weight="bold")).grid(row=0,
                                                                                                           column=1,
                                                                                                           pady=10)
        ctk.CTkLabel(compare_frame, text="【样品 2】 (选填对比)", font=ctk.CTkFont(size=16, weight="bold")).grid(row=0,
                                                                                                               column=2,
                                                                                                               pady=10)

        ctk.CTkLabel(compare_frame, text="深度/伸度 (%):", font=ctk.CTkFont(size=14)).grid(row=1, column=0, padx=10,
                                                                                           pady=10, sticky="e")
        self.entry_phy_d1 = ctk.CTkEntry(compare_frame, width=130, placeholder_text="例: 25")
        self.entry_phy_d1.grid(row=1, column=1, padx=10, pady=10)
        self.entry_phy_d2 = ctk.CTkEntry(compare_frame, width=130, placeholder_text="可留空")
        self.entry_phy_d2.grid(row=1, column=2, padx=10, pady=10)

        ctk.CTkLabel(compare_frame, text="断裂强度 (g/D):", font=ctk.CTkFont(size=14)).grid(row=2, column=0, padx=10,
                                                                                            pady=10, sticky="e")
        self.entry_phy_s1 = ctk.CTkEntry(compare_frame, width=130, placeholder_text="例: 7.5")
        self.entry_phy_s1.grid(row=2, column=1, padx=10, pady=10)
        self.entry_phy_s2 = ctk.CTkEntry(compare_frame, width=130, placeholder_text="可留空")
        self.entry_phy_s2.grid(row=2, column=2, padx=10, pady=10)

        btn_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        btn_frame.pack(pady=20)
        ctk.CTkButton(btn_frame, text="开始对比计算", font=ctk.CTkFont(size=15, weight="bold"), height=35,
                      command=self.calc_physical).pack(side="left", padx=10)
        ctk.CTkButton(btn_frame, text="一键清空", font=ctk.CTkFont(size=15), height=35, fg_color="#7f8c8d",
                      hover_color="#95a5a6", command=self.clear_physical_inputs).pack(side="left", padx=10)

        self.result_label_phy = ctk.CTkLabel(self.main_frame, text="", font=ctk.CTkFont(size=16, weight="bold"))
        self.result_label_phy.pack(pady=10)

    def calc_physical(self):
        try:
            d1_str = self.entry_phy_d1.get().strip()
            s1_str = self.entry_phy_s1.get().strip()
            d2_str = self.entry_phy_d2.get().strip()
            s2_str = self.entry_phy_s2.get().strip()

            if not d1_str or not s1_str:
                self.result_label_phy.configure(text="❌ 样品 1 的参数必须填写完整！", text_color="red")
                return

            d1 = float(d1_str)
            s1 = float(s1_str)
            if d1 < 0: return

            I1 = math.sqrt(d1) * s1
            res_text = f"🔹 样品 1 物性值 (I): {I1:.2f}\n"

            if d2_str and s2_str:
                d2 = float(d2_str)
                s2 = float(s2_str)
                if d2 < 0: return

                I2 = math.sqrt(d2) * s2
                res_text += f"🔹 样品 2 物性值 (I): {I2:.2f}\n\n"

                if I1 > I2:
                    res_text += "🏆 比较结果:  样品 1  >  样品 2"
                elif I1 < I2:
                    res_text += "🏆 比较结果:  样品 1  <  样品 2"
                else:
                    res_text += "⚖️ 比较结果:  样品 1  =  样品 2"
            elif d2_str or s2_str:
                res_text += "\n(提示: 样品 2 数据未填全，已当作单列计算器使用)"

            self.result_label_phy.configure(text=res_text, text_color="green")
        except ValueError:
            self.result_label_phy.configure(text="输入格式错误！请确保填入的是纯数字。", text_color="red")

    def clear_physical_inputs(self):
        self.entry_phy_d1.delete(0, 'end')
        self.entry_phy_s1.delete(0, 'end')
        self.entry_phy_d2.delete(0, 'end')
        self.entry_phy_s2.delete(0, 'end')
        self.result_label_phy.configure(text="")

    # =======================================================
    # 【8号功能区】：挤出量与生产规格拆解 (机台配置版)
    # =======================================================
    def show_extrusion_frame(self):
        self.clear_main_frame()
        title = ctk.CTkLabel(self.main_frame, text="挤出量与生产规格拆解 (机台联动)",
                             font=ctk.CTkFont(size=20, weight="bold"))
        title.pack(pady=(10, 5))

        # --- 预置机台数据表 (格式为 机台号: (泵孔数, 单孔ml数)) ---
        self.machine_data = {
            "1号机": (2, 6.0), "2号机": (2, 6.0), "3号机": (2, 6.0), "4号机": (2, 6.0),
            "5号机": (4, 8.0), "6号机": (4, 8.0), "7号机": (4, 8.0), "8号机": (4, 8.0),
            "9号机": (3, 11.0), "10号机": (3, 11.0),
            "11号机": (2, 6.0), "12号机": (2, 6.0),
            "13号机": (4, 5.5), "14号机": (4, 5.5),
            "15号机": (2, 6.0)
        }

        # --- 变量绑定区 ---
        self.var_machine = ctk.StringVar(value="1号机")
        self.var_pump_holes = ctk.StringVar(value="2")
        self.var_pump_ml = ctk.StringVar(value="6.0")

        self.var_rpm = ctk.StringVar()
        self.var_den = ctk.StringVar(value="1.2")
        self.var_ext = ctk.StringVar(value="")  # 第一步结果：挤出量

        self.var_speed = ctk.StringVar()
        self.var_tot_den = ctk.StringVar(value="")  # 第二步结果：总丹尼

        self.var_holes = ctk.StringVar()
        self.var_target_den = ctk.StringVar()  # 辅助变量：单股目标丹尼

        # 绑定实时监听 (只要其中一个数变了，下面的所有框全自动重算)
        for var in [self.var_pump_holes, self.var_pump_ml, self.var_rpm, self.var_den, self.var_speed, self.var_holes,
                    self.var_target_den]:
            var.trace_add("write", self.calc_step_by_step)

        # --- 第一部分：挤出量计算 ---
        frame1 = ctk.CTkFrame(self.main_frame, corner_radius=8)
        frame1.pack(fill="x", padx=20, pady=5)
        ctk.CTkLabel(frame1, text="【第一步】挤出量计算", font=ctk.CTkFont(size=15, weight="bold"),
                     text_color="#3498db").grid(row=0, column=0, columnspan=4, pady=5, sticky="w", padx=10)

        ctk.CTkLabel(frame1, text="选择机台号:").grid(row=1, column=0, padx=10, pady=5, sticky="e")
        self.combo_mach = ctk.CTkComboBox(frame1, values=list(self.machine_data.keys()), variable=self.var_machine,
                                          command=self.on_machine_change, width=120)
        self.combo_mach.grid(row=1, column=1, padx=10, pady=5)

        ctk.CTkLabel(frame1, text="计量泵规格:").grid(row=1, column=2, padx=10, pady=5, sticky="e")
        self.lbl_pump_spec = ctk.CTkLabel(frame1, text="2 孔  |  6.0 ml/孔", text_color="gray",
                                          font=ctk.CTkFont(weight="bold"))
        self.lbl_pump_spec.grid(row=1, column=3, padx=10, pady=5, sticky="w")

        ctk.CTkLabel(frame1, text="计量泵转速 (rpm):").grid(row=2, column=0, padx=10, pady=5, sticky="e")
        ctk.CTkEntry(frame1, width=120, textvariable=self.var_rpm).grid(row=2, column=1, padx=10, pady=5)

        ctk.CTkLabel(frame1, text="熔体密度 (g/cm³):").grid(row=2, column=2, padx=10, pady=5, sticky="e")
        ctk.CTkEntry(frame1, width=120, textvariable=self.var_den).grid(row=2, column=3, padx=10, pady=5, sticky="w")

        self.lbl_res1 = ctk.CTkLabel(frame1, text="挤出量: 0.00 g/min", font=ctk.CTkFont(size=15, weight="bold"),
                                     text_color="green")
        self.lbl_res1.grid(row=3, column=1, columnspan=3, padx=10, pady=5, sticky="w")

        # --- 第二部分：总丹尼计算 ---
        frame2 = ctk.CTkFrame(self.main_frame, corner_radius=8)
        frame2.pack(fill="x", padx=20, pady=5)
        ctk.CTkLabel(frame2, text="【第二步】总丹尼计算", font=ctk.CTkFont(size=15, weight="bold"),
                     text_color="#3498db").grid(row=0, column=0, columnspan=4, pady=5, sticky="w", padx=10)

        ctk.CTkLabel(frame2, text="总挤出量 (自动引入):").grid(row=1, column=0, padx=10, pady=5, sticky="e")
        ctk.CTkEntry(frame2, width=120, textvariable=self.var_ext, state="readonly", fg_color="#e0e0e0",
                     text_color="black").grid(row=1, column=1, padx=10, pady=5)

        ctk.CTkLabel(frame2, text="卷绕速度 (m/min):").grid(row=1, column=2, padx=10, pady=5, sticky="e")
        ctk.CTkEntry(frame2, width=120, textvariable=self.var_speed).grid(row=1, column=3, padx=10, pady=5)

        self.lbl_res2 = ctk.CTkLabel(frame2, text="总丹尼: 0.00 D", font=ctk.CTkFont(size=15, weight="bold"),
                                     text_color="green")
        self.lbl_res2.grid(row=2, column=1, columnspan=3, padx=10, pady=5, sticky="w")

        # --- 第三部分：喷丝板与股数计算 ---
        frame3 = ctk.CTkFrame(self.main_frame, corner_radius=8)
        frame3.pack(fill="x", padx=20, pady=5)
        ctk.CTkLabel(frame3, text="【第三步】单纤分配与产出股数", font=ctk.CTkFont(size=15, weight="bold"),
                     text_color="#3498db").grid(row=0, column=0, columnspan=4, pady=5, sticky="w", padx=10)

        ctk.CTkLabel(frame3, text="总丹尼 (自动引入):").grid(row=1, column=0, padx=10, pady=5, sticky="e")
        ctk.CTkEntry(frame3, width=120, textvariable=self.var_tot_den, state="readonly", fg_color="#e0e0e0",
                     text_color="black").grid(row=1, column=1, padx=10, pady=5)

        ctk.CTkLabel(frame3, text="喷丝板总孔数 (F):").grid(row=1, column=2, padx=10, pady=5, sticky="e")
        ctk.CTkEntry(frame3, width=120, textvariable=self.var_holes).grid(row=1, column=3, padx=10, pady=5)

        ctk.CTkLabel(frame3, text="单股目标丹尼 (D):").grid(row=2, column=0, padx=10, pady=5, sticky="e")
        ctk.CTkEntry(frame3, width=120, textvariable=self.var_target_den, placeholder_text="填入用于算股数").grid(row=2,
                                                                                                                  column=1,
                                                                                                                  padx=10,
                                                                                                                  pady=5)

        self.lbl_res3 = ctk.CTkLabel(frame3, text="等待输入参数...", font=ctk.CTkFont(size=14, weight="bold"),
                                     text_color="gray", justify="left")
        self.lbl_res3.grid(row=3, column=0, columnspan=4, padx=20, pady=10, sticky="w")

        # 一键清空按钮
        ctk.CTkButton(self.main_frame, text="一键清空参数", font=ctk.CTkFont(size=14), height=30, fg_color="#7f8c8d",
                      hover_color="#95a5a6", command=self.clear_extrusion_inputs).pack(pady=10)

    # --- 独家事件与联动计算逻辑 ---
    def on_machine_change(self, choice):
        if choice in self.machine_data:
            h, m = self.machine_data[choice]
            self.lbl_pump_spec.configure(text=f"{h} 孔  |  {m} ml/孔")
            self.var_pump_holes.set(str(h))
            self.var_pump_ml.set(str(m))

    def calc_step_by_step(self, *args):
        # 1. 第一步：算总挤出量 (孔数 * ml * rpm * density)
        ext_val = 0.0
        try:
            h, m = float(self.var_pump_holes.get()), float(self.var_pump_ml.get())
            r, d = float(self.var_rpm.get()), float(self.var_den.get())
            ext_val = h * m * r * d
            self.var_ext.set(f"{ext_val:.2f}")
            self.lbl_res1.configure(text=f"挤出量: {ext_val:.2f} g/min", text_color="green")
        except ValueError:
            self.var_ext.set("")
            self.lbl_res1.configure(text="挤出量: 等待输入参数", text_color="gray")

        # 2. 第二步：算总丹尼
        tot_den_val = 0.0
        try:
            s = float(self.var_speed.get())
            if s > 0 and ext_val > 0:
                tot_den_val = (ext_val * 9000) / s
                self.var_tot_den.set(f"{tot_den_val:.2f}")
                self.lbl_res2.configure(text=f"总丹尼: {tot_den_val:.2f} D", text_color="green")
            else:
                self.var_tot_den.set("")
                self.lbl_res2.configure(text="总丹尼: 卷绕速度不能为0", text_color="red")
        except ValueError:
            self.var_tot_den.set("")
            self.lbl_res2.configure(text="总丹尼: 等待输入速度", text_color="gray")

        # 3. 第三步：算单纤丹尼和可产出股数
        try:
            holes_F = float(self.var_holes.get())
            res3_text = ""
            if holes_F > 0 and tot_den_val > 0:
                dpf = tot_den_val / holes_F
                res3_text += f"✅ 单纤丹尼 (DPF): {dpf:.2f}\n"

                # 计算能分多少股纱线
                try:
                    tden = float(self.var_target_den.get())
                    if tden > 0:
                        strands = tot_den_val / tden
                        res3_text += f"✅ 可产出股数: {strands:.2f} 股 (按 {tden}D/股 计算)"
                except ValueError:
                    res3_text += "💡 (在左侧输入单股目标丹尼，即可自动算出能出几股)"

                self.lbl_res3.configure(text=res3_text, text_color="green")
            else:
                self.lbl_res3.configure(text="等待输入有效喷丝板孔数...", text_color="gray")
        except ValueError:
            self.lbl_res3.configure(text="等待输入喷丝板参数...", text_color="gray")

    def clear_extrusion_inputs(self):
        self.var_machine.set("1号机")
        self.on_machine_change("1号机")
        self.var_rpm.set("")
        self.var_den.set("1.2")
        self.var_speed.set("")
        self.var_holes.set("")
        self.var_target_den.set("")

    # =======================================================
    # 【9号功能区】：频闪仪转速与线速度双向换算
    # =======================================================
    def show_strobe_frame(self):
        self.clear_main_frame()
        title = ctk.CTkLabel(self.main_frame, text="频闪仪转速与线速度双向换算",
                             font=ctk.CTkFont(size=20, weight="bold"))
        title.pack(pady=(20, 5))

        formula_text = (
            "⚙️ 计算公式：\n"
            "线速度(m/min) = 转速(RPM) × π × 辊筒直径(mm) ÷ 1000\n"
            "转速(RPM) = (线速度(m/min) × 1000) ÷ (π × 辊筒直径(mm))\n"
            "💡 提示：必填辊筒直径。然后在 转速/线速度 中【填入1个，留空1个】"
        )
        formula_label = ctk.CTkLabel(self.main_frame, text=formula_text, font=ctk.CTkFont(size=13, slant="italic"),
                                     text_color="gray", justify="left")
        formula_label.pack(pady=(0, 20))

        # 换算卡片区域
        input_frame = ctk.CTkFrame(self.main_frame, corner_radius=10)
        input_frame.pack(fill="x", padx=40, pady=10)

        # 1. 必填：辊筒直径
        ctk.CTkLabel(input_frame, text="测试辊筒直径 (mm):", font=ctk.CTkFont(size=14, weight="bold")).grid(row=0,
                                                                                                            column=0,
                                                                                                            padx=10,
                                                                                                            pady=15,
                                                                                                            sticky="e")
        self.entry_strobe_dia = ctk.CTkEntry(input_frame, width=150, placeholder_text="必填, 例: 190")
        self.entry_strobe_dia.grid(row=0, column=1, padx=10, pady=15)

        # 2. 选填：频闪仪转速
        ctk.CTkLabel(input_frame, text="频闪仪转速 (RPM):", font=ctk.CTkFont(size=14)).grid(row=1, column=0, padx=10,
                                                                                            pady=10, sticky="e")
        self.entry_strobe_rpm = ctk.CTkEntry(input_frame, width=150, placeholder_text="留空或输入")
        self.entry_strobe_rpm.grid(row=1, column=1, padx=10, pady=10)

        # 3. 选填：线速度
        ctk.CTkLabel(input_frame, text="线速度 (m/min):", font=ctk.CTkFont(size=14)).grid(row=2, column=0, padx=10,
                                                                                          pady=10, sticky="e")
        self.entry_strobe_speed = ctk.CTkEntry(input_frame, width=150, placeholder_text="留空或输入")
        self.entry_strobe_speed.grid(row=2, column=1, padx=10, pady=10)

        # 按钮组 (放在右侧)
        btn_frame = ctk.CTkFrame(input_frame, fg_color="transparent")
        btn_frame.grid(row=0, column=2, rowspan=3, padx=30)
        ctk.CTkButton(btn_frame, text="智能联动换算", font=ctk.CTkFont(size=14, weight="bold"), height=35,
                      command=self.calc_strobe).pack(pady=10)
        ctk.CTkButton(btn_frame, text="一键清空", font=ctk.CTkFont(size=14), height=35, fg_color="#7f8c8d",
                      hover_color="#95a5a6", command=self.clear_strobe_inputs).pack(pady=5)

        # 结果展示
        self.result_label_strobe = ctk.CTkLabel(self.main_frame, text="", font=ctk.CTkFont(size=16, weight="bold"))
        self.result_label_strobe.pack(pady=20)

    def calc_strobe(self):
        try:
            dia_mm = float(self.entry_strobe_dia.get())
            if dia_mm <= 0:
                self.result_label_strobe.configure(text="❌ 错误：辊筒直径必须大于 0！", text_color="red")
                return

            rpm_str = self.entry_strobe_rpm.get().strip()
            speed_str = self.entry_strobe_speed.get().strip()

            filled_count = sum([1 for x in [rpm_str, speed_str] if x != ""])

            if filled_count != 1:
                self.result_label_strobe.configure(text="❌ 错误：在 转速 和 线速度 中，只能填写【其中1个】！",
                                                   text_color="red")
                return

            # π 取近似值即可，使用 math.pi
            if rpm_str:  # 已知 RPM，求 m/min
                rpm = float(rpm_str)
                speed = (rpm * math.pi * dia_mm) / 1000
                self.entry_strobe_speed.delete(0, 'end')
                self.entry_strobe_speed.insert(0, f"{speed:.2f}")
                self.result_label_strobe.configure(text=f"✅ 计算完成！对应线速度: {speed:.2f} m/min", text_color="green")

            elif speed_str:  # 已知 m/min，求 RPM
                speed = float(speed_str)
                rpm = (speed * 1000) / (math.pi * dia_mm)
                self.entry_strobe_rpm.delete(0, 'end')
                # 频闪仪转速通常看整数，这里保留0位小数
                self.entry_strobe_rpm.insert(0, f"{rpm:.0f}")
                self.result_label_strobe.configure(text=f"✅ 计算完成！对应频闪仪转速: {rpm:.0f} RPM", text_color="green")

        except ValueError:
            self.result_label_strobe.configure(text="输入格式错误！请确保填入的是纯数字。", text_color="red")

    def clear_strobe_inputs(self):
        self.entry_strobe_dia.delete(0, 'end')
        self.entry_strobe_rpm.delete(0, 'end')
        self.entry_strobe_speed.delete(0, 'end')
        self.result_label_strobe.configure(text="")

if __name__ == "__main__":
    app = FiberCalculatorApp()
    app.mainloop()