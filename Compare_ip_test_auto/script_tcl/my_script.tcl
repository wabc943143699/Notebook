
    set project_name "inst2"

    set project_dir "D:/Code/vivado/compare_test/inst2"

    set filelist "D:/Code/vivado/compare_test/inst2/rtl"

    create_project $project_name $project_dir -part xc7k325tffg676-3 -force

    source $filelist

    set_property top top [current_fileset]

    
    create_ip \
        -name floating_point \
        -vendor xilinx.com \
        -library ip \
        -version 7.1 \
        -module_name floating_point_0 \
        -dir "D:/Code/vivado/compare_test/inst2"
    
    

                set_property \
                    -dict [list \
                        CONFIG.Operation_Type {Compare} \
                        CONFIG.Flow_Control {NonBlocking} \
                        CONFIG.Maximum_Latency {false} \
                        CONFIG.Has_ACLKEN {True} \
                        CONFIG.Has_ARESETn {True} \
                        CONFIG.C_Has_INVALID_OP {True} \
                        CONFIG.Has_A_TLAST {True} \
                        CONFIG.Has_A_TUSER {True} \
                        CONFIG.Has_B_TLAST {True} \
                        CONFIG.Has_B_TUSER {True} \
                        CONFIG.Has_OPERATION_TLAST {True} \
                        CONFIG.Has_OPERATION_TUSER {True} \
                        CONFIG.A_Precision_Type {Double} \
                        CONFIG.C_A_Exponent_Width {11.0} \
                        CONFIG.C_A_Fraction_Width {53.0} \
                        CONFIG.Result_Precision_Type {Custom} \
                        CONFIG.C_Result_Exponent_Width {1} \
                        CONFIG.C_Result_Fraction_Width {0} \
                        CONFIG.C_Mult_Usage {No_Usage} \
                        CONFIG.Has_RESULT_TREADY {false} \
                        CONFIG.C_Latency {2.0} \
                        CONFIG.C_Rate {1} \
                        CONFIG.RESULT_TLAST_Behv {Pass_A_TLAST} \
                    ] \
                    [get_ips floating_point_0]

                
    

    generate_target {instantiation_template} [get_files "D:/Code/vivado/compare_test/inst2/floating_point_0/floating_point_0.xci"]
    generate_target all [get_files  "D:/Code/vivado/compare_test/inst2/floating_point_0/floating_point_0.xci"]
    catch { config_ip_cache -export [get_ips -all floating_point_0] }
    export_ip_user_files \
        -of_objects [get_files "D:/Code/vivado/compare_test/inst2/floating_point_0/floating_point_0.xci"] \
        -no_script \
        -sync \
        -force \
        -quiet

    create_ip_run [get_files -of_objects [get_fileset sources_1] "D:/Code/vivado/compare_test/inst2/floating_point_0/floating_point_0.xci"]
    launch_runs -jobs 16 floating_point_0_synth_1
    export_simulation \
        -of_objects [get_files "D:/Code/vivado/compare_test/inst2/floating_point_0/floating_point_0.xci"] \
        -directory "D:/Code/vivado/compare_test/inst2/my_project.ip_user_files/sim_scripts" \
        -ip_user_files_dir "D:/Code/vivado/compare_test/inst2/my_project.ip_user_files" \
        -ipstatic_source_dir "D:/Code/vivado/compare_test/inst2/my_project.ip_user_files/ipstatic" \
        -lib_map_path [list \
            {modelsim="D:/Code/vivado/compare_test/inst2/my_project.cache/compile_simlib/modelsim"} \
            {questa="D:/Code/vivado/compare_test/inst2/my_project.cache/compile_simlib/questa"} \
            {riviera="D:/Code/vivado/compare_test/inst2/my_project.cache/compile_simlib/riviera"} \
            {activehdl="D:/Code/vivado/compare_test/inst2/my_project.cache/compile_simlib/activehdl"} \
        ] \
        -use_ip_compiled_libs \
        -force \
        -quiet

    

    reset_run synth_1
    reset_run impl_1

    launch_runs synth_1
    wait_on_run synth_1

    open_run synth_1 -name synth_1
    opt_design
    report_utilization -file "${project_dir}/${project_name}_utilization_synth_summary.rpt"
    puts "Synthesis utilization summary report generated."

    launch_runs impl_1
    wait_on_run impl_1
    open_run impl_1 -name impl_1
    report_utilization -file "${project_dir}/${project_name}_utilization_impl_summary.rpt"
    puts "Implementation utilization summary report generated."

    set_property top tb [get_filesets sim_1]

    set_property target_simulator "XSim" [current_project]

    launch_simulation
    restart
    run all

    close_sim
    close_project
    