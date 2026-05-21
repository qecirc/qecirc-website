OPENQASM 2.0;
include "qelib1.inc";

qreg q[37];

reset q[14];
reset q[4];
reset q[27];
reset q[33];
reset q[15];
reset q[8];
reset q[20];
reset q[35];
reset q[36];
reset q[24];
reset q[16];
reset q[34];
reset q[22];
reset q[28];
reset q[32];
reset q[13];
reset q[25];
reset q[30];
reset q[26];
reset q[31]; h q[31]; // decomposed RX
reset q[23]; h q[23]; // decomposed RX
reset q[21]; h q[21]; // decomposed RX
reset q[18]; h q[18]; // decomposed RX
reset q[17]; h q[17]; // decomposed RX
reset q[12]; h q[12]; // decomposed RX
reset q[11]; h q[11]; // decomposed RX
reset q[10]; h q[10]; // decomposed RX
reset q[9]; h q[9]; // decomposed RX
reset q[7]; h q[7]; // decomposed RX
reset q[6]; h q[6]; // decomposed RX
reset q[5]; h q[5]; // decomposed RX
reset q[3]; h q[3]; // decomposed RX
reset q[2]; h q[2]; // decomposed RX
reset q[1]; h q[1]; // decomposed RX
reset q[29]; h q[29]; // decomposed RX
reset q[0]; h q[0]; // decomposed RX
reset q[19]; h q[19]; // decomposed RX
cx q[19], q[30];
cx q[7], q[35];
cx q[0], q[26];
cx q[1], q[28];
cx q[5], q[34];
cx q[6], q[20];
cx q[11], q[4];
cx q[12], q[13];
cx q[17], q[25];
cx q[3], q[15];
cx q[9], q[16];
cx q[10], q[27];
cx q[21], q[22];
cx q[23], q[24];
cx q[7], q[36];
cx q[18], q[30];
cx q[31], q[35];
cx q[20], q[25];
cx q[0], q[34];
cx q[4], q[19];
cx q[5], q[12];
cx q[6], q[11];
cx q[28], q[13];
cx q[1], q[8];
cx q[16], q[15];
cx q[24], q[22];
cx q[36], q[17];
cx q[2], q[7];
cx q[18], q[14];
cx q[31], q[32];
cx q[35], q[33];
cx q[26], q[20];
cx q[3], q[5];
cx q[6], q[23];
cx q[10], q[11];
cx q[21], q[4];
cx q[32], q[34];
cx q[28], q[35];
cx q[29], q[2];
cx q[0], q[36];
cx q[27], q[33];
cx q[14], q[9];
cx q[31], q[18];
cx q[11], q[20];
cx q[23], q[21];
cx q[4], q[6];
cx q[25], q[10];
cx q[7], q[1];
cx q[30], q[26];
cx q[33], q[36];
cx q[29], q[28];
cx q[12], q[31];
cx q[5], q[14];
cx q[34], q[18];
cx q[13], q[32];
cx q[2], q[8];
cx q[17], q[27];
cx q[9], q[3];
cx q[19], q[0];
