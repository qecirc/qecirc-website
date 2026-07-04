OPENQASM 2.0;
include "qelib1.inc";

qreg q[7];

sx q[3];
sx q[1];
sx q[4];
cx q[3], q[0];
cx q[3], q[5];
cx q[1], q[0];
cx q[5], q[6];
cx q[0], q[3];
s q[5];
cx q[0], q[2];
cx q[4], q[5];
cx q[1], q[0];
cx q[3], q[5];
s q[4];
s q[1];
cx q[5], q[3];
cx q[5], q[6];
