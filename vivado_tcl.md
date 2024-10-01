# Vivado tcl 自动化脚本记录

### 下面这段用来输出vivado跑出来的资源报告,还能自动仿真，如果要输出仿真时的数据，需要在tb文件里编写对应的代码
```tcl
# 这个文件名为 run.tcl
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
# [current_fileset]指的是Design Source这个"文件夹"(vivado ui 里 Sources这部分能看到的那个文件夹)
set_property top top [current_fileset]
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
close_project


```
```tcl
# 这个文件名为 rtl_list.tcl,在上面的run.tcl里被使用，用来将rtl文件加进工程中
set path D:/Code/vivado/script_tcl

read_verilog $path/rtl/top.v
read_verilog $path/rtl/tb.v
```
