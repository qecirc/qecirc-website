OPENQASM 2.0;
include "qelib1.inc";

qreg q[19];

reset q[3];
reset q[2];
reset q[18];
reset q[17];
reset q[14];
reset q[16];
reset q[7];
reset q[12];
reset q[8];
reset q[11]; h q[11]; // decomposed RX
reset q[9]; h q[9]; // decomposed RX
reset q[6]; h q[6]; // decomposed RX
reset q[5]; h q[5]; // decomposed RX
reset q[1]; h q[1]; // decomposed RX
reset q[0]; h q[0]; // decomposed RX
reset q[10]; h q[10]; // decomposed RX
reset q[15]; h q[15]; // decomposed RX
reset q[13]; h q[13]; // decomposed RX
cx q[4], q[3];
cx q[5], q[7];
cx q[6], q[14];
cx q[0], q[16];
cx q[11], q[2];
cx q[1], q[8];
cx q[9], q[12];
cx q[4], q[18];
cx q[5], q[14];
cx q[6], q[3];
cx q[13], q[16];
cx q[15], q[6];
cx q[7], q[4];
cx q[0], q[18];
cx q[11], q[5];
cx q[13], q[8];
cx q[10], q[11];
cx q[0], q[5];
cx q[1], q[7];
cx q[9], q[18];
cx q[2], q[15];
cx q[4], q[17];
cx q[10], q[12];
cx q[15], q[4];
cx q[7], q[0];
cx q[16], q[1];
cx q[6], q[17];
cx q[11], q[9];
cx q[18], q[2];
