OPENQASM 2.0;
include "qelib1.inc";

qreg q[8];
creg rec[1];

h q[0];
h q[3];
h q[5];
cx q[3], q[1];
cx q[5], q[4];
cx q[0], q[2];
cx q[4], q[3];
cx q[1], q[0];
cx q[1], q[6];
cx q[2], q[4];
cx q[4], q[6];
cx q[2], q[7];
cx q[3], q[7];
cx q[6], q[7];
measure q[7] -> rec[0]; reset q[7]; // decomposed MR
