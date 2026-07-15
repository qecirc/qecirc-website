OPENQASM 2.0;
include "qelib1.inc";

qreg q[16];

h q[3];
h q[1];
h q[7];
h q[0];
h q[8];
h q[10];
h q[15];
h q[12];
h q[13];
barrier q;

cx q[10], q[4];
cx q[12], q[6];
barrier q;

cx q[3], q[10];
cx q[7], q[12];
barrier q;

cx q[1], q[12];
barrier q;

cx q[0], q[12];
barrier q;

cx q[10], q[4];
cx q[12], q[6];
barrier q;

cx q[15], q[5];
cx q[13], q[2];
barrier q;

cx q[6], q[15];
cx q[4], q[13];
barrier q;

cx q[0], q[13];
barrier q;

cx q[8], q[13];
barrier q;

cx q[15], q[5];
cx q[13], q[2];
barrier q;

