OPENQASM 2.0;
include "qelib1.inc";

qreg q[12];

h q[0];
h q[4];
cx q[0], q[5];
cx q[5], q[2];
cx q[2], q[6];
cx q[0], q[5];
cx q[6], q[8];
cx q[4], q[5];
cx q[5], q[3];
cx q[6], q[7];
cx q[5], q[0];
cx q[7], q[11];
cx q[5], q[2];
cx q[2], q[1];
cx q[2], q[11];
cx q[4], q[11];
