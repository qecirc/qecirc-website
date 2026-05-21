OPENQASM 2.0;
include "qelib1.inc";

qreg q[17];

reset q[13];
reset q[7];
reset q[6];
reset q[5];
reset q[3];
reset q[2];
reset q[0];
reset q[4];
reset q[16]; h q[16]; // decomposed RX
reset q[15]; h q[15]; // decomposed RX
reset q[1]; h q[1]; // decomposed RX
reset q[9]; h q[9]; // decomposed RX
reset q[11]; h q[11]; // decomposed RX
reset q[8]; h q[8]; // decomposed RX
reset q[14]; h q[14]; // decomposed RX
reset q[10]; h q[10]; // decomposed RX
reset q[12]; h q[12]; // decomposed RX
cx q[10], q[4];
cx q[15], q[3];
cx q[11], q[2];
cx q[14], q[5];
cx q[12], q[6];
cx q[10], q[0];
cx q[1], q[15];
cx q[16], q[3];
cx q[8], q[4];
cx q[6], q[13];
cx q[16], q[12];
cx q[9], q[0];
cx q[2], q[1];
cx q[15], q[5];
cx q[3], q[7];
cx q[14], q[6];
cx q[0], q[11];
cx q[8], q[7];
cx q[5], q[13];
cx q[4], q[3];
cx q[12], q[15];
cx q[1], q[10];
cx q[9], q[2];
