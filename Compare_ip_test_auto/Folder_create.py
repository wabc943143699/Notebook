import os
import shutil

# 创建文件夹的根目录，例如 D:\TestDirectory
root_directory = r"D:/Code/vivado/compare_test"
# inst数量
inst_num = 2
# 要创建的文件夹名称列表
folders_to_create = [f"inst{i+1}" for i in range(inst_num)]


# 要复制的文件路径列表
files_to_copy = [r"D:/Code/vivado/script_tcl/clear.bat", r"D:/Code/vivado/script_tcl/rtl_list.tcl"]
folder_to_copy = [r"D:/Code/vivado/script_tcl/rtl"]
# 开始创建文件夹并复制文件
for folder in folders_to_create:
    # 构建新文件夹的完整路径
    #folder_path = os.path.join(root_directory, folder)
    folder_path = root_directory + '/' + folder
    
    if os.path.exists(folder_path):
        shutil.rmtree(folder_path)
        print(f"文件夹 {folder_path} 已删除")
    
    # 创建新的文件夹
    os.makedirs(folder_path)
    print(f"文件夹 {folder_path} 创建成功")
    
    # 将文件复制到新创建的文件夹中
    for file_path in files_to_copy:
        if os.path.exists(file_path):
            shutil.copy(file_path, folder_path)
            print(f"文件 {file_path} 已复制到 {folder_path}")
        else:
            print(f"文件 {file_path} 不存在，跳过复制")
    
    # 将整个文件夹及其内容复制到新创建的文件夹中
    for i in folder_to_copy:
        if os.path.exists(i):
            destination_folder = os.path.join(folder_path, os.path.basename(i))
            shutil.copytree(i, destination_folder)
            print(f"文件夹 {i} 及其内容已复制到 {destination_folder}")
        else:
            print(f"文件夹 {i} 不存在，跳过复制")

    # 修改rtl_list里面的路径
    rtl_list_path = folder_path + "/rtl_list.tcl"
    with open(rtl_list_path, 'r') as rtl_list:
        file_data = rtl_list.read()
    file_data = file_data.replace("set path D:/Code/vivado/script_tcl", "set path " + folder_path)
    with open(rtl_list_path, 'w') as rtl_list:
        rtl_list.write(file_data)
    print("rtl_list文件修改成功")
    # print(file_data)

    # tb文件也需要改一下，因为tb里有一个路径要往出保存数据
    tb_file_path = folder_path + "/rtl/tb.v"
    with open(tb_file_path, 'r') as tb_file:
        tb_data = tb_file.read()
    tb_data = tb_data.replace("D:/Code/vivado/script_tcl/my_project_dir/data_out.txt", folder_path + "/data_out.txt")
    with open(tb_file_path, 'w') as tb_file:
        tb_file.write(tb_data)
