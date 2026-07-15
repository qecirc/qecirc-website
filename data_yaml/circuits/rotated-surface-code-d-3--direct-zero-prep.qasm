OPENQASM 2.0;
include "qelib1.inc";

qreg q[9];

h q[1];
h q[8];
h q[5];
h q[7];
barrier q;

cx q[1], q[0];
barrier q;

cx q[1], q[4];
barrier q;

cx q[1], q[3];
cx q[8], q[2];
barrier q;

cx q[5], q[6];
barrier q;

cx q[5], q[0];
barrier q;

cx q[5], q[8];
cx q[7], q[1];
barrier q;

