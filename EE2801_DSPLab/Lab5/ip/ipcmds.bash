sed -i '/twentynm/d' ip_core_sim/ip_core_msim.tcl
sed -i '/stratix/d' ip_core_sim/ip_core_msim.tcl
sed -i '/arria/d' ip_core_sim/ip_core_msim.tcl

cd ip_core_sim/
vsim -c -do "
	source ip_core_msim.tcl; 
	design_com; 
	vlog -sv ip_core_tb.v; 
	vsim -L cyclonev -L altera_mf -L lpm -L sgate -L altera -L altera_lnsim work.ip_core_tb; 
	run -all; 
	quit
 "