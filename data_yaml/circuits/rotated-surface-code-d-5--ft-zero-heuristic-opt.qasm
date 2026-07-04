OPENQASM 2.0;
include "qelib1.inc";

qreg q[42];
creg rec[17];

h q[11];
h q[14];
h q[3];
h q[18];
h q[13];
h q[23];
h q[22];
h q[20];
h q[16];
h q[1];
h q[5];
h q[2];
h q[30];
h q[31];
h q[32];
h q[33];
cx q[3], q[24];
cx q[14], q[6];
cx q[18], q[17];
cx q[13], q[12];
cx q[23], q[10];
cx q[22], q[9];
cx q[20], q[19];
cx q[16], q[15];
cx q[1], q[21];
cx q[14], q[3];
cx q[18], q[24];
cx q[23], q[0];
cx q[22], q[4];
cx q[20], q[10];
cx q[1], q[8];
cx q[2], q[21];
cx q[11], q[14];
cx q[6], q[23];
cx q[0], q[4];
cx q[22], q[7];
cx q[1], q[9];
cx q[5], q[8];
cx q[3], q[25];
cx q[13], q[6];
cx q[17], q[0];
cx q[12], q[22];
cx q[16], q[7];
cx q[19], q[1];
cx q[15], q[5];
cx q[24], q[25];
cx q[3], q[27];
cx q[30], q[14];
cx q[6], q[25];
cx q[24], q[27];
cx q[31], q[14];
cx q[30], q[34];
cx q[0], q[25];
cx q[23], q[27];
cx q[6], q[28];
cx q[30], q[24];
cx q[31], q[38];
cx q[12], q[25];
cx q[0], q[26];
cx q[23], q[28];
cx q[31], q[24];
cx q[30], q[35];
cx q[10], q[25];
cx q[17], q[26];
cx q[0], q[27];
cx q[22], q[28];
cx q[30], q[6];
cx q[7], q[25];
cx q[10], q[26];
cx q[30], q[0];
cx q[31], q[6];
measure q[27] -> rec[0]; reset q[27]; // decomposed MR
cx q[9], q[25];
cx q[16], q[26];
cx q[10], q[28];
cx q[30], q[36];
cx q[31], q[38];
cx q[19], q[25];
cx q[7], q[26];
cx q[30], q[22];
cx q[31], q[23];
measure q[38] -> rec[1]; reset q[38]; // decomposed MR
cx q[5], q[25];
cx q[9], q[26];
cx q[7], q[29];
cx q[30], q[10];
h q[31];
cx q[32], q[23];
cx q[8], q[25];
cx q[1], q[26];
cx q[9], q[28];
cx q[30], q[37];
cx q[32], q[39];
measure q[31] -> rec[2]; reset q[31]; // decomposed MR
cx q[1], q[28];
cx q[9], q[29];
cx q[30], q[7];
cx q[32], q[0];
measure q[25] -> rec[3]; reset q[25]; // decomposed MR
measure q[26] -> rec[4]; reset q[26]; // decomposed MR
cx q[5], q[29];
cx q[30], q[36];
cx q[32], q[40];
measure q[28] -> rec[5]; reset q[28]; // decomposed MR
cx q[8], q[29];
cx q[30], q[1];
cx q[32], q[22];
measure q[36] -> rec[6]; reset q[36]; // decomposed MR
cx q[32], q[10];
cx q[30], q[34];
measure q[29] -> rec[7]; reset q[29]; // decomposed MR
cx q[30], q[5];
cx q[32], q[39];
measure q[34] -> rec[8]; reset q[34]; // decomposed MR
cx q[32], q[7];
cx q[30], q[37];
measure q[39] -> rec[9]; reset q[39]; // decomposed MR
cx q[30], q[35];
cx q[32], q[40];
measure q[37] -> rec[10]; reset q[37]; // decomposed MR
cx q[30], q[21];
cx q[32], q[9];
measure q[35] -> rec[11]; reset q[35]; // decomposed MR
measure q[40] -> rec[12]; reset q[40]; // decomposed MR
h q[30];
h q[32];
cx q[33], q[9];
cx q[33], q[41];
measure q[30] -> rec[13]; reset q[30]; // decomposed MR
measure q[32] -> rec[14]; reset q[32]; // decomposed MR
cx q[33], q[1];
cx q[33], q[5];
cx q[33], q[41];
cx q[33], q[21];
measure q[41] -> rec[15]; reset q[41]; // decomposed MR
h q[33];
measure q[33] -> rec[16]; reset q[33]; // decomposed MR
