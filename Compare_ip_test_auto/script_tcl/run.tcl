#设置项目名称
set project_name "my_project"
#设置项目路径(绝对路径)
set project_dir "D:/Code/vivado/script_tcl/my_project_dir"
#设置rtl文件路径
set filelist "D:/Code/vivado/script_tcl/rtl_list.tcl"
#新建项目
create_project $project_name $project_dir -part xc7k325tffg676-3 -force
#添加rtl文件
source $filelist
#设置顶层文件
# 这里也可以用[get_filesets sources_1]，直接选中Design sources这个set
# set_property top top [get_filesets sources_1] 和 set_property top top [current_fileset] 的效果是一样的
set_property top top [current_fileset] 

#生成比较ip核
create_ip -name floating_point -vendor xilinx.com -library ip -version 7.1 -module_name floating_point_0 -dir d:/Code/vivado/script_tcl/my_project_dir/my_project.srcs/sources_1/ip
set_property -dict [list CONFIG.Operation_Type {Compare} CONFIG.Flow_Control {NonBlocking} CONFIG.Maximum_Latency {false} CONFIG.C_Latency {1} CONFIG.Has_ACLKEN {true} CONFIG.Has_ARESETn {true} CONFIG.C_Has_INVALID_OP {true} CONFIG.Has_A_TLAST {true} CONFIG.Has_A_TUSER {true} CONFIG.Has_B_TLAST {true} CONFIG.Has_B_TUSER {true} CONFIG.Has_OPERATION_TLAST {true} CONFIG.Has_OPERATION_TUSER {true} CONFIG.A_Precision_Type {Single} CONFIG.C_A_Exponent_Width {8} CONFIG.C_A_Fraction_Width {24} CONFIG.Result_Precision_Type {Custom} CONFIG.C_Result_Exponent_Width {1} CONFIG.C_Result_Fraction_Width {0} CONFIG.C_Mult_Usage {No_Usage} CONFIG.Has_RESULT_TREADY {false} CONFIG.C_Rate {1} CONFIG.RESULT_TLAST_Behv {Pass_A_TLAST}] [get_ips floating_point_0]
generate_target {instantiation_template} [get_files d:/Code/vivado/script_tcl/my_project_dir/my_project.srcs/sources_1/ip/floating_point_0/floating_point_0.xci]
generate_target all [get_files  d:/Code/vivado/script_tcl/my_project_dir/my_project.srcs/sources_1/ip/floating_point_0/floating_point_0.xci]
catch { config_ip_cache -export [get_ips -all floating_point_0] }
export_ip_user_files -of_objects [get_files d:/Code/vivado/script_tcl/my_project_dir/my_project.srcs/sources_1/ip/floating_point_0/floating_point_0.xci] -no_script -sync -force -quiet
create_ip_run [get_files -of_objects [get_fileset sources_1] d:/Code/vivado/script_tcl/my_project_dir/my_project.srcs/sources_1/ip/floating_point_0/floating_point_0.xci]
launch_runs -jobs 16 floating_point_0_synth_1
export_simulation -of_objects [get_files d:/Code/vivado/script_tcl/my_project_dir/my_project.srcs/sources_1/ip/floating_point_0/floating_point_0.xci] -directory D:/Code/vivado/script_tcl/my_project_dir/my_project.ip_user_files/sim_scripts -ip_user_files_dir D:/Code/vivado/script_tcl/my_project_dir/my_project.ip_user_files -ipstatic_source_dir D:/Code/vivado/script_tcl/my_project_dir/my_project.ip_user_files/ipstatic -lib_map_path [list {modelsim=D:/Code/vivado/script_tcl/my_project_dir/my_project.cache/compile_simlib/modelsim} {questa=D:/Code/vivado/script_tcl/my_project_dir/my_project.cache/compile_simlib/questa} {riviera=D:/Code/vivado/script_tcl/my_project_dir/my_project.cache/compile_simlib/riviera} {activehdl=D:/Code/vivado/script_tcl/my_project_dir/my_project.cache/compile_simlib/activehdl}] -use_ip_compiled_libs -force -quiet

#初始化
reset_run synth_1
reset_run impl_1

# 跑synthesis
launch_runs synth_1
wait_on_run synth_1

open_run synth_1 -name synth_1
opt_design
report_utilization -file "${project_dir}/${project_name}_utilization_synth_summary.rpt"
puts "Synthesis utilization summary report generated."
# 跑implementation
launch_runs impl_1
wait_on_run impl_1
open_run impl_1 -name impl_1
report_utilization -file "${project_dir}/${project_name}_utilization_impl_summary.rpt"
puts "Implementation utilization summary report generated."


# 下面是仿真流程
# 先设置sim_1里的顶层文件
set_property top tb [get_filesets sim_1]
# 选择仿真器
set_property target_simulator "XSim" [current_project]  
# 运行仿真
launch_simulation
restart
run all

close_sim
#close_project





# compare programmable single nonblocking latency = 1 all signal enable----------------------------------------------------------
#--------------------------------------------------------------------------------------------------------------------------------
# create_ip -name floating_point -vendor xilinx.com -library ip -version 7.1 -module_name floating_point_0 -dir d:/Code/vivado/script_tcl/my_project_dir/my_project.srcs/sources_1/ip
# set_property -dict [list CONFIG.Operation_Type {Compare} CONFIG.Flow_Control {NonBlocking} CONFIG.Maximum_Latency {false} CONFIG.C_Latency {1} CONFIG.Has_ACLKEN {true} CONFIG.Has_ARESETn {true} CONFIG.C_Has_INVALID_OP {true} CONFIG.Has_A_TLAST {true} CONFIG.Has_A_TUSER {true} CONFIG.Has_B_TLAST {true} CONFIG.Has_B_TUSER {true} CONFIG.Has_OPERATION_TLAST {true} CONFIG.Has_OPERATION_TUSER {true} CONFIG.A_Precision_Type {Single} CONFIG.C_A_Exponent_Width {8} CONFIG.C_A_Fraction_Width {24} CONFIG.Result_Precision_Type {Custom} CONFIG.C_Result_Exponent_Width {1} CONFIG.C_Result_Fraction_Width {0} CONFIG.C_Mult_Usage {No_Usage} CONFIG.Has_RESULT_TREADY {false} CONFIG.C_Rate {1} CONFIG.RESULT_TLAST_Behv {Pass_A_TLAST}] [get_ips floating_point_0]
# generate_target {instantiation_template} [get_files d:/Code/vivado/script_tcl/my_project_dir/my_project.srcs/sources_1/ip/floating_point_0/floating_point_0.xci]
# generate_target all [get_files  d:/Code/vivado/script_tcl/my_project_dir/my_project.srcs/sources_1/ip/floating_point_0/floating_point_0.xci]
# catch { config_ip_cache -export [get_ips -all floating_point_0] }
# export_ip_user_files -of_objects [get_files d:/Code/vivado/script_tcl/my_project_dir/my_project.srcs/sources_1/ip/floating_point_0/floating_point_0.xci] -no_script -sync -force -quiet
# create_ip_run [get_files -of_objects [get_fileset sources_1] d:/Code/vivado/script_tcl/my_project_dir/my_project.srcs/sources_1/ip/floating_point_0/floating_point_0.xci]
# launch_runs -jobs 16 floating_point_0_synth_1
# export_simulation -of_objects [get_files d:/Code/vivado/script_tcl/my_project_dir/my_project.srcs/sources_1/ip/floating_point_0/floating_point_0.xci] -directory D:/Code/vivado/script_tcl/my_project_dir/my_project.ip_user_files/sim_scripts -ip_user_files_dir D:/Code/vivado/script_tcl/my_project_dir/my_project.ip_user_files -ipstatic_source_dir D:/Code/vivado/script_tcl/my_project_dir/my_project.ip_user_files/ipstatic -lib_map_path [list {modelsim=D:/Code/vivado/script_tcl/my_project_dir/my_project.cache/compile_simlib/modelsim} {questa=D:/Code/vivado/script_tcl/my_project_dir/my_project.cache/compile_simlib/questa} {riviera=D:/Code/vivado/script_tcl/my_project_dir/my_project.cache/compile_simlib/riviera} {activehdl=D:/Code/vivado/script_tcl/my_project_dir/my_project.cache/compile_simlib/activehdl}] -use_ip_compiled_libs -force -quiet


