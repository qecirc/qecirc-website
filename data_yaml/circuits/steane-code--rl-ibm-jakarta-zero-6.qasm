OPENQASM 2.0;
include "qelib1.inc";

qreg q[7];

sx q[2];
sx q[5];
sx q[6];
cx q[2], q[0];
s q[5];
cx q[0], q[1];
s q[2];
cx q[0], q[3];
cx q[5], q[3];
cx q[3], q[0];
cx q[6], q[5];
cx q[5], q[3];
cx q[1], q[0];
cx q[5], q[4];
cx q[0], q[1];
cx q[3], q[5];
cx q[6], q[5];
s q[6];
