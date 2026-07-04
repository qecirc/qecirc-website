OPENQASM 2.0;
include "qelib1.inc";

qreg q[9];

h q[0];
h q[3];
barrier q;

cx q[3], q[6];
barrier q;

cx q[0], q[6];
barrier q;

cx q[3], q[5];
cx q[0], q[2];
cx q[6], q[8];
barrier q;

cx q[3], q[4];
cx q[0], q[1];
cx q[6], q[7];
