OPENQASM 2.0;
include "qelib1.inc";

qreg q[10];

h q[3];
h q[7];
h q[5];
h q[8];
cx q[5], q[6];
cx q[8], q[2];
cx q[3], q[0];
cx q[7], q[1];
cx q[5], q[0];
cx q[3], q[7];
cx q[3], q[4];
cx q[5], q[2];
cx q[4], q[9];
cx q[5], q[9];
cx q[0], q[9];
