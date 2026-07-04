OPENQASM 2.0;
include "qelib1.inc";

qreg q[11];
creg rec[3];

h q[1];
h q[0];
h q[8];
h q[6];
h q[10];
cx q[6], q[4];
cx q[1], q[7];
cx q[8], q[2];
cx q[4], q[3];
cx q[0], q[6];
cx q[6], q[8];
cx q[3], q[1];
cx q[6], q[5];
cx q[3], q[9];
cx q[10], q[9];
cx q[0], q[9];
cx q[10], q[9];
h q[10];
cx q[5], q[9];
measure q[9] -> rec[0]; reset q[9]; // decomposed MR
measure q[10] -> rec[1]; reset q[10]; // decomposed MR
cx q[4], q[9];
cx q[0], q[9];
cx q[5], q[9];
measure q[9] -> rec[2]; reset q[9]; // decomposed MR
