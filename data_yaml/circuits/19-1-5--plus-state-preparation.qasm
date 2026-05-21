OPENQASM 2.0;
include "qelib1.inc";

qreg q[19];

reset q[11];
reset q[6];
reset q[5];
reset q[4];
reset q[3];
reset q[18];
reset q[10];
reset q[13];
reset q[8];
reset q[9]; h q[9]; // decomposed RX
reset q[2]; h q[2]; // decomposed RX
reset q[17]; h q[17]; // decomposed RX
reset q[14]; h q[14]; // decomposed RX
reset q[1]; h q[1]; // decomposed RX
reset q[0]; h q[0]; // decomposed RX
reset q[16]; h q[16]; // decomposed RX
reset q[7]; h q[7]; // decomposed RX
reset q[12]; h q[12]; // decomposed RX
reset q[15]; h q[15]; // decomposed RX
cx q[7], q[4];
cx q[1], q[5];
cx q[2], q[11];
cx q[12], q[18];
cx q[15], q[6];
cx q[7], q[8];
cx q[0], q[1];
cx q[17], q[4];
cx q[5], q[11];
cx q[12], q[10];
cx q[15], q[2];
cx q[6], q[3];
cx q[8], q[13];
cx q[16], q[0];
cx q[18], q[1];
cx q[14], q[17];
cx q[5], q[4];
cx q[9], q[11];
cx q[16], q[13];
cx q[11], q[10];
cx q[14], q[3];
cx q[4], q[15];
cx q[0], q[7];
cx q[2], q[18];
cx q[1], q[8];
cx q[17], q[6];
cx q[9], q[12];
