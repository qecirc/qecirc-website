OPENQASM 2.0;
include "qelib1.inc";

qreg q[17];

h q[1];
h q[8];
h q[5];
h q[7];
cx q[1], q[11];
cx q[8], q[16];
barrier q;

cx q[11], q[3];
cx q[16], q[2];
barrier q;

cx q[11], q[4];
barrier q;

cx q[11], q[0];
barrier q;

cx q[1], q[11];
cx q[8], q[16];
barrier q;

cx q[5], q[14];
cx q[7], q[9];
barrier q;

cx q[14], q[8];
cx q[9], q[1];
barrier q;

cx q[14], q[0];
barrier q;

cx q[14], q[6];
barrier q;

cx q[5], q[14];
cx q[7], q[9];
barrier q;

