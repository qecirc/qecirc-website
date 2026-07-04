OPENQASM 2.0;
include "qelib1.inc";

qreg q[7];

h q[0];
h q[1];
h q[3];
cx q[0], q[6];
cx q[1], q[5];
cx q[6], q[4];
cx q[3], q[5];
cx q[1], q[6];
cx q[3], q[0];
cx q[0], q[2];
cx q[1], q[2];
