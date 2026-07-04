OPENQASM 2.0;
include "qelib1.inc";

qreg q[9];

h q[1];
h q[8];
h q[7];
h q[5];
barrier q;

cx q[1], q[0];
cx q[3], q[2];
barrier q;

cx q[5], q[6];
cx q[8], q[2];
cx q[1], q[3];
barrier q;

cx q[6], q[8];
cx q[5], q[0];
cx q[7], q[1];
cx q[3], q[4];
