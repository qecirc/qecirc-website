OPENQASM 2.0;
include "qelib1.inc";

qreg q[32];
creg rec[16];

reset q[16]; h q[16]; // decomposed RX
reset q[17]; h q[17]; // decomposed RX
reset q[18]; h q[18]; // decomposed RX
reset q[19]; h q[19]; // decomposed RX
reset q[20]; h q[20]; // decomposed RX
reset q[21]; h q[21]; // decomposed RX
reset q[22]; h q[22]; // decomposed RX
reset q[23]; h q[23]; // decomposed RX
reset q[24]; h q[24]; // decomposed RX
reset q[25]; h q[25]; // decomposed RX
reset q[26]; h q[26]; // decomposed RX
reset q[27]; h q[27]; // decomposed RX
reset q[28]; h q[28]; // decomposed RX
reset q[29]; h q[29]; // decomposed RX
reset q[30]; h q[30]; // decomposed RX
reset q[31]; h q[31]; // decomposed RX
barrier q;

cx q[16], q[12];
cx q[17], q[6];
cx q[18], q[2];
cx q[19], q[11];
cx q[20], q[1];
cx q[21], q[0];
cx q[22], q[9];
cx q[23], q[13];
cz q[24], q[7];
cz q[25], q[15];
cz q[26], q[3];
cz q[27], q[10];
cz q[28], q[5];
cz q[29], q[4];
cz q[30], q[14];
cz q[31], q[8];
barrier q;

barrier q;

cx q[16], q[15];
cx q[17], q[7];
cx q[18], q[3];
cx q[19], q[10];
cx q[20], q[4];
cx q[21], q[5];
cx q[22], q[14];
cx q[23], q[8];
cz q[24], q[12];
cz q[25], q[6];
cz q[26], q[11];
cz q[27], q[2];
cz q[28], q[1];
cz q[29], q[0];
cz q[30], q[13];
cz q[31], q[9];
barrier q;

barrier q;

cx q[16], q[14];
cx q[17], q[8];
cx q[18], q[7];
cx q[19], q[15];
cx q[20], q[3];
cx q[21], q[10];
cx q[22], q[5];
cx q[23], q[4];
cz q[24], q[9];
cz q[25], q[13];
cz q[26], q[12];
cz q[27], q[6];
cz q[28], q[2];
cz q[29], q[11];
cz q[30], q[1];
cz q[31], q[0];
barrier q;

barrier q;

cx q[16], q[13];
cx q[17], q[9];
cx q[18], q[12];
cx q[19], q[6];
cx q[20], q[11];
cx q[21], q[2];
cx q[22], q[1];
cx q[23], q[0];
cz q[24], q[14];
cz q[25], q[8];
cz q[26], q[15];
cz q[27], q[7];
cz q[28], q[3];
cz q[29], q[10];
cz q[30], q[4];
cz q[31], q[5];
barrier q;

h q[16]; measure q[16] -> rec[0]; h q[16]; // decomposed MX
h q[17]; measure q[17] -> rec[1]; h q[17]; // decomposed MX
h q[18]; measure q[18] -> rec[2]; h q[18]; // decomposed MX
h q[19]; measure q[19] -> rec[3]; h q[19]; // decomposed MX
h q[20]; measure q[20] -> rec[4]; h q[20]; // decomposed MX
h q[21]; measure q[21] -> rec[5]; h q[21]; // decomposed MX
h q[22]; measure q[22] -> rec[6]; h q[22]; // decomposed MX
h q[23]; measure q[23] -> rec[7]; h q[23]; // decomposed MX
h q[24]; measure q[24] -> rec[8]; h q[24]; // decomposed MX
h q[25]; measure q[25] -> rec[9]; h q[25]; // decomposed MX
h q[26]; measure q[26] -> rec[10]; h q[26]; // decomposed MX
h q[27]; measure q[27] -> rec[11]; h q[27]; // decomposed MX
h q[28]; measure q[28] -> rec[12]; h q[28]; // decomposed MX
h q[29]; measure q[29] -> rec[13]; h q[29]; // decomposed MX
h q[30]; measure q[30] -> rec[14]; h q[30]; // decomposed MX
h q[31]; measure q[31] -> rec[15]; h q[31]; // decomposed MX
