OPENQASM 2.0;
include "qelib1.inc";

qreg q[17];
creg rec[8];

reset q[9]; h q[9]; // decomposed RX
reset q[10]; h q[10]; // decomposed RX
reset q[11]; h q[11]; // decomposed RX
reset q[12]; h q[12]; // decomposed RX
reset q[13]; h q[13]; // decomposed RX
reset q[14]; h q[14]; // decomposed RX
reset q[15]; h q[15]; // decomposed RX
reset q[16]; h q[16]; // decomposed RX
barrier q;

cx q[9], q[0];
cx q[11], q[7];
cx q[12], q[6];
barrier q;

barrier q;

cz q[13], q[4];
cz q[14], q[8];
cz q[15], q[5];
barrier q;

barrier q;

cx q[9], q[4];
cx q[11], q[1];
cx q[12], q[8];
barrier q;

barrier q;

cz q[13], q[3];
cz q[14], q[0];
cz q[15], q[7];
barrier q;

barrier q;

cx q[9], q[1];
cx q[10], q[8];
cx q[12], q[5];
barrier q;

barrier q;

cz q[14], q[2];
cz q[15], q[0];
cz q[16], q[6];
barrier q;

barrier q;

cx q[9], q[3];
cx q[10], q[2];
cx q[12], q[0];
barrier q;

barrier q;

cz q[14], q[4];
cz q[15], q[1];
cz q[16], q[5];
barrier q;

h q[9]; measure q[9] -> rec[0]; h q[9]; // decomposed MX
h q[10]; measure q[10] -> rec[1]; h q[10]; // decomposed MX
h q[11]; measure q[11] -> rec[2]; h q[11]; // decomposed MX
h q[12]; measure q[12] -> rec[3]; h q[12]; // decomposed MX
h q[13]; measure q[13] -> rec[4]; h q[13]; // decomposed MX
h q[14]; measure q[14] -> rec[5]; h q[14]; // decomposed MX
h q[15]; measure q[15] -> rec[6]; h q[15]; // decomposed MX
h q[16]; measure q[16] -> rec[7]; h q[16]; // decomposed MX
