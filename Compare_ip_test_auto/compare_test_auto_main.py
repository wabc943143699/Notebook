import pandas as pd
import time
import subprocess
# 下面是自定义函数
from compare_tcl_generate import ip_param_setting
from compare_tcl_generate import ip_generate
from compare_tcl_generate import tcl_generate
from Powershell_control_auto import powershell_work_auto


start_time = time.time()
# 先读取存放inst case的Excel表
Excel_path = r"D:/Code/vivado/script_tcl/compare_inst.xlsx"
Excel = pd.read_excel(Excel_path, engine='openpyxl')

inst_num = 2
# 项目根目录
project_root_dir = r"D:/Code/vivado/compare_test"

for current_inst_num in range(inst_num):

    # 项目名
    project_name = "inst" + f"{current_inst_num+1}"
    print("\n"+project_name)
    # 项目路径
    project_dir = project_root_dir + "/" + project_name

    # print(project_dir)
    # filelist 指的是 rtl_list.tcl的路径
    filelist = project_dir + "/rtl_list.tcl"
    # print(filelist)
    # 源文件顶层名称
    source_top_module = "top"
    # 仿真文件顶层文件名称
    tb_top_module = "tb"
    # 设置IP核路径
    ip_dir = project_dir

    # ip核参数配置
    row_index = current_inst_num
    param_setting = ip_param_setting(op_mode = Excel.at[row_index, "op_mode"], is_blocking = Excel.at[row_index, "is_blocking"], latency = int(Excel.at[row_index, "latency"]), 
                                     aclken_vld = Excel.at[row_index, "aclken_vld"], aresetn_vld = Excel.at[row_index, "aresetn_vld"], invalid_op = Excel.at[row_index, "invalid_op"], 
                                     Has_A_TLAST = Excel.at[row_index, "Has_A_TLAST"], Has_A_TUSER = Excel.at[row_index, "Has_A_TUSER"], Has_B_TLAST = Excel.at[row_index, "Has_B_TLAST"], 
                                     Has_B_TUSER = Excel.at[row_index, "Has_B_TUSER"], Has_OPERATION_TLAST = Excel.at[row_index, "Has_OPERATION_TLAST"], Has_OPERATION_TUSER = Excel.at[row_index, "Has_OPERATION_TUSER"], 
                                     Precision_Type = Excel.at[row_index, "Precision_Type"], Exp_width = int(Excel.at[row_index, "Exp_width"]), Fra_width = int(Excel.at[row_index, "Fra_width"]), 
                                     Axi_Optimize_Goal = Excel.at[row_index, "Axi_Optimize_Goal"], Has_RESULT_TREADY = Excel.at[row_index, "Has_RESULT_TREADY"], Result_Exponent_Width = int(Excel.at[row_index, "Result_Exponent_Width"]))
    
    create_ip = ip_generate(ip_dir, project_dir, param_setting)
    # 生成run.tcl脚本文件
    tcl_generate(project_name, project_dir, filelist, source_top_module, tb_top_module, create_ip)

    # 调用Powershell运行vivado tcl脚本文件
    powershell_work_auto(working_directory = project_dir, command = "vivado -mode batch -source run.tcl")



end_time = time.time()
print(f"运行时间{end_time-start_time}秒")



