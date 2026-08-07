OPENQASM 2.0;
include "qelib1.inc";

qreg q[13];
creg rec[6];

reset q[7]; h q[7]; // decomposed RX
reset q[8]; h q[8]; // decomposed RX
reset q[9]; h q[9]; // decomposed RX
reset q[10]; h q[10]; // decomposed RX
reset q[11]; h q[11]; // decomposed RX
reset q[12]; h q[12]; // decomposed RX
barrier q;

cx q[7], q[4];
cx q[8], q[2];
cx q[9], q[6];
barrier q;

cx q[7], q[5];
cx q[8], q[6];
cx q[9], q[2];
barrier q;

cx q[7], q[6];
cx q[8], q[5];
cx q[9], q[4];
barrier q;

cx q[7], q[3];
cx q[8], q[1];
cx q[9], q[0];
barrier q;

barrier q;

cz q[10], q[4];
cz q[11], q[2];
cz q[12], q[6];
barrier q;

cz q[10], q[5];
cz q[11], q[6];
cz q[12], q[2];
barrier q;

cz q[10], q[6];
cz q[11], q[5];
cz q[12], q[4];
barrier q;

cz q[10], q[3];
cz q[11], q[1];
cz q[12], q[0];
barrier q;

h q[7]; measure q[7] -> rec[0]; h q[7]; // decomposed MX
h q[8]; measure q[8] -> rec[1]; h q[8]; // decomposed MX
h q[9]; measure q[9] -> rec[2]; h q[9]; // decomposed MX
h q[10]; measure q[10] -> rec[3]; h q[10]; // decomposed MX
h q[11]; measure q[11] -> rec[4]; h q[11]; // decomposed MX
h q[12]; measure q[12] -> rec[5]; h q[12]; // decomposed MX
