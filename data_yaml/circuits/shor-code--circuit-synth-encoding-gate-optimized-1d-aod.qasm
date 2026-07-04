OPENQASM 2.0;
include "qelib1.inc";

qreg q[9];

h q[3];
h q[6];
barrier q;

cx q[6], q[0];
barrier q;

cx q[3], q[6];
barrier q;

cx q[3], q[5];
cx q[6], q[8];
cx q[0], q[2];
barrier q;

cx q[3], q[4];
cx q[6], q[7];
cx q[0], q[1];
