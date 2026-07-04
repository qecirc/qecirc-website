OPENQASM 2.0;
include "qelib1.inc";

qreg q[10];

h q[3];
h q[7];
h q[0];
h q[2];
h q[6];
h q[9];
cx q[3], q[8];
cx q[6], q[1];
cx q[0], q[1];
cx q[6], q[5];
cx q[3], q[4];
cx q[0], q[8];
cx q[7], q[1];
cx q[9], q[1];
cx q[2], q[8];
cx q[9], q[8];
cx q[9], q[0];
h q[9];
