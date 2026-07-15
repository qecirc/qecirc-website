OPENQASM 2.0;
include "qelib1.inc";

qreg q[13];

h q[7];
h q[4];
h q[10];
h q[3];
h q[2];
h q[1];
h q[0];
barrier q;

cx q[3], q[8];
cx q[2], q[5];
barrier q;

cx q[7], q[8];
cx q[4], q[5];
cx q[10], q[11];
barrier q;

cx q[3], q[5];
cx q[2], q[11];
barrier q;

cx q[1], q[9];
cx q[0], q[6];
barrier q;

cx q[8], q[9];
cx q[5], q[6];
cx q[11], q[12];
barrier q;

cx q[1], q[6];
cx q[0], q[12];
barrier q;

