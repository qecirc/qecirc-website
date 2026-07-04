OPENQASM 2.0;
include "qelib1.inc";

qreg q[43];
creg rec[24];

h q[11];
h q[9];
h q[6];
h q[5];
h q[4];
h q[3];
h q[2];
h q[1];
h q[16];
h q[25];
h q[26];
h q[27];
h q[28];
h q[29];
h q[30];
cx q[2], q[15];
cx q[4], q[7];
cx q[5], q[18];
cx q[16], q[13];
cx q[1], q[8];
cx q[9], q[12];
cx q[11], q[10];
cx q[18], q[0];
cx q[2], q[5];
cx q[4], q[17];
cx q[6], q[15];
cx q[1], q[7];
cx q[13], q[8];
cx q[10], q[12];
cx q[0], q[16];
cx q[17], q[14];
cx q[2], q[11];
cx q[3], q[6];
cx q[4], q[5];
cx q[9], q[18];
cx q[3], q[14];
cx q[15], q[4];
cx q[7], q[0];
cx q[16], q[1];
cx q[18], q[2];
cx q[6], q[17];
cx q[11], q[9];
cx q[11], q[19];
cx q[4], q[20];
cx q[9], q[22];
cx q[3], q[19];
cx q[11], q[21];
cx q[9], q[23];
cx q[4], q[24];
cx q[2], q[19];
cx q[3], q[20];
cx q[6], q[21];
cx q[25], q[9];
cx q[27], q[11];
cx q[14], q[19];
cx q[2], q[20];
cx q[5], q[21];
cx q[6], q[23];
cx q[25], q[31];
cx q[26], q[9];
cx q[27], q[36];
cx q[30], q[11];
cx q[16], q[19];
cx q[18], q[20];
cx q[2], q[22];
cx q[3], q[23];
cx q[25], q[6];
cx q[26], q[34];
cx q[27], q[9];
cx q[30], q[41];
cx q[7], q[19];
cx q[17], q[20];
cx q[18], q[21];
cx q[0], q[22];
cx q[3], q[24];
cx q[25], q[32];
cx q[26], q[5];
cx q[28], q[9];
cx q[29], q[6];
cx q[12], q[19];
cx q[17], q[21];
cx q[7], q[22];
cx q[14], q[24];
measure q[20] -> rec[0]; reset q[20]; // decomposed MR
cx q[25], q[4];
cx q[26], q[35];
cx q[28], q[37];
cx q[29], q[39];
cx q[8], q[19];
cx q[12], q[21];
cx q[10], q[22];
cx q[25], q[3];
cx q[28], q[5];
cx q[12], q[23];
measure q[19] -> rec[1]; reset q[19]; // decomposed MR
measure q[21] -> rec[2]; reset q[21]; // decomposed MR
measure q[22] -> rec[3]; reset q[22]; // decomposed MR
cx q[25], q[33];
cx q[26], q[3];
cx q[28], q[38];
cx q[29], q[5];
cx q[15], q[23];
cx q[25], q[1];
cx q[26], q[18];
cx q[28], q[16];
cx q[29], q[40];
cx q[30], q[5];
cx q[15], q[24];
measure q[23] -> rec[4]; reset q[23]; // decomposed MR
cx q[25], q[0];
cx q[26], q[34];
cx q[28], q[7];
cx q[30], q[42];
measure q[24] -> rec[5]; reset q[24]; // decomposed MR
cx q[25], q[31];
measure q[34] -> rec[6]; reset q[34]; // decomposed MR
cx q[26], q[14];
cx q[28], q[37];
cx q[30], q[3];
measure q[31] -> rec[7]; reset q[31]; // decomposed MR
cx q[25], q[12];
cx q[26], q[35];
measure q[37] -> rec[8]; reset q[37]; // decomposed MR
cx q[29], q[14];
cx q[30], q[18];
cx q[25], q[33];
measure q[35] -> rec[9]; reset q[35]; // decomposed MR
cx q[26], q[10];
cx q[29], q[16];
cx q[30], q[41];
measure q[33] -> rec[10]; reset q[33]; // decomposed MR
cx q[25], q[32];
h q[26];
cx q[27], q[10];
cx q[29], q[39];
measure q[41] -> rec[11]; reset q[41]; // decomposed MR
cx q[30], q[14];
measure q[32] -> rec[12]; reset q[32]; // decomposed MR
cx q[25], q[13];
measure q[26] -> rec[13]; reset q[26]; // decomposed MR
cx q[27], q[36];
measure q[39] -> rec[14]; reset q[39]; // decomposed MR
cx q[29], q[15];
cx q[30], q[42];
h q[25];
measure q[36] -> rec[15]; reset q[36]; // decomposed MR
cx q[27], q[12];
cx q[29], q[40];
measure q[42] -> rec[16]; reset q[42]; // decomposed MR
measure q[25] -> rec[17]; reset q[25]; // decomposed MR
h q[27];
cx q[28], q[12];
measure q[40] -> rec[18]; reset q[40]; // decomposed MR
cx q[29], q[13];
measure q[27] -> rec[19]; reset q[27]; // decomposed MR
cx q[28], q[38];
h q[29];
cx q[30], q[12];
measure q[38] -> rec[20]; reset q[38]; // decomposed MR
cx q[28], q[8];
measure q[29] -> rec[21]; reset q[29]; // decomposed MR
h q[30];
h q[28];
measure q[30] -> rec[22]; reset q[30]; // decomposed MR
measure q[28] -> rec[23]; reset q[28]; // decomposed MR
