OPENQASM 2.0;
include "qelib1.inc";

qreg q[20];
creg rec[10];

h q[12];
h q[10];
h q[8];
h q[4];
h q[2];
h q[1];
h q[0];
cx q[1], q[3];
cx q[8], q[15];
cx q[0], q[6];
cx q[4], q[5];
cx q[10], q[11];
cx q[2], q[3];
cx q[1], q[7];
cx q[12], q[15];
cx q[0], q[5];
cx q[3], q[9];
cx q[2], q[6];
cx q[4], q[7];
cx q[15], q[14];
cx q[1], q[5];
cx q[9], q[13];
cx q[3], q[11];
cx q[2], q[7];
cx q[4], q[6];
cx q[10], q[14];
cx q[0], q[3];
cx q[8], q[9];
cx q[12], q[13];
cx q[11], q[15];
cx q[4], q[17];
cx q[12], q[16];
cx q[2], q[17];
cx q[11], q[16];
cx q[5], q[17];
cx q[9], q[16];
cx q[3], q[17];
cx q[14], q[16];
measure q[17] -> rec[0]; reset q[17]; // decomposed MR
measure q[16] -> rec[1]; reset q[16]; // decomposed MR
cx q[10], q[17];
cx q[1], q[16];
cx q[2], q[17];
cx q[0], q[16];
cx q[1], q[17];
cx q[6], q[16];
cx q[11], q[17];
cx q[7], q[16];
measure q[17] -> rec[2]; reset q[17]; // decomposed MR
measure q[16] -> rec[3]; reset q[16]; // decomposed MR
h q[17];
h q[16];
cx q[17], q[12];
cx q[16], q[2];
cx q[17], q[19];
cx q[16], q[18];
cx q[17], q[10];
cx q[16], q[1];
cx q[17], q[4];
cx q[16], q[6];
cx q[17], q[1];
cx q[16], q[18];
cx q[17], q[6];
cx q[16], q[5];
cx q[17], q[15];
measure q[18] -> rec[4]; reset q[18]; // decomposed MR
h q[16];
cx q[17], q[3];
cx q[17], q[19];
measure q[16] -> rec[5]; reset q[16]; // decomposed MR
cx q[17], q[9];
measure q[19] -> rec[6]; reset q[19]; // decomposed MR
h q[16];
h q[17];
cx q[16], q[12];
measure q[17] -> rec[7]; reset q[17]; // decomposed MR
cx q[16], q[15];
cx q[16], q[13];
h q[17];
cx q[16], q[14];
cx q[17], q[8];
h q[16];
cx q[17], q[2];
cx q[17], q[0];
measure q[16] -> rec[8]; reset q[16]; // decomposed MR
cx q[17], q[7];
cx q[17], q[11];
cx q[17], q[5];
cx q[17], q[13];
cx q[17], q[14];
h q[17];
measure q[17] -> rec[9]; reset q[17]; // decomposed MR
