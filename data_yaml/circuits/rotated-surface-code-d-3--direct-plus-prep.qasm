OPENQASM 2.0;
include "qelib1.inc";

qreg q[9];

h q[3];
h q[1];
h q[7];
h q[0];
h q[8];
barrier q;

cx q[0], q[6];
barrier q;

cx q[1], q[6];
barrier q;

cx q[3], q[4];
cx q[7], q[6];
barrier q;

cx q[8], q[2];
barrier q;

cx q[0], q[2];
barrier q;

cx q[6], q[5];
cx q[4], q[2];
barrier q;

