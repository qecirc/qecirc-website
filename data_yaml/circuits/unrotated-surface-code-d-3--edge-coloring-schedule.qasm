OPENQASM 2.0;
include "qelib1.inc";

qreg q[25];
creg rec[12];

reset q[13]; h q[13]; // decomposed RX
reset q[14]; h q[14]; // decomposed RX
reset q[15]; h q[15]; // decomposed RX
reset q[16]; h q[16]; // decomposed RX
reset q[17]; h q[17]; // decomposed RX
reset q[18]; h q[18]; // decomposed RX
reset q[19]; h q[19]; // decomposed RX
reset q[20]; h q[20]; // decomposed RX
reset q[21]; h q[21]; // decomposed RX
reset q[22]; h q[22]; // decomposed RX
reset q[23]; h q[23]; // decomposed RX
reset q[24]; h q[24]; // decomposed RX
barrier q;

cx q[13], q[4];
cx q[14], q[5];
cx q[15], q[6];
cx q[16], q[7];
cx q[17], q[8];
cx q[18], q[9];
barrier q;

barrier q;

cz q[19], q[2];
cz q[20], q[0];
cz q[21], q[3];
cz q[22], q[1];
barrier q;

barrier q;

cx q[14], q[2];
cx q[15], q[0];
cx q[17], q[3];
cx q[18], q[1];
cz q[19], q[11];
cz q[20], q[12];
cz q[21], q[5];
cz q[22], q[6];
cz q[23], q[8];
cz q[24], q[9];
barrier q;

barrier q;

cx q[13], q[2];
cx q[14], q[0];
cx q[16], q[3];
cx q[17], q[1];
cz q[19], q[10];
cz q[20], q[11];
cz q[21], q[4];
cz q[22], q[5];
cz q[23], q[7];
cz q[24], q[8];
barrier q;

barrier q;

cz q[21], q[2];
cz q[22], q[0];
cz q[23], q[3];
cz q[24], q[1];
barrier q;

barrier q;

cx q[13], q[10];
cx q[14], q[11];
cx q[15], q[12];
cx q[16], q[4];
cx q[17], q[5];
cx q[18], q[6];
barrier q;

h q[13]; measure q[13] -> rec[0]; h q[13]; // decomposed MX
h q[14]; measure q[14] -> rec[1]; h q[14]; // decomposed MX
h q[15]; measure q[15] -> rec[2]; h q[15]; // decomposed MX
h q[16]; measure q[16] -> rec[3]; h q[16]; // decomposed MX
h q[17]; measure q[17] -> rec[4]; h q[17]; // decomposed MX
h q[18]; measure q[18] -> rec[5]; h q[18]; // decomposed MX
h q[19]; measure q[19] -> rec[6]; h q[19]; // decomposed MX
h q[20]; measure q[20] -> rec[7]; h q[20]; // decomposed MX
h q[21]; measure q[21] -> rec[8]; h q[21]; // decomposed MX
h q[22]; measure q[22] -> rec[9]; h q[22]; // decomposed MX
h q[23]; measure q[23] -> rec[10]; h q[23]; // decomposed MX
h q[24]; measure q[24] -> rec[11]; h q[24]; // decomposed MX
