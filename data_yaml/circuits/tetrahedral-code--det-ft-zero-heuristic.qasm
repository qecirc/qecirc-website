OPENQASM 2.0;
include "qelib1.inc";

qreg q[17];
creg rec[4];

h q[3];
h q[12];
h q[10];
h q[9];
h q[16];
cx q[12], q[4];
cx q[10], q[14];
cx q[9], q[6];
cx q[3], q[14];
cx q[6], q[1];
cx q[10], q[8];
cx q[14], q[12];
cx q[4], q[1];
cx q[9], q[10];
cx q[3], q[0];
cx q[10], q[11];
cx q[0], q[2];
cx q[12], q[9];
cx q[4], q[3];
cx q[14], q[10];
cx q[11], q[13];
cx q[0], q[15];
cx q[1], q[11];
cx q[10], q[5];
cx q[14], q[7];
cx q[16], q[15];
cx q[12], q[10];
cx q[6], q[14];
cx q[1], q[2];
cx q[6], q[15];
cx q[16], q[15];
h q[16];
cx q[5], q[15];
measure q[15] -> rec[0]; reset q[15]; // decomposed MR
measure q[16] -> rec[1]; reset q[16]; // decomposed MR
cx q[2], q[15];
cx q[13], q[16];
cx q[14], q[15];
cx q[10], q[16];
cx q[11], q[15];
cx q[4], q[16];
measure q[15] -> rec[2]; reset q[15]; // decomposed MR
measure q[16] -> rec[3]; reset q[16]; // decomposed MR
