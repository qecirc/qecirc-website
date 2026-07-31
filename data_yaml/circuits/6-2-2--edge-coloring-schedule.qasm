OPENQASM 2.0;
include "qelib1.inc";

qreg q[10];
creg rec[4];

reset q[6]; h q[6]; // decomposed RX
reset q[7]; h q[7]; // decomposed RX
reset q[8]; h q[8]; // decomposed RX
reset q[9]; h q[9]; // decomposed RX
barrier q;

cx q[6], q[2];
cx q[7], q[0];
barrier q;

cx q[6], q[0];
cx q[7], q[1];
barrier q;

cx q[6], q[1];
cx q[7], q[4];
barrier q;

cx q[6], q[3];
cx q[7], q[5];
barrier q;

barrier q;

cz q[8], q[2];
cz q[9], q[0];
barrier q;

cz q[8], q[1];
cz q[9], q[5];
barrier q;

cz q[8], q[3];
cz q[9], q[1];
barrier q;

cz q[8], q[0];
cz q[9], q[4];
barrier q;

h q[6]; measure q[6] -> rec[0]; h q[6]; // decomposed MX
h q[7]; measure q[7] -> rec[1]; h q[7]; // decomposed MX
h q[8]; measure q[8] -> rec[2]; h q[8]; // decomposed MX
h q[9]; measure q[9] -> rec[3]; h q[9]; // decomposed MX
