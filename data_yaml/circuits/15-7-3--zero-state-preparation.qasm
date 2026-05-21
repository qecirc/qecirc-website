OPENQASM 2.0;
include "qelib1.inc";

qreg q[15];

reset q[2];
reset q[4];
reset q[5];
reset q[6];
reset q[8];
reset q[9];
reset q[10];
reset q[11];
reset q[12];
reset q[13];
reset q[14];
reset q[0]; h q[0]; // decomposed RX
reset q[1]; h q[1]; // decomposed RX
reset q[3]; h q[3]; // decomposed RX
reset q[7]; h q[7]; // decomposed RX
cx q[3], q[13];
cx q[1], q[9];
cx q[0], q[10];
cx q[10], q[12];
cx q[7], q[9];
cx q[3], q[11];
cx q[1], q[5];
cx q[0], q[6];
cx q[13], q[14];
cx q[7], q[11];
cx q[6], q[8];
cx q[3], q[5];
cx q[1], q[2];
cx q[0], q[4];
cx q[9], q[10];
cx q[7], q[8];
cx q[3], q[4];
cx q[0], q[2];
cx q[5], q[6];
cx q[9], q[13];
cx q[11], q[12];
cx q[10], q[14];
