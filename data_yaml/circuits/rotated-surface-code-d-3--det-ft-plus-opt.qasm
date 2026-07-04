OPENQASM 2.0;
include "qelib1.inc";

qreg q[11];
creg rec[3];

h q[4];
h q[1];
h q[0];
h q[8];
h q[5];
h q[9];
cx q[4], q[3];
cx q[0], q[2];
cx q[5], q[6];
cx q[1], q[7];
cx q[3], q[2];
cx q[8], q[0];
cx q[6], q[1];
cx q[0], q[7];
cx q[9], q[2];
cx q[9], q[10];
cx q[9], q[1];
cx q[9], q[10];
cx q[9], q[0];
measure q[10] -> rec[0]; reset q[10]; // decomposed MR
h q[9];
measure q[9] -> rec[1]; reset q[9]; // decomposed MR
h q[9];
cx q[9], q[1];
cx q[9], q[0];
cx q[9], q[8];
h q[9];
measure q[9] -> rec[2]; reset q[9]; // decomposed MR
