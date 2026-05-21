OPENQASM 2.0;
include "qelib1.inc";

qreg q[31];

reset q[12];
reset q[7];
reset q[13];
reset q[1];
reset q[26];
reset q[28];
reset q[30];
reset q[18];
reset q[22];
reset q[15];
reset q[16];
reset q[29];
reset q[19];
reset q[25];
reset q[24];
reset q[23]; h q[23]; // decomposed RX
reset q[21]; h q[21]; // decomposed RX
reset q[17]; h q[17]; // decomposed RX
reset q[11]; h q[11]; // decomposed RX
reset q[10]; h q[10]; // decomposed RX
reset q[8]; h q[8]; // decomposed RX
reset q[6]; h q[6]; // decomposed RX
reset q[5]; h q[5]; // decomposed RX
reset q[4]; h q[4]; // decomposed RX
reset q[3]; h q[3]; // decomposed RX
reset q[9]; h q[9]; // decomposed RX
reset q[20]; h q[20]; // decomposed RX
reset q[0]; h q[0]; // decomposed RX
reset q[27]; h q[27]; // decomposed RX
reset q[14]; h q[14]; // decomposed RX
cx q[9], q[25];
cx q[2], q[13];
cx q[4], q[29];
cx q[5], q[24];
cx q[10], q[18];
cx q[23], q[12];
cx q[0], q[19];
cx q[8], q[7];
cx q[17], q[15];
cx q[25], q[13];
cx q[14], q[2];
cx q[9], q[4];
cx q[11], q[29];
cx q[5], q[26];
cx q[12], q[22];
cx q[20], q[0];
cx q[24], q[9];
cx q[18], q[25];
cx q[3], q[4];
cx q[6], q[14];
cx q[10], q[2];
cx q[21], q[11];
cx q[13], q[23];
cx q[22], q[16];
cx q[27], q[5];
cx q[12], q[30];
cx q[0], q[15];
cx q[19], q[18];
cx q[26], q[21];
cx q[4], q[13];
cx q[6], q[28];
cx q[17], q[10];
cx q[25], q[8];
cx q[9], q[1];
cx q[23], q[7];
cx q[3], q[12];
cx q[29], q[30];
cx q[14], q[24];
cx q[11], q[16];
cx q[27], q[28];
cx q[20], q[17];
cx q[5], q[6];
cx q[7], q[1];
cx q[10], q[19];
cx q[21], q[22];
cx q[2], q[26];
cx q[23], q[4];
cx q[8], q[9];
