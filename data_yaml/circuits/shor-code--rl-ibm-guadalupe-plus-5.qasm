OPENQASM 2.0;
include "qelib1.inc";

qreg q[9];

sx q[1];
sx q[3];
cx q[1], q[8];
cx q[3], q[5];
cx q[1], q[0];
cx q[8], q[7];
cx q[3], q[4];
cx q[0], q[2];
cx q[5], q[7];
cx q[1], q[8];
s q[4];
cx q[7], q[8];
s q[2];
cx q[7], q[6];
