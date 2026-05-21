OPENQASM 2.0;
include "qelib1.inc";

qreg q[23];

reset q[15];
reset q[11];
reset q[8];
reset q[7];
reset q[6];
reset q[5];
reset q[4];
reset q[3];
reset q[0];
reset q[22];
reset q[10];
reset q[2]; h q[2]; // decomposed RX
reset q[1]; h q[1]; // decomposed RX
reset q[19]; h q[19]; // decomposed RX
reset q[12]; h q[12]; // decomposed RX
reset q[14]; h q[14]; // decomposed RX
reset q[20]; h q[20]; // decomposed RX
reset q[13]; h q[13]; // decomposed RX
reset q[9]; h q[9]; // decomposed RX
reset q[21]; h q[21]; // decomposed RX
reset q[18]; h q[18]; // decomposed RX
reset q[17]; h q[17]; // decomposed RX
reset q[16]; h q[16]; // decomposed RX
cx q[9], q[0];
cx q[20], q[3];
cx q[14], q[4];
cx q[12], q[5];
cx q[16], q[6];
cx q[19], q[7];
cx q[21], q[11];
cx q[18], q[8];
cx q[17], q[15];
cx q[4], q[22];
cx q[13], q[19];
cx q[5], q[0];
cx q[1], q[3];
cx q[7], q[6];
cx q[2], q[11];
cx q[8], q[10];
cx q[2], q[20];
cx q[0], q[14];
cx q[6], q[22];
cx q[3], q[15];
cx q[11], q[4];
cx q[19], q[5];
cx q[1], q[7];
cx q[7], q[21];
cx q[3], q[10];
cx q[1], q[0];
cx q[6], q[12];
cx q[5], q[11];
cx q[4], q[13];
cx q[8], q[20];
cx q[15], q[19];
cx q[15], q[21];
cx q[11], q[18];
cx q[7], q[22];
cx q[19], q[20];
cx q[2], q[5];
cx q[4], q[17];
cx q[0], q[8];
cx q[3], q[1];
cx q[6], q[14];
cx q[5], q[0];
cx q[1], q[15];
cx q[19], q[18];
cx q[6], q[13];
cx q[4], q[20];
cx q[7], q[3];
cx q[8], q[2];
cx q[11], q[16];
cx q[19], q[16];
cx q[7], q[20];
cx q[4], q[18];
cx q[15], q[22];
cx q[8], q[13];
cx q[11], q[9];
cx q[2], q[3];
cx q[6], q[5];
cx q[0], q[1];
