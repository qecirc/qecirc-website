OPENQASM 2.0;
include "qelib1.inc";

qreg q[13];
creg rec[6];

h q[7];
h q[3];
h q[2];
h q[1];
h q[0];
cx q[0], q[6];
cx q[1], q[8];
cx q[0], q[9];
cx q[2], q[6];
cx q[7], q[8];
cx q[1], q[5];
cx q[0], q[4];
cx q[3], q[9];
cx q[6], q[8];
cx q[3], q[4];
cx q[9], q[10];
cx q[3], q[6];
cx q[7], q[9];
cx q[4], q[5];
cx q[8], q[10];
cx q[7], q[11];
cx q[8], q[12];
cx q[3], q[11];
cx q[2], q[11];
cx q[1], q[11];
cx q[10], q[11];
cx q[10], q[12];
measure q[11] -> rec[0]; reset q[11]; // decomposed MR
cx q[4], q[12];
cx q[0], q[11];
measure q[12] -> rec[1]; reset q[12]; // decomposed MR
cx q[5], q[11];
cx q[9], q[11];
cx q[10], q[11];
cx q[6], q[11];
measure q[11] -> rec[2]; reset q[11]; // decomposed MR
h q[11];
cx q[11], q[3];
cx q[11], q[12];
cx q[11], q[1];
cx q[11], q[0];
cx q[11], q[12];
cx q[11], q[5];
measure q[12] -> rec[3]; reset q[12]; // decomposed MR
h q[11];
measure q[11] -> rec[4]; reset q[11]; // decomposed MR
h q[11];
cx q[11], q[7];
cx q[11], q[2];
cx q[11], q[9];
cx q[11], q[6];
h q[11];
measure q[11] -> rec[5]; reset q[11]; // decomposed MR
