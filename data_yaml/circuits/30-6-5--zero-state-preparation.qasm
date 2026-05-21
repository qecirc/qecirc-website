OPENQASM 2.0;
include "qelib1.inc";

qreg q[30];

reset q[4];
reset q[2];
reset q[1];
reset q[0];
reset q[24];
reset q[15];
reset q[9];
reset q[23];
reset q[29];
reset q[21];
reset q[27];
reset q[28];
reset q[20];
reset q[25];
reset q[19];
reset q[14];
reset q[8];
reset q[11];
reset q[22]; h q[22]; // decomposed RX
reset q[16]; h q[16]; // decomposed RX
reset q[13]; h q[13]; // decomposed RX
reset q[10]; h q[10]; // decomposed RX
reset q[7]; h q[7]; // decomposed RX
reset q[6]; h q[6]; // decomposed RX
reset q[5]; h q[5]; // decomposed RX
reset q[3]; h q[3]; // decomposed RX
reset q[18]; h q[18]; // decomposed RX
reset q[12]; h q[12]; // decomposed RX
reset q[17]; h q[17]; // decomposed RX
reset q[26]; h q[26]; // decomposed RX
cx q[26], q[28];
cx q[17], q[8];
cx q[12], q[14];
cx q[18], q[23];
cx q[5], q[29];
cx q[10], q[1];
cx q[3], q[9];
cx q[22], q[19];
cx q[23], q[25];
cx q[12], q[11];
cx q[5], q[0];
cx q[6], q[14];
cx q[7], q[8];
cx q[10], q[28];
cx q[13], q[1];
cx q[16], q[18];
cx q[29], q[20];
cx q[17], q[5];
cx q[12], q[25];
cx q[9], q[11];
cx q[6], q[3];
cx q[10], q[15];
cx q[1], q[0];
cx q[18], q[4];
cx q[28], q[24];
cx q[8], q[21];
cx q[22], q[20];
cx q[23], q[5];
cx q[16], q[8];
cx q[3], q[15];
cx q[1], q[14];
cx q[28], q[18];
cx q[24], q[25];
cx q[21], q[27];
cx q[11], q[2];
cx q[0], q[4];
cx q[17], q[19];
cx q[5], q[21];
cx q[13], q[2];
cx q[3], q[28];
cx q[7], q[24];
cx q[18], q[1];
cx q[27], q[11];
cx q[25], q[15];
cx q[19], q[0];
cx q[8], q[14];
cx q[4], q[20];
cx q[26], q[19];
cx q[12], q[5];
cx q[13], q[27];
cx q[16], q[24];
cx q[22], q[25];
cx q[15], q[4];
cx q[8], q[3];
cx q[0], q[18];
cx q[20], q[28];
cx q[11], q[1];
cx q[14], q[21];
cx q[17], q[2];
cx q[5], q[3];
cx q[20], q[2];
cx q[21], q[24];
cx q[28], q[27];
cx q[18], q[11];
cx q[14], q[19];
cx q[4], q[8];
cx q[1], q[25];
cx q[15], q[0];
