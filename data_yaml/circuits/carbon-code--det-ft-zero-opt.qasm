OPENQASM 2.0;
include "qelib1.inc";

qreg q[15];
creg rec[7];

h q[2];
h q[4];
h q[3];
h q[6];
h q[10];
cx q[2], q[8];
cx q[6], q[7];
cx q[4], q[5];
cx q[3], q[9];
cx q[8], q[0];
cx q[5], q[11];
cx q[7], q[1];
cx q[9], q[2];
cx q[8], q[6];
cx q[10], q[5];
cx q[8], q[4];
cx q[10], q[3];
cx q[10], q[7];
cx q[3], q[8];
cx q[4], q[10];
cx q[7], q[0];
cx q[0], q[12];
cx q[4], q[12];
cx q[0], q[14];
cx q[1], q[12];
cx q[3], q[12];
cx q[9], q[12];
cx q[11], q[12];
measure q[12] -> rec[0]; reset q[12]; // decomposed MR
cx q[4], q[12];
cx q[3], q[12];
cx q[4], q[13];
cx q[10], q[12];
cx q[1], q[13];
cx q[4], q[14];
cx q[9], q[12];
cx q[6], q[13];
cx q[7], q[14];
cx q[11], q[13];
measure q[12] -> rec[1]; reset q[12]; // decomposed MR
cx q[11], q[14];
measure q[13] -> rec[2]; reset q[13]; // decomposed MR
h q[12];
measure q[14] -> rec[3]; reset q[14]; // decomposed MR
cx q[12], q[0];
cx q[12], q[13];
cx q[12], q[2];
cx q[12], q[1];
cx q[12], q[3];
cx q[12], q[10];
cx q[12], q[13];
cx q[12], q[11];
measure q[13] -> rec[4]; reset q[13]; // decomposed MR
h q[12];
measure q[12] -> rec[5]; reset q[12]; // decomposed MR
h q[12];
cx q[12], q[4];
cx q[12], q[5];
cx q[12], q[6];
cx q[12], q[8];
cx q[12], q[7];
cx q[12], q[9];
h q[12];
measure q[12] -> rec[6]; reset q[12]; // decomposed MR
