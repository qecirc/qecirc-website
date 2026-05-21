OPENQASM 2.0;
include "qelib1.inc";

qreg q[30];

reset q[22];
reset q[16];
reset q[13];
reset q[10];
reset q[7];
reset q[6];
reset q[5];
reset q[3];
reset q[2];
reset q[15];
reset q[12];
reset q[26];
reset q[4]; h q[4]; // decomposed RX
reset q[1]; h q[1]; // decomposed RX
reset q[0]; h q[0]; // decomposed RX
reset q[24]; h q[24]; // decomposed RX
reset q[18]; h q[18]; // decomposed RX
reset q[9]; h q[9]; // decomposed RX
reset q[23]; h q[23]; // decomposed RX
reset q[17]; h q[17]; // decomposed RX
reset q[29]; h q[29]; // decomposed RX
reset q[21]; h q[21]; // decomposed RX
reset q[27]; h q[27]; // decomposed RX
reset q[28]; h q[28]; // decomposed RX
reset q[20]; h q[20]; // decomposed RX
reset q[25]; h q[25]; // decomposed RX
reset q[19]; h q[19]; // decomposed RX
reset q[14]; h q[14]; // decomposed RX
reset q[8]; h q[8]; // decomposed RX
reset q[11]; h q[11]; // decomposed RX
cx q[25], q[12];
cx q[17], q[2];
cx q[23], q[3];
cx q[11], q[5];
cx q[8], q[6];
cx q[21], q[13];
cx q[27], q[26];
cx q[19], q[22];
cx q[9], q[15];
cx q[2], q[3];
cx q[29], q[5];
cx q[25], q[7];
cx q[8], q[10];
cx q[21], q[16];
cx q[14], q[26];
cx q[18], q[6];
cx q[2], q[12];
cx q[3], q[5];
cx q[0], q[7];
cx q[27], q[10];
cx q[24], q[16];
cx q[25], q[22];
cx q[11], q[21];
cx q[28], q[26];
cx q[19], q[12];
cx q[0], q[9];
cx q[4], q[7];
cx q[15], q[10];
cx q[1], q[22];
cx q[14], q[3];
cx q[24], q[27];
cx q[21], q[8];
cx q[18], q[25];
cx q[5], q[2];
cx q[20], q[11];
cx q[8], q[29];
cx q[2], q[9];
cx q[15], q[6];
cx q[11], q[7];
cx q[3], q[13];
cx q[19], q[0];
cx q[1], q[27];
cx q[28], q[18];
cx q[24], q[5];
cx q[4], q[16];
cx q[20], q[14];
cx q[25], q[10];
cx q[27], q[12];
cx q[14], q[7];
cx q[0], q[10];
cx q[8], q[22];
cx q[28], q[11];
cx q[4], q[15];
cx q[25], q[20];
cx q[5], q[21];
cx q[1], q[2];
cx q[3], q[19];
cx q[18], q[24];
cx q[2], q[13];
cx q[11], q[22];
cx q[20], q[1];
cx q[4], q[28];
cx q[14], q[21];
cx q[0], q[24];
cx q[15], q[25];
cx q[19], q[5];
cx q[8], q[3];
cx q[27], q[18];
