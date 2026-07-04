OPENQASM 2.0;
include "qelib1.inc";

qreg q[17];

h q[3];
h q[7];
h q[5];
h q[8];
cx q[3], q[10];
cx q[7], q[12];
cx q[8], q[16];
cx q[5], q[14];
cx q[10], q[1];
cx q[16], q[2];
cx q[10], q[4];
cx q[12], q[1];
cx q[8], q[16];
cx q[10], q[0];
cx q[7], q[12];
cx q[3], q[10];
cx q[14], q[0];
cx q[14], q[6];
cx q[14], q[8];
cx q[5], q[14];
