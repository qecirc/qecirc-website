OPENQASM 2.0;
include "qelib1.inc";

qreg q[7];

h q[0];
h q[4];
h q[6];
barrier q;

cx q[4], q[5];
cx q[1], q[2];
cx q[0], q[3];
barrier q;

cx q[6], q[3];
cx q[4], q[1];
cx q[0], q[2];
barrier q;

cx q[6], q[4];
cx q[3], q[5];
cx q[1], q[0];
