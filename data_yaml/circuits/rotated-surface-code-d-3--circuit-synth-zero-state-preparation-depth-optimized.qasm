OPENQASM 2.0;
include "qelib1.inc";

qreg q[9];

h q[3];
h q[2];
h q[8];
h q[7];
cx q[8], q[6];
cx q[3], q[0];
cx q[8], q[5];
cx q[3], q[1];
cx q[5], q[0];
cx q[7], q[1];
cx q[2], q[8];
cx q[3], q[4];
