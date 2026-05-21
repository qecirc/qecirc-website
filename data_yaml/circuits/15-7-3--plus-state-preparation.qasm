OPENQASM 2.0;
include "qelib1.inc";

qreg q[15];

reset q[0];
reset q[1];
reset q[3];
reset q[7];
reset q[2]; h q[2]; // decomposed RX
reset q[4]; h q[4]; // decomposed RX
reset q[5]; h q[5]; // decomposed RX
reset q[6]; h q[6]; // decomposed RX
reset q[8]; h q[8]; // decomposed RX
reset q[9]; h q[9]; // decomposed RX
reset q[10]; h q[10]; // decomposed RX
reset q[11]; h q[11]; // decomposed RX
reset q[12]; h q[12]; // decomposed RX
reset q[13]; h q[13]; // decomposed RX
reset q[14]; h q[14]; // decomposed RX
cx q[13], q[3];
cx q[9], q[1];
cx q[10], q[0];
cx q[12], q[10];
cx q[9], q[7];
cx q[11], q[3];
cx q[5], q[1];
cx q[6], q[0];
cx q[14], q[13];
cx q[11], q[7];
cx q[8], q[6];
cx q[5], q[3];
cx q[2], q[1];
cx q[4], q[0];
cx q[10], q[9];
cx q[8], q[7];
cx q[4], q[3];
cx q[2], q[0];
cx q[6], q[5];
cx q[13], q[9];
cx q[12], q[11];
cx q[14], q[10];
