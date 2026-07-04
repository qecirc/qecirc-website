OPENQASM 2.0;
include "qelib1.inc";

qreg q[10];
creg rec[1];

h q[4];
h q[2];
h q[8];
h q[7];
cx q[8], q[6];
cx q[4], q[0];
cx q[8], q[5];
cx q[4], q[1];
cx q[5], q[0];
cx q[7], q[1];
cx q[2], q[8];
cx q[4], q[3];
cx q[4], q[9];
cx q[2], q[9];
cx q[0], q[9];
cx q[8], q[9];
measure q[9] -> rec[0]; reset q[9]; // decomposed MR
