OPENQASM 2.0;
include "qelib1.inc";

qreg q[13];

h q[4];
h q[5];
h q[6];
h q[10];
h q[11];
h q[12];
barrier q;

cx q[4], q[3];
cx q[5], q[1];
barrier q;

cx q[4], q[7];
cx q[5], q[8];
cx q[6], q[9];
barrier q;

cx q[5], q[3];
cx q[6], q[1];
barrier q;

cx q[10], q[2];
cx q[11], q[0];
barrier q;

cx q[10], q[4];
cx q[11], q[5];
cx q[12], q[6];
barrier q;

cx q[11], q[2];
cx q[12], q[0];
barrier q;

