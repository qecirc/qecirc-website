OPENQASM 2.0;
include "qelib1.inc";

qreg q[10];
creg rec[1];

h q[2];
h q[7];
cx q[7], q[4];
cx q[4], q[5];
cx q[2], q[7];
cx q[2], q[0];
cx q[4], q[3];
cx q[7], q[8];
cx q[0], q[1];
cx q[7], q[6];
cx q[1], q[9];
cx q[4], q[9];
cx q[7], q[9];
measure q[9] -> rec[0]; reset q[9]; // decomposed MR
