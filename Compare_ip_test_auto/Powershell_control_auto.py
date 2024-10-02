import subprocess

# 要运行的 PowerShell 命令
# command = "ls"

# 指定工作目录，例如 D:\TestDirectory
# working_directory = r"D:/Code/vivado/script_tcl"

def powershell_work_auto(working_directory, command):
    with open(working_directory+"/run.log", "w") as run_log, open(working_directory+"/error.log", "w") as error_log:
        # 执行 PowerShell 命令，将输出和错误分别重定向到文件
        result = subprocess.run(
            ["powershell", "-Command", command],
            cwd=working_directory,
            stdout=run_log,       # 将输出写入 run.log
            stderr=error_log,     # 将错误写入 error.log
            text=True
        )
    print("Powershell命令已执行")
