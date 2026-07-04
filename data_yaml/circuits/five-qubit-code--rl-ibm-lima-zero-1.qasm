OPENQASM 2.0;
include "qelib1.inc";

qreg q[5];

sx q[4];
sx q[3];
sx q[2];
cx q[3], q[0];
cx q[4], q[1];
cx q[3], q[2];
sx q[1];
x q[0];
cx q[3], q[4];
cx q[4], q[3];
cx q[1], q[4];
cx q[2], q[3];
s q[1];
s q[2];
x q[4];
