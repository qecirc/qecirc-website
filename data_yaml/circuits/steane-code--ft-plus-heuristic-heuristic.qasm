OPENQASM 2.0;
include "qelib1.inc";

qreg q[8];
creg rec[1];

h q[2];
h q[4];
h q[5];
h q[6];
h q[7];
cx q[5], q[3];
cx q[2], q[0];
cx q[6], q[5];
cx q[4], q[3];
cx q[0], q[1];
cx q[6], q[2];
cx q[5], q[1];
cx q[4], q[0];
cx q[7], q[2];
cx q[7], q[4];
cx q[7], q[5];
h q[7];
measure q[7] -> rec[0]; reset q[7]; // decomposed MR
