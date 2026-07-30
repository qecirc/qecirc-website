OPENQASM 2.0;
include "qelib1.inc";

qreg q[18];
creg rec[8];

h q[0];
h q[1];
h q[3];
h q[7];
h q[11];
cx q[3], q[12];
cx q[1], q[9];
cx q[0], q[8];
cx q[12], q[14];
cx q[11], q[8];
cx q[9], q[10];
cx q[7], q[3];
cx q[1], q[5];
cx q[0], q[4];
cx q[14], q[15];
cx q[12], q[13];
cx q[11], q[10];
cx q[7], q[4];
cx q[5], q[6];
cx q[1], q[2];
cx q[8], q[9];
cx q[3], q[0];
cx q[11], q[15];
cx q[7], q[6];
cx q[10], q[14];
cx q[8], q[12];
cx q[4], q[5];
cx q[3], q[2];
cx q[9], q[13];
cx q[0], q[1];
cx q[1], q[16];
cx q[3], q[17];
cx q[7], q[16];
cx q[5], q[17];
cx q[8], q[16];
cx q[11], q[17];
cx q[14], q[16];
cx q[13], q[17];
measure q[16] -> rec[0]; reset q[16]; // decomposed MR
measure q[17] -> rec[1]; reset q[17]; // decomposed MR
cx q[1], q[16];
cx q[4], q[17];
cx q[3], q[16];
cx q[5], q[17];
cx q[13], q[16];
cx q[8], q[17];
cx q[15], q[16];
cx q[9], q[17];
measure q[16] -> rec[2]; reset q[16]; // decomposed MR
measure q[17] -> rec[3]; reset q[17]; // decomposed MR
h q[16];
cx q[16], q[1];
cx q[16], q[17];
cx q[16], q[3];
cx q[16], q[4];
cx q[16], q[6];
cx q[16], q[8];
cx q[16], q[10];
cx q[16], q[13];
cx q[16], q[17];
cx q[16], q[15];
measure q[17] -> rec[4]; reset q[17]; // decomposed MR
h q[16];
cx q[1], q[17];
measure q[16] -> rec[5]; reset q[16]; // decomposed MR
cx q[6], q[16];
cx q[7], q[16];
cx q[12], q[16];
cx q[7], q[17];
cx q[13], q[16];
cx q[10], q[17];
cx q[12], q[17];
measure q[16] -> rec[6]; reset q[16]; // decomposed MR
measure q[17] -> rec[7]; reset q[17]; // decomposed MR
