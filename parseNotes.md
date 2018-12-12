First trim each line

ignore the line if it starts with #

split the line with , delimiter and strip off the spaces to get the line columns, strip off " also while processing column values

each substation is identified by substation id
each device is identified by device id, substation id
each node is identified by node id, substation id

if line cols start with SUBSTN,it is a substation record, hence update **current substation**. substation id col = 1, substation name col = 2

if line cols start with DEVTYP,it is a device type record,hence update **current device type**. device type name col = 1

if line cols start with DEVICE, it is a device record, hence upadte **current device**. device id col = 1, device name col = 2, device voltage = 5

if the device is a BUS, then it is node by itself, hence it has only one node. The node name is device id col, i.e., column 1

if the device is a line, then the node pair is stored in the device definition itself, the current substation node is col 7 and remote substation id is col 11, remote substation node is col 10

if the device is a RE, then the node is stored in the device definition itself, the node name is col 7

if device is not line, bus then node pair can be found from the sttd point which will come in the coming lines

if the line cols start with POINT,STTD then update the **current node**. the node pair columns are 4 and 5