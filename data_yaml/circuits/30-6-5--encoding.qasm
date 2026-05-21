OPENQASM 2.0;
include "qelib1.inc";

qreg q[30];

reset q[6];
reset q[5];
reset q[24];
reset q[9];
reset q[12];
reset q[27];
reset q[28];
reset q[20];
reset q[25];
reset q[19];
reset q[8];
reset q[11];
reset q[7]; h q[7]; // decomposed RX
reset q[4]; h q[4]; // decomposed RX
reset q[1]; h q[1]; // decomposed RX
reset q[0]; h q[0]; // decomposed RX
reset q[18]; h q[18]; // decomposed RX
reset q[15]; h q[15]; // decomposed RX
reset q[23]; h q[23]; // decomposed RX
reset q[17]; h q[17]; // decomposed RX
reset q[26]; h q[26]; // decomposed RX
reset q[29]; h q[29]; // decomposed RX
reset q[21]; h q[21]; // decomposed RX
reset q[14]; h q[14]; // decomposed RX
cx q[21], q[28];
cx q[18], q[19];
cx q[0], q[25];
cx q[1], q[8];
cx q[2], q[12];
cx q[4], q[20];
cx q[7], q[27];
cx q[10], q[9];
cx q[13], q[11];
cx q[22], q[24];
cx q[16], q[6];
cx q[19], q[12];
cx q[0], q[9];
cx q[1], q[27];
cx q[3], q[10];
cx q[4], q[2];
cx q[7], q[21];
cx q[13], q[18];
cx q[14], q[20];
cx q[17], q[25];
cx q[23], q[28];
cx q[24], q[11];
cx q[15], q[19];
cx q[1], q[13];
cx q[0], q[18];
cx q[3], q[8];
cx q[4], q[7];
cx q[22], q[10];
cx q[17], q[27];
cx q[23], q[16];
cx q[9], q[24];
cx q[14], q[0];
cx q[29], q[4];
cx q[15], q[1];
cx q[22], q[5];
cx q[19], q[25];
cx q[2], q[10];
cx q[28], q[3];
cx q[8], q[20];
cx q[11], q[7];
cx q[14], q[22];
cx q[26], q[25];
cx q[17], q[5];
cx q[15], q[6];
cx q[3], q[20];
cx q[21], q[19];
cx q[1], q[28];
cx q[8], q[4];
cx q[18], q[2];
cx q[26], q[28];
cx q[29], q[21];
cx q[17], q[4];
cx q[3], q[23];
cx q[12], q[5];
cx q[8], q[24];
cx q[11], q[6];
cx q[16], q[2];
cx q[22], q[1];
cx q[18], q[15];
cx q[19], q[14];
cx q[27], q[8];
cx q[26], q[19];
cx q[20], q[14];
cx q[6], q[18];
cx q[16], q[4];
cx q[23], q[15];
cx q[25], q[24];
cx q[29], q[5];
cx q[1], q[11];
cx q[21], q[3];
cx q[22], q[2];
cx q[0], q[28];
cx q[23], q[2];
cx q[26], q[11];
cx q[25], q[4];
cx q[5], q[18];
cx q[16], q[8];
cx q[21], q[24];
cx q[17], q[14];
cx q[7], q[0];
cx q[12], q[1];
cx q[15], q[3];
cx q[28], q[27];
cx q[20], q[19];
cx q[28], q[18];
cx q[23], q[5];
cx q[10], q[7];
cx q[26], q[15];
cx q[17], q[2];
cx q[3], q[11];
cx q[19], q[25];
cx q[4], q[8];
cx q[24], q[0];
cx q[27], q[1];
cx q[14], q[21];
