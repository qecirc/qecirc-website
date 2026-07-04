OPENQASM 2.0;
include "qelib1.inc";

qreg q[7];

sx q[0];
sx q[6];
cx q[0], q[2];
cx q[6], q[5];
s q[6];
s q[0];
cx q[0], q[3];
cx q[3], q[5];
cx q[0], q[1];
cx q[5], q[4];
sx q[3];
cx q[3], q[0];
cx q[3], q[5];
cx q[5], q[3];
cx q[0], q[3];
cx q[0], q[2];
s q[0];
