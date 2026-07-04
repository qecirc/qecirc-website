OPENQASM 2.0;
include "qelib1.inc";

qreg q[30];
creg rec[13];

h q[13];
h q[7];
h q[6];
h q[5];
h q[3];
h q[2];
h q[0];
h q[4];
h q[22];
h q[23];
h q[24];
cx q[3], q[1];
cx q[4], q[10];
cx q[2], q[11];
cx q[5], q[14];
cx q[3], q[16];
cx q[0], q[10];
cx q[14], q[12];
cx q[4], q[8];
cx q[1], q[2];
cx q[3], q[15];
cx q[6], q[16];
cx q[0], q[9];
cx q[10], q[1];
cx q[5], q[15];
cx q[7], q[3];
cx q[13], q[6];
cx q[11], q[0];
cx q[16], q[12];
cx q[2], q[9];
cx q[7], q[8];
cx q[13], q[5];
cx q[3], q[4];
cx q[6], q[14];
cx q[7], q[17];
cx q[13], q[18];
cx q[2], q[17];
cx q[6], q[18];
cx q[13], q[19];
cx q[7], q[20];
cx q[0], q[17];
cx q[15], q[18];
cx q[6], q[19];
cx q[5], q[20];
cx q[7], q[21];
cx q[22], q[13];
cx q[23], q[2];
cx q[4], q[17];
cx q[12], q[18];
cx q[15], q[19];
cx q[3], q[20];
cx q[22], q[25];
cx q[23], q[28];
cx q[10], q[17];
cx q[12], q[19];
cx q[16], q[20];
cx q[3], q[21];
measure q[18] -> rec[0]; reset q[18]; // decomposed MR
cx q[22], q[7];
cx q[14], q[20];
cx q[0], q[21];
measure q[17] -> rec[1]; reset q[17]; // decomposed MR
measure q[19] -> rec[2]; reset q[19]; // decomposed MR
cx q[22], q[26];
cx q[24], q[7];
cx q[9], q[21];
measure q[20] -> rec[3]; reset q[20]; // decomposed MR
cx q[22], q[1];
cx q[24], q[29];
measure q[21] -> rec[4]; reset q[21]; // decomposed MR
cx q[22], q[4];
cx q[24], q[3];
cx q[22], q[27];
cx q[23], q[4];
cx q[22], q[9];
cx q[24], q[4];
cx q[22], q[11];
cx q[24], q[29];
cx q[22], q[25];
cx q[23], q[11];
measure q[29] -> rec[5]; reset q[29]; // decomposed MR
measure q[25] -> rec[6]; reset q[25]; // decomposed MR
cx q[22], q[14];
cx q[23], q[28];
cx q[22], q[27];
measure q[28] -> rec[7]; reset q[28]; // decomposed MR
cx q[23], q[8];
measure q[27] -> rec[8]; reset q[27]; // decomposed MR
cx q[22], q[26];
h q[23];
cx q[24], q[8];
measure q[26] -> rec[9]; reset q[26]; // decomposed MR
cx q[22], q[12];
measure q[23] -> rec[10]; reset q[23]; // decomposed MR
h q[24];
h q[22];
measure q[24] -> rec[11]; reset q[24]; // decomposed MR
measure q[22] -> rec[12]; reset q[22]; // decomposed MR
