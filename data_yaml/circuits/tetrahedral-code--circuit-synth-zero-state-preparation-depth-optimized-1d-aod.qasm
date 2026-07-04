OPENQASM 2.0;
include "qelib1.inc";

qreg q[15];

h q[7];
h q[3];
h q[1];
h q[0];
barrier q;

cx q[0], q[14];
cx q[1], q[9];
cx q[3], q[11];
barrier q;

cx q[14], q[2];
cx q[9], q[5];
cx q[0], q[10];
cx q[1], q[13];
cx q[7], q[3];
barrier q;

cx q[2], q[4];
cx q[14], q[8];
cx q[11], q[9];
cx q[10], q[12];
cx q[0], q[6];
cx q[7], q[13];
cx q[3], q[1];
barrier q;

cx q[5], q[2];
cx q[11], q[8];
cx q[7], q[12];
cx q[9], q[14];
cx q[13], q[10];
cx q[3], q[0];
cx q[1], q[6];
