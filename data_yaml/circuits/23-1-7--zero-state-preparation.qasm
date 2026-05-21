OPENQASM 2.0;
include "qelib1.inc";

qreg q[23];

reset q[2];
reset q[1];
reset q[19];
reset q[12];
reset q[14];
reset q[20];
reset q[13];
reset q[9];
reset q[21];
reset q[18];
reset q[17];
reset q[16];
reset q[15]; h q[15]; // decomposed RX
reset q[11]; h q[11]; // decomposed RX
reset q[8]; h q[8]; // decomposed RX
reset q[7]; h q[7]; // decomposed RX
reset q[6]; h q[6]; // decomposed RX
reset q[5]; h q[5]; // decomposed RX
reset q[4]; h q[4]; // decomposed RX
reset q[3]; h q[3]; // decomposed RX
reset q[0]; h q[0]; // decomposed RX
reset q[22]; h q[22]; // decomposed RX
reset q[10]; h q[10]; // decomposed RX
cx q[0], q[9];
cx q[3], q[20];
cx q[4], q[14];
cx q[5], q[12];
cx q[6], q[16];
cx q[7], q[19];
cx q[11], q[21];
cx q[8], q[18];
cx q[15], q[17];
cx q[22], q[4];
cx q[19], q[13];
cx q[0], q[5];
cx q[3], q[1];
cx q[6], q[7];
cx q[11], q[2];
cx q[10], q[8];
cx q[20], q[2];
cx q[14], q[0];
cx q[22], q[6];
cx q[15], q[3];
cx q[4], q[11];
cx q[5], q[19];
cx q[7], q[1];
cx q[21], q[7];
cx q[10], q[3];
cx q[0], q[1];
cx q[12], q[6];
cx q[11], q[5];
cx q[13], q[4];
cx q[20], q[8];
cx q[19], q[15];
cx q[21], q[15];
cx q[18], q[11];
cx q[22], q[7];
cx q[20], q[19];
cx q[5], q[2];
cx q[17], q[4];
cx q[8], q[0];
cx q[1], q[3];
cx q[14], q[6];
cx q[0], q[5];
cx q[15], q[1];
cx q[18], q[19];
cx q[13], q[6];
cx q[20], q[4];
cx q[3], q[7];
cx q[2], q[8];
cx q[16], q[11];
cx q[16], q[19];
cx q[20], q[7];
cx q[18], q[4];
cx q[22], q[15];
cx q[13], q[8];
cx q[9], q[11];
cx q[3], q[2];
cx q[5], q[6];
cx q[1], q[0];
