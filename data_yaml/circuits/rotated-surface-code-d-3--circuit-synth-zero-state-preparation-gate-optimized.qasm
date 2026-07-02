OPENQASM 2.0;
include "qelib1.inc";

qreg q[9];

h q[3];
h q[2];
h q[1];
h q[0];
cx q[0], q[5];
cx q[1], q[7];
cx q[2], q[8];
cx q[3], q[5];
cx q[3], q[1];
cx q[5], q[6];
cx q[3], q[4];
cx q[5], q[8];
