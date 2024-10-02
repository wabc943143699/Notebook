# 一个具有自动综合、实现、创建浮点比较ip、仿真等功能的python脚本
## 利用python脚本生成vivado tcl脚本进行自动化操作
Excel表中编写的是要生成的ip核参数，通过控制Folder_create.py里面的inst_num = 2参数和文件路径，将rtl文件和rtl_list.tcl脚本复制到各个case的文件夹中
然后修改compare_test_auto_main.py里面的inst_num = 2参数和文件路径，生成vivado tcl脚本并自动运行tcl脚本，运行信息存在run.log中


