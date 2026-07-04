OPENQASM 2.0;
include "qelib1.inc";

qreg q[7];

h q[0];
h q[1];
h q[3];
barrier q;

cx q[3], q[5];
cx q[0], q[2];
barrier q;

cx q[5], q[6];
cx q[3], q[4];
cx q[1], q[0];
barrier q;

cx q[2], q[6];
cx q[1], q[5];
cx q[0], q[4];
