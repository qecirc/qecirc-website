OPENQASM 2.0;
include "qelib1.inc";

qreg q[15];

reset q[1];
reset q[11];
reset q[13];
reset q[14];
reset q[8]; h q[8]; // decomposed RX
reset q[10]; h q[10]; // decomposed RX
reset q[12]; h q[12]; // decomposed RX
reset q[7]; h q[7]; // decomposed RX
cx q[10], q[4];
cx q[8], q[13];
cx q[7], q[14];
cx q[0], q[1];
cx q[9], q[11];
cx q[12], q[2];
cx q[13], q[10];
cx q[3], q[7];
cx q[0], q[8];
cx q[4], q[1];
cx q[14], q[10];
cx q[6], q[0];
cx q[2], q[4];
cx q[7], q[9];
cx q[12], q[13];
cx q[14], q[11];
cx q[10], q[12];
cx q[5], q[4];
cx q[7], q[0];
cx q[9], q[6];
cx q[2], q[3];
cx q[10], q[9];
cx q[11], q[8];
cx q[13], q[14];
cx q[3], q[5];
cx q[0], q[4];
cx q[2], q[6];
cx q[1], q[3];
cx q[8], q[7];
cx q[4], q[2];
cx q[12], q[11];
