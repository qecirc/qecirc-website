OPENQASM 2.0;
include "qelib1.inc";

qreg q[5];

sx q[3];
sx q[4];
sx q[2];
cx q[3], q[1];
cx q[1], q[0];
cx q[4], q[3];
sx q[1];
cx q[4], q[2];
cx q[3], q[1];
cx q[0], q[1];
cx q[3], q[4];
s q[0];
sx q[4];
x q[3];
cx q[1], q[0];
s q[1];
sx q[1];
x q[1];
