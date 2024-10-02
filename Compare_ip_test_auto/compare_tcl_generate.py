# # 设置项目名称
# project_name = "my_project"

# # 设置项目路径 (绝对路径)
# project_dir = r"D:/Code/vivado/script_tcl/my_project_dir"

# # 设置RTL文件路径
# filelist = r"D:/Code/vivado/script_tcl/rtl_list.tcl"

# # 设置源文件顶层文件名称
# source_top_module = "top"
# # 设置仿真文件顶层文件名称
# tb_top_module = "top"
# # 设置IP核路径
# ip_dir = f"{project_dir}/my_project.srcs/sources_1/ip"


# 生成TCL脚本
def tcl_generate(project_name, project_dir, filelist, source_top_module, tb_top_module, create_ip):

    tcl_script = f"""
    set project_name "{project_name}"

    set project_dir "{project_dir}"

    set filelist "{filelist}"

    create_project $project_name $project_dir -part xc7k325tffg676-3 -force

    source $filelist

    set_property top {source_top_module} [current_fileset]

    {create_ip}

    reset_run synth_1
    reset_run impl_1

    launch_runs synth_1
    wait_on_run synth_1

    open_run synth_1 -name synth_1
    opt_design
    report_utilization -file "${{project_dir}}/${{project_name}}_utilization_synth_summary.rpt"
    puts "Synthesis utilization summary report generated."

    launch_runs impl_1
    wait_on_run impl_1
    open_run impl_1 -name impl_1
    report_utilization -file "${{project_dir}}/${{project_name}}_utilization_impl_summary.rpt"
    puts "Implementation utilization summary report generated."

    set_property top {tb_top_module} [get_filesets sim_1]

    set_property target_simulator "XSim" [current_project]

    launch_simulation
    restart
    run all

    close_sim
    close_project
    """

    # 将TCL脚本写入文件
    with open(project_dir + "/run.tcl", "w") as tcl_file:
        tcl_file.write(tcl_script)

    print(f"TCL script has been written to {project_dir}/run.tcl")




def ip_generate(ip_dir, project_dir, param_setting):

    create_ip = f"""
    create_ip \\
        -name floating_point \\
        -vendor xilinx.com \\
        -library ip \\
        -version 7.1 \\
        -module_name floating_point_0 \\
        -dir "{ip_dir}"
    
    {param_setting}
    

    generate_target {{instantiation_template}} [get_files "{ip_dir}/floating_point_0/floating_point_0.xci"]
    generate_target all [get_files  "{ip_dir}/floating_point_0/floating_point_0.xci"]
    catch {{ config_ip_cache -export [get_ips -all floating_point_0] }}
    export_ip_user_files \\
        -of_objects [get_files "{ip_dir}/floating_point_0/floating_point_0.xci"] \\
        -no_script \\
        -sync \\
        -force \\
        -quiet

    create_ip_run [get_files -of_objects [get_fileset sources_1] "{ip_dir}/floating_point_0/floating_point_0.xci"]
    launch_runs -jobs 16 floating_point_0_synth_1
    export_simulation \\
        -of_objects [get_files "{ip_dir}/floating_point_0/floating_point_0.xci"] \\
        -directory "{project_dir}/my_project.ip_user_files/sim_scripts" \\
        -ip_user_files_dir "{project_dir}/my_project.ip_user_files" \\
        -ipstatic_source_dir "{project_dir}/my_project.ip_user_files/ipstatic" \\
        -lib_map_path [list \\
            {{modelsim="{project_dir}/my_project.cache/compile_simlib/modelsim"}} \\
            {{questa="{project_dir}/my_project.cache/compile_simlib/questa"}} \\
            {{riviera="{project_dir}/my_project.cache/compile_simlib/riviera"}} \\
            {{activehdl="{project_dir}/my_project.cache/compile_simlib/activehdl"}} \\
        ] \\
        -use_ip_compiled_libs \\
        -force \\
        -quiet

    """
    return create_ip

def ip_param_setting(op_mode, is_blocking, latency = 2, aclken_vld = "true", aresetn_vld = "true", invalid_op = "true", Has_A_TLAST = "true", Has_A_TUSER = "true", 
                     Has_B_TLAST = "true", Has_B_TUSER = "true", Has_OPERATION_TLAST = "true", Has_OPERATION_TUSER = "true", Precision_Type = "Single", Exp_width = 8, Fra_width = 24, 
                     Axi_Optimize_Goal = "Performance", Has_RESULT_TREADY = "true", Result_Exponent_Width = 1):
    if(op_mode == "Programmable"):
        if(is_blocking == "nonblocking"):
            if(latency > 0):
                param_setting = f"""

                set_property \\
                    -dict [list \\
                        CONFIG.Operation_Type {{Compare}} \\
                        CONFIG.Flow_Control {{NonBlocking}} \\
                        CONFIG.Maximum_Latency {{false}} \\
                        CONFIG.Has_ACLKEN {{{aclken_vld}}} \\
                        CONFIG.Has_ARESETn {{{aresetn_vld}}} \\
                        CONFIG.C_Has_INVALID_OP {{{invalid_op}}} \\
                        CONFIG.Has_A_TLAST {{{Has_A_TLAST}}} \\
                        CONFIG.Has_A_TUSER {{{Has_A_TUSER}}} \\
                        CONFIG.Has_B_TLAST {{{Has_B_TLAST}}} \\
                        CONFIG.Has_B_TUSER {{{Has_B_TUSER}}} \\
                        CONFIG.Has_OPERATION_TLAST {{{Has_OPERATION_TLAST}}} \\
                        CONFIG.Has_OPERATION_TUSER {{{Has_OPERATION_TUSER}}} \\
                        CONFIG.A_Precision_Type {{{Precision_Type}}} \\
                        CONFIG.C_A_Exponent_Width {{{Exp_width}}} \\
                        CONFIG.C_A_Fraction_Width {{{Fra_width}}} \\
                        CONFIG.Result_Precision_Type {{Custom}} \\
                        CONFIG.C_Result_Exponent_Width {{1}} \\
                        CONFIG.C_Result_Fraction_Width {{0}} \\
                        CONFIG.C_Mult_Usage {{No_Usage}} \\
                        CONFIG.Has_RESULT_TREADY {{false}} \\
                        CONFIG.C_Latency {{{latency}}} \\
                        CONFIG.C_Rate {{1}} \\
                        CONFIG.RESULT_TLAST_Behv {{Pass_A_TLAST}} \\
                    ] \\
                    [get_ips floating_point_0]

                """
            else:
                param_setting = f"""

                set_property -dict [list \\
                    CONFIG.Operation_Type {{Compare}} \\
                    CONFIG.Flow_Control {{NonBlocking}} \\
                    CONFIG.Maximum_Latency {{false}} \\
                    CONFIG.C_Latency {{{latency}}} \\
                    CONFIG.C_Has_INVALID_OP {{{invalid_op}}} \\
                    CONFIG.Has_A_TLAST {{{Has_A_TLAST}}} \\
                    CONFIG.Has_A_TUSER {{{Has_A_TUSER}}} \\
                    CONFIG.Has_B_TLAST {{{Has_B_TLAST}}} \\
                    CONFIG.Has_B_TUSER {{{Has_B_TUSER}}} \\
                    CONFIG.Has_OPERATION_TLAST {{{Has_OPERATION_TLAST}}} \\
                    CONFIG.Has_OPERATION_TUSER {{{Has_OPERATION_TUSER}}} \\
                    CONFIG.A_Precision_Type {{{Precision_Type}}} \\
                    CONFIG.C_A_Exponent_Width {{{Exp_width}}} \\
                    CONFIG.C_A_Fraction_Width {{{Fra_width}}} \\
                    CONFIG.Result_Precision_Type {{Custom}} \\
                    CONFIG.C_Result_Exponent_Width {{1}} \\
                    CONFIG.C_Result_Fraction_Width {{0}} \\
                    CONFIG.C_Mult_Usage {{No_Usage}} \\
                    CONFIG.Has_RESULT_TREADY {{false}} \\
                    CONFIG.C_Rate {{1}} \\
                    CONFIG.RESULT_TLAST_Behv {{Pass_A_TLAST}}] [get_ips floating_point_0]

                """
        elif(is_blocking == "blocking"):
            if(latency > 0):
                param_setting = f"""

                set_property -dict [list \\
                    CONFIG.Operation_Type {{Compare}} \\
                    CONFIG.Flow_Control {{Blocking}} \\
                    CONFIG.Axi_Optimize_Goal {{{Axi_Optimize_Goal}}} \\
                    CONFIG.Maximum_Latency {{false}} \\
                    CONFIG.Has_ACLKEN {{{aclken_vld}}} \\
                    CONFIG.Has_ARESETn {{{aresetn_vld}}} \\
                    CONFIG.C_Has_INVALID_OP {{{invalid_op}}} \\
                    CONFIG.Has_A_TLAST {{{Has_A_TLAST}}} \\
                    CONFIG.Has_A_TUSER {{{Has_A_TUSER}}} \\
                    CONFIG.Has_B_TLAST {{{Has_B_TLAST}}} \\
                    CONFIG.Has_B_TUSER {{{Has_B_TUSER}}} \\
                    CONFIG.Has_OPERATION_TLAST {{{Has_OPERATION_TLAST}}} \\
                    CONFIG.Has_OPERATION_TUSER {{{Has_OPERATION_TUSER}}} \\
                    CONFIG.A_Precision_Type {{{Precision_Type}}} \\
                    CONFIG.C_A_Exponent_Width {{{Exp_width}}} \\
                    CONFIG.C_A_Fraction_Width {{{Fra_width}}} \\
                    CONFIG.Result_Precision_Type {{Custom}} \\
                    CONFIG.C_Result_Exponent_Width {{1}} \\
                    CONFIG.C_Result_Fraction_Width {{0}} \\
                    CONFIG.C_Mult_Usage {{No_Usage}} \\
                    CONFIG.Has_RESULT_TREADY {{{Has_RESULT_TREADY}}} \\
                    CONFIG.C_Latency {{{latency}}} \\
                    CONFIG.C_Rate {{1}} \\
                    CONFIG.RESULT_TLAST_Behv {{Pass_A_TLAST}}] [get_ips floating_point_0]

                """
    elif(op_mode == "Greater_Than" or op_mode == "Less_Than" or op_mode == "Greater_Than_Or_Equal" or op_mode == "Less_Than_Or_Equal"):
        if(is_blocking == "nonblocking"):
            if(latency > 0):
                param_setting = f"""

                set_property -dict [list \\
                    CONFIG.Operation_Type {{Compare}} \\
                    CONFIG.C_Compare_Operation {{{op_mode}}} \\
                    CONFIG.Flow_Control {{NonBlocking}} \\
                    CONFIG.Maximum_Latency {{false}} \\
                    CONFIG.Has_ACLKEN {{{aclken_vld}}} \\
                    CONFIG.Has_ARESETn {{{aresetn_vld}}} \\
                    CONFIG.C_Has_INVALID_OP {{{invalid_op}}} \\
                    CONFIG.Has_A_TLAST {{{Has_A_TLAST}}} \\
                    CONFIG.Has_A_TUSER {{{Has_A_TUSER}}} \\
                    CONFIG.Has_B_TLAST {{{Has_B_TLAST}}} \\
                    CONFIG.Has_B_TUSER {{{Has_B_TUSER}}} \\
                    CONFIG.A_Precision_Type {{{Precision_Type}}} \\
                    CONFIG.C_A_Exponent_Width {{{Exp_width}}} \\
                    CONFIG.C_A_Fraction_Width {{{Fra_width}}} \\
                    CONFIG.Result_Precision_Type {{Custom}} \\
                    CONFIG.C_Result_Exponent_Width {{1}} \\
                    CONFIG.C_Result_Fraction_Width {{0}} \\
                    CONFIG.C_Mult_Usage {{No_Usage}} \\
                    CONFIG.Has_RESULT_TREADY {{false}} \\
                    CONFIG.C_Latency {{{latency}}} \\
                    CONFIG.C_Rate {{1}} \\
                    CONFIG.RESULT_TLAST_Behv {{Pass_A_TLAST}}] [get_ips floating_point_0]

                """
            else:
                param_setting = f"""

                set_property -dict [list \\
                    CONFIG.Operation_Type {{Compare}} \\
                    CONFIG.C_Compare_Operation {{{op_mode}}} \\
                    CONFIG.Flow_Control {{NonBlocking}} \\
                    CONFIG.Maximum_Latency {{false}} \\
                    CONFIG.C_Has_INVALID_OP {{{invalid_op}}} \\
                    CONFIG.Has_A_TLAST {{{Has_A_TLAST}}} \\
                    CONFIG.Has_A_TUSER {{{Has_A_TUSER}}} \\
                    CONFIG.Has_B_TLAST {{{Has_B_TLAST}}} \\
                    CONFIG.Has_B_TUSER {{{Has_B_TUSER}}} \\
                    CONFIG.A_Precision_Type {{{Precision_Type}}} \\
                    CONFIG.C_A_Exponent_Width {{{Exp_width}}} \\
                    CONFIG.C_A_Fraction_Width {{{Fra_width}}} \\
                    CONFIG.Result_Precision_Type {{Custom}} \\
                    CONFIG.C_Result_Exponent_Width {{1}} \\
                    CONFIG.C_Result_Fraction_Width {{0}} \\
                    CONFIG.C_Mult_Usage {{No_Usage}} \\
                    CONFIG.Has_RESULT_TREADY {{false}} \\
                    CONFIG.C_Latency {{{latency}}} \\
                    CONFIG.C_Rate {{1}} \\
                    CONFIG.RESULT_TLAST_Behv {{Pass_A_TLAST}}] [get_ips floating_point_0]

                """
        elif(is_blocking == "blocking"):
            if(Has_RESULT_TREADY == "true"):
                if(latency > 3):
                    param_setting = f"""

                    set_property -dict [list \\
                        CONFIG.Operation_Type {{Compare}} \\
                        CONFIG.C_Compare_Operation {{{op_mode}}} \\
                        CONFIG.A_Precision_Type {{{Precision_Type}}} \\
                        CONFIG.Axi_Optimize_Goal {{Performance}} \\
                        CONFIG.Maximum_Latency {{false}} \\
                        CONFIG.C_Latency {{{latency}}} \\
                        CONFIG.Has_ACLKEN {{{aclken_vld}}} \\
                        CONFIG.Has_ARESETn {{{aresetn_vld}}} \\
                        CONFIG.C_Has_INVALID_OP {{{invalid_op}}} \\
                        CONFIG.Has_A_TLAST {{{Has_A_TLAST}}} \\
                        CONFIG.Has_A_TUSER {{{Has_A_TUSER}}} \\
                        CONFIG.Has_B_TLAST {{{Has_B_TLAST}}} \\
                        CONFIG.Has_B_TUSER {{{Has_B_TUSER}}} \\
                        CONFIG.C_A_Exponent_Width {{{Exp_width}}} \\
                        CONFIG.C_A_Fraction_Width {{{Fra_width}}} \\
                        CONFIG.Result_Precision_Type {{Custom}} \\
                        CONFIG.C_Result_Exponent_Width {{1}} \\
                        CONFIG.C_Result_Fraction_Width {{0}} \\
                        CONFIG.C_Accum_Msb {{32}} \\
                        CONFIG.C_Accum_Lsb {{-31}} \\
                        CONFIG.C_Accum_Input_Msb {{32}} \\
                        CONFIG.C_Mult_Usage {{No_Usage}} \\
                        CONFIG.C_Rate {{1}} \\
                        CONFIG.RESULT_TLAST_Behv {{Pass_A_TLAST}}] [get_ips floating_point_0]

                    """
                elif(latency == 3):
                    param_setting = f"""

                    set_property -dict [list \\
                        CONFIG.Operation_Type {{Compare}} \\
                        CONFIG.C_Compare_Operation {{{op_mode}}} \\
                        CONFIG.Axi_Optimize_Goal {{Performance}} \\
                        CONFIG.Maximum_Latency {{false}} \\
                        CONFIG.C_Latency {{{latency}}} \\
                        CONFIG.Has_ACLKEN {{{aclken_vld}}} \\
                        CONFIG.Has_ARESETn {{{aresetn_vld}}} \\
                        CONFIG.C_Has_INVALID_OP {{{invalid_op}}} \\
                        CONFIG.Has_A_TLAST {{{Has_A_TLAST}}} \\
                        CONFIG.Has_A_TUSER {{{Has_A_TUSER}}} \\
                        CONFIG.Has_B_TLAST {{{Has_B_TLAST}}} \\
                        CONFIG.Has_B_TUSER {{{Has_B_TUSER}}} \\
                        CONFIG.A_Precision_Type {{{Precision_Type}}} \\
                        CONFIG.C_A_Exponent_Width {{{Exp_width}}} \\
                        CONFIG.C_A_Fraction_Width {{{Fra_width}}} \\
                        CONFIG.Result_Precision_Type {{Custom}} \\
                        CONFIG.C_Result_Exponent_Width {{1}} \\
                        CONFIG.C_Result_Fraction_Width {{0}} \\
                        CONFIG.C_Mult_Usage {{No_Usage}} \\
                        CONFIG.C_Rate {{1}} \\
                        CONFIG.RESULT_TLAST_Behv {{Pass_A_TLAST}}] [get_ips floating_point_0]

                    """
            elif(Has_RESULT_TREADY == "false"):
                if(latency == 3):
                    param_setting = f"""

                    set_property -dict [list \\
                        CONFIG.Operation_Type {{Compare}} \\
                        CONFIG.C_Compare_Operation {{{op_mode}}} \\
                        CONFIG.Axi_Optimize_Goal {{Performance}} \\
                        CONFIG.Has_RESULT_TREADY {{false}} \\
                        CONFIG.Maximum_Latency {{false}} \\
                        CONFIG.Has_ACLKEN {{{aclken_vld}}} \\
                        CONFIG.Has_ARESETn {{{aresetn_vld}}} \\
                        CONFIG.C_Has_INVALID_OP {{{invalid_op}}} \\
                        CONFIG.Has_A_TLAST {{{Has_A_TLAST}}} \\
                        CONFIG.Has_A_TUSER {{{Has_A_TUSER}}} \\
                        CONFIG.Has_B_TLAST {{{Has_B_TLAST}}} \\
                        CONFIG.Has_B_TUSER {{{Has_B_TUSER}}} \\
                        CONFIG.A_Precision_Type {{{Precision_Type}}} \\
                        CONFIG.C_A_Exponent_Width {{{Exp_width}}} \\
                        CONFIG.C_A_Fraction_Width {{{Fra_width}}} \\
                        CONFIG.Result_Precision_Type {{Custom}} \\
                        CONFIG.C_Result_Exponent_Width {{1}} \\
                        CONFIG.C_Result_Fraction_Width {{0}} \\
                        CONFIG.C_Mult_Usage {{No_Usage}} \\
                        CONFIG.C_Latency {{{latency}}} \\
                        CONFIG.C_Rate {{1}} \\
                        CONFIG.RESULT_TLAST_Behv {{Pass_A_TLAST}}] [get_ips floating_point_0]

                    """
                elif(latency < 3):
                    param_setting = f"""
                    set_property -dict [list \\
                        CONFIG.Operation_Type {{Compare}} \\
                        CONFIG.C_Compare_Operation {{{op_mode}}} \\
                        CONFIG.Axi_Optimize_Goal {{Performance}} \\
                        CONFIG.Has_RESULT_TREADY {{false}} \\
                        CONFIG.Maximum_Latency {{false}} \\
                        CONFIG.C_Latency {{{latency}}} \\
                        CONFIG.Has_ACLKEN {{{aclken_vld}}} \\
                        CONFIG.Has_ARESETn {{{aresetn_vld}}} \\
                        CONFIG.C_Has_INVALID_OP {{{invalid_op}}} \\
                        CONFIG.Has_A_TLAST {{{Has_A_TLAST}}} \\
                        CONFIG.Has_A_TUSER {{{Has_A_TUSER}}} \\
                        CONFIG.Has_B_TLAST {{{Has_B_TLAST}}} \\
                        CONFIG.Has_B_TUSER {{{Has_B_TUSER}}} \\
                        CONFIG.A_Precision_Type {{{Precision_Type}}} \\
                        CONFIG.C_A_Exponent_Width {{{Exp_width}}} \\
                        CONFIG.C_A_Fraction_Width {{{Fra_width}}} \\
                        CONFIG.Result_Precision_Type {{Custom}} \\
                        CONFIG.C_Result_Exponent_Width {{1}} \\
                        CONFIG.C_Result_Fraction_Width {{0}} \\
                        CONFIG.C_Mult_Usage {{No_Usage}} \\
                        CONFIG.C_Rate {{1}} \\
                        CONFIG.RESULT_TLAST_Behv {{Pass_A_TLAST}}] [get_ips floating_point_0]

                    """

    elif(op_mode == "Equal" or op_mode == "Not_Equal" or op_mode == "Unordered" or op_mode == "Condition_Code"):
        if(is_blocking == "nonblocking"):
            if(latency > 0):
                param_setting = f"""

                set_property -dict [list \\
                    CONFIG.Operation_Type {{Compare}} \\
                    CONFIG.C_Compare_Operation {{{op_mode}}} \\
                    CONFIG.Flow_Control {{NonBlocking}} \\
                    CONFIG.Maximum_Latency {{false}} \\
                    CONFIG.Has_ACLKEN {{{aclken_vld}}} \\
                    CONFIG.Has_ARESETn {{{aresetn_vld}}} \\
                    CONFIG.Has_A_TLAST {{{Has_A_TLAST}}} \\
                    CONFIG.Has_A_TUSER {{{Has_A_TUSER}}} \\
                    CONFIG.Has_B_TLAST {{{Has_B_TLAST}}} \\
                    CONFIG.Has_B_TUSER {{{Has_B_TUSER}}} \\
                    CONFIG.A_Precision_Type {{{Precision_Type}}} \\
                    CONFIG.C_A_Exponent_Width {{{Exp_width}}} \\
                    CONFIG.C_A_Fraction_Width {{{Fra_width}}} \\
                    CONFIG.Result_Precision_Type {{Custom}} \\
                    CONFIG.C_Result_Exponent_Width {{{Result_Exponent_Width}}} \\
                    CONFIG.C_Result_Fraction_Width {{0}} \\
                    CONFIG.C_Mult_Usage {{No_Usage}} \\
                    CONFIG.Has_RESULT_TREADY {{false}} \\
                    CONFIG.C_Latency {{{latency}}} \\
                    CONFIG.C_Rate {{1}} \\
                    CONFIG.RESULT_TLAST_Behv {{Pass_A_TLAST}}] [get_ips floating_point_0]

                """
            else:
                param_setting = f"""

                set_property -dict [list \\
                    CONFIG.Operation_Type {{Compare}} \\
                    CONFIG.C_Compare_Operation {{{op_mode}}} \\
                    CONFIG.Flow_Control {{NonBlocking}} \\
                    CONFIG.Maximum_Latency {{false}} \\
                    CONFIG.Has_A_TLAST {{{Has_A_TLAST}}} \\
                    CONFIG.Has_A_TUSER {{{Has_A_TUSER}}} \\
                    CONFIG.Has_B_TLAST {{{Has_B_TLAST}}} \\
                    CONFIG.Has_B_TUSER {{{Has_B_TUSER}}} \\
                    CONFIG.A_Precision_Type {{{Precision_Type}}} \\
                    CONFIG.C_A_Exponent_Width {{{Exp_width}}} \\
                    CONFIG.C_A_Fraction_Width {{{Fra_width}}} \\
                    CONFIG.Result_Precision_Type {{Custom}} \\
                    CONFIG.C_Result_Exponent_Width {{{Result_Exponent_Width}}} \\
                    CONFIG.C_Result_Fraction_Width {{0}} \\
                    CONFIG.C_Mult_Usage {{No_Usage}} \\
                    CONFIG.Has_RESULT_TREADY {{false}} \\
                    CONFIG.C_Latency {{{latency}}} \\
                    CONFIG.C_Rate {{1}} \\
                    CONFIG.RESULT_TLAST_Behv {{Pass_A_TLAST}}] [get_ips floating_point_0]

                """
        elif(is_blocking == "blocking"):
            if(Has_RESULT_TREADY == "true"):
                if(latency > 3):
                    param_setting = f"""

                    set_property -dict [list \\
                        CONFIG.Operation_Type {{Compare}} \\
                        CONFIG.C_Compare_Operation {{{op_mode}}} \\
                        CONFIG.A_Precision_Type {{{Precision_Type}}} \\
                        CONFIG.Axi_Optimize_Goal {{Performance}} \\
                        CONFIG.Maximum_Latency {{false}} \\
                        CONFIG.C_Latency {{{latency}}} \\
                        CONFIG.Has_ACLKEN {{{aclken_vld}}} \\
                        CONFIG.Has_ARESETn {{{aresetn_vld}}} \\
                        CONFIG.Has_A_TLAST {{{Has_A_TLAST}}} \\
                        CONFIG.Has_A_TUSER {{{Has_A_TUSER}}} \\
                        CONFIG.Has_B_TLAST {{{Has_B_TLAST}}} \\
                        CONFIG.Has_B_TUSER {{{Has_B_TUSER}}} \\
                        CONFIG.C_A_Exponent_Width {{{Exp_width}}} \\
                        CONFIG.C_A_Fraction_Width {{{Fra_width}}} \\
                        CONFIG.Result_Precision_Type {{Custom}} \\
                        CONFIG.C_Result_Exponent_Width {{{Result_Exponent_Width}}} \\
                        CONFIG.C_Result_Fraction_Width {{0}} \\
                        CONFIG.C_Accum_Msb {{32}} \\
                        CONFIG.C_Accum_Lsb {{-31}} \\
                        CONFIG.C_Accum_Input_Msb {{32}} \\
                        CONFIG.C_Mult_Usage {{No_Usage}} \\
                        CONFIG.C_Rate {{1}} \\
                        CONFIG.RESULT_TLAST_Behv {{Pass_A_TLAST}}] [get_ips floating_point_0]

                    """
                elif(latency == 3):
                    param_setting = f"""

                    set_property -dict [list \\
                        CONFIG.Operation_Type {{Compare}} \\
                        CONFIG.C_Compare_Operation {{{op_mode}}} \\
                        CONFIG.Axi_Optimize_Goal {{Performance}} \\
                        CONFIG.Maximum_Latency {{false}} \\
                        CONFIG.C_Latency {{{latency}}} \\
                        CONFIG.Has_ACLKEN {{{aclken_vld}}} \\
                        CONFIG.Has_ARESETn {{{aresetn_vld}}} \\
                        CONFIG.Has_A_TLAST {{{Has_A_TLAST}}} \\
                        CONFIG.Has_A_TUSER {{{Has_A_TUSER}}} \\
                        CONFIG.Has_B_TLAST {{{Has_B_TLAST}}} \\
                        CONFIG.Has_B_TUSER {{{Has_B_TUSER}}} \\
                        CONFIG.A_Precision_Type {{{Precision_Type}}} \\
                        CONFIG.C_A_Exponent_Width {{{Exp_width}}} \\
                        CONFIG.C_A_Fraction_Width {{{Fra_width}}} \\
                        CONFIG.Result_Precision_Type {{Custom}} \\
                        CONFIG.C_Result_Exponent_Width {{{Result_Exponent_Width}}} \\
                        CONFIG.C_Result_Fraction_Width {{0}} \\
                        CONFIG.C_Mult_Usage {{No_Usage}} \\
                        CONFIG.C_Rate {{1}} \\
                        CONFIG.RESULT_TLAST_Behv {{Pass_A_TLAST}}] [get_ips floating_point_0]

                    """
            elif(Has_RESULT_TREADY == "false"):
                if(latency == 3):
                    param_setting = f"""

                    set_property -dict [list \\
                        CONFIG.Operation_Type {{Compare}} \\
                        CONFIG.C_Compare_Operation {{{op_mode}}} \\
                        CONFIG.Axi_Optimize_Goal {{Performance}} \\
                        CONFIG.Has_RESULT_TREADY {{false}} \\
                        CONFIG.Maximum_Latency {{false}} \\
                        CONFIG.Has_ACLKEN {{{aclken_vld}}} \\
                        CONFIG.Has_ARESETn {{{aresetn_vld}}} \\
                        CONFIG.Has_A_TLAST {{{Has_A_TLAST}}} \\
                        CONFIG.Has_A_TUSER {{{Has_A_TUSER}}} \\
                        CONFIG.Has_B_TLAST {{{Has_B_TLAST}}} \\
                        CONFIG.Has_B_TUSER {{{Has_B_TUSER}}} \\
                        CONFIG.A_Precision_Type {{{Precision_Type}}} \\
                        CONFIG.C_A_Exponent_Width {{{Exp_width}}} \\
                        CONFIG.C_A_Fraction_Width {{{Fra_width}}} \\
                        CONFIG.Result_Precision_Type {{Custom}} \\
                        CONFIG.C_Result_Exponent_Width {{{Result_Exponent_Width}}} \\
                        CONFIG.C_Result_Fraction_Width {{0}} \\
                        CONFIG.C_Mult_Usage {{No_Usage}} \\
                        CONFIG.C_Latency {{{latency}}} \\
                        CONFIG.C_Rate {{1}} \\
                        CONFIG.RESULT_TLAST_Behv {{Pass_A_TLAST}}] [get_ips floating_point_0]

                    """
                elif(latency < 3):
                    param_setting = f"""
                    set_property -dict [list \\
                        CONFIG.Operation_Type {{Compare}} \\
                        CONFIG.C_Compare_Operation {{{op_mode}}} \\
                        CONFIG.Axi_Optimize_Goal {{Performance}} \\
                        CONFIG.Has_RESULT_TREADY {{false}} \\
                        CONFIG.Maximum_Latency {{false}} \\
                        CONFIG.C_Latency {{{latency}}} \\
                        CONFIG.Has_ACLKEN {{{aclken_vld}}} \\
                        CONFIG.Has_ARESETn {{{aresetn_vld}}} \\
                        CONFIG.Has_A_TLAST {{{Has_A_TLAST}}} \\
                        CONFIG.Has_A_TUSER {{{Has_A_TUSER}}} \\
                        CONFIG.Has_B_TLAST {{{Has_B_TLAST}}} \\
                        CONFIG.Has_B_TUSER {{{Has_B_TUSER}}} \\
                        CONFIG.A_Precision_Type {{{Precision_Type}}} \\
                        CONFIG.C_A_Exponent_Width {{{Exp_width}}} \\
                        CONFIG.C_A_Fraction_Width {{{Fra_width}}} \\
                        CONFIG.Result_Precision_Type {{Custom}} \\
                        CONFIG.C_Result_Exponent_Width {{{Result_Exponent_Width}}} \\
                        CONFIG.C_Result_Fraction_Width {{0}} \\
                        CONFIG.C_Mult_Usage {{No_Usage}} \\
                        CONFIG.C_Rate {{1}} \\
                        CONFIG.RESULT_TLAST_Behv {{Pass_A_TLAST}}] [get_ips floating_point_0]

                    """

    return param_setting

# def main():
#     project_name = "my_project"

#     # 设置项目路径 (绝对路径)
#     project_dir = r"D:/Code/vivado/script_tcl/my_project_dir"

#     # 设置RTL文件路径
#     filelist = r"D:/Code/vivado/script_tcl/rtl_list.tcl"

#     # 设置源文件顶层文件名称
#     source_top_module = "top"
#     # 设置仿真文件顶层文件名称
#     tb_top_module = "tb"
#     # 设置IP核路径
#     ip_dir = f"{project_dir}"


#     param_setting = ip_param_setting("Equal", "blocking", latency=3,Precision_Type="Custom",Exp_width=13,Fra_width=53,Has_RESULT_TREADY="false")
#     create_ip = ip_generate(ip_dir, project_dir, param_setting)
#     tcl_generate(project_name, project_dir, filelist, source_top_module, tb_top_module, create_ip)


# main()