OPENQASM 2.0;
include "qelib1.inc";

qreg q[64];
creg rec[40];

h q[16];
h q[13];
h q[8];
h q[6];
h q[5];
h q[4];
h q[3];
h q[2];
h q[1];
h q[0];
h q[27];
h q[32];
h q[25];
h q[39];
h q[42];
h q[43];
h q[50];
h q[40];
h q[44];
h q[47];
h q[54];
h q[52];
h q[46];
h q[55];
h q[56];
h q[57];
h q[58];
cx q[3], q[15];
cx q[8], q[23];
cx q[16], q[22];
cx q[4], q[21];
cx q[2], q[19];
cx q[1], q[7];
cx q[27], q[26];
cx q[0], q[14];
cx q[32], q[37];
cx q[52], q[48];
cx q[42], q[51];
cx q[57], q[63];
cx q[39], q[33];
cx q[25], q[34];
cx q[40], q[41];
cx q[47], q[45];
cx q[46], q[49];
cx q[58], q[60];
cx q[3], q[9];
cx q[22], q[17];
cx q[8], q[10];
cx q[13], q[15];
cx q[21], q[12];
cx q[16], q[20];
cx q[19], q[7];
cx q[39], q[27];
cx q[2], q[14];
cx q[32], q[38];
cx q[25], q[37];
cx q[52], q[49];
cx q[26], q[34];
cx q[51], q[53];
cx q[43], q[41];
cx q[63], q[62];
cx q[54], q[42];
cx q[55], q[45];
cx q[58], q[61];
cx q[56], q[60];
cx q[23], q[17];
cx q[3], q[4];
cx q[5], q[22];
cx q[6], q[15];
cx q[8], q[11];
cx q[13], q[18];
cx q[16], q[21];
cx q[7], q[9];
cx q[0], q[20];
cx q[27], q[28];
cx q[32], q[31];
cx q[26], q[38];
cx q[37], q[24];
cx q[39], q[35];
cx q[47], q[52];
cx q[40], q[53];
cx q[50], q[41];
cx q[51], q[48];
cx q[43], q[45];
cx q[58], q[59];
cx q[57], q[61];
cx q[56], q[63];
cx q[6], q[8];
cx q[1], q[22];
cx q[3], q[19];
cx q[4], q[10];
cx q[17], q[18];
cx q[5], q[2];
cx q[13], q[16];
cx q[14], q[11];
cx q[21], q[23];
cx q[28], q[24];
cx q[27], q[32];
cx q[37], q[33];
cx q[31], q[30];
cx q[38], q[36];
cx q[25], q[35];
cx q[39], q[29];
cx q[44], q[40];
cx q[55], q[51];
cx q[54], q[47];
cx q[50], q[49];
cx q[52], q[53];
cx q[41], q[42];
cx q[58], q[45];
cx q[60], q[48];
h q[58]; measure q[58] -> rec[0]; h q[58]; // decomposed MX
h q[60]; measure q[60] -> rec[1]; h q[60]; // decomposed MX
cx q[1], q[3];
cx q[8], q[9];
cx q[4], q[20];
cx q[15], q[17];
cx q[0], q[18];
cx q[5], q[23];
cx q[6], q[7];
cx q[13], q[14];
cx q[11], q[12];
cx q[2], q[10];
cx q[22], q[19];
cx q[24], q[16];
cx q[57], q[42];
cx q[59], q[47];
cx q[61], q[49];
cx q[56], q[50];
cx q[62], q[51];
cx q[63], q[52];
h q[24]; measure q[24] -> rec[2]; h q[24]; // decomposed MX
h q[57]; measure q[57] -> rec[3]; h q[57]; // decomposed MX
h q[59]; measure q[59] -> rec[4]; h q[59]; // decomposed MX
h q[61]; measure q[61] -> rec[5]; h q[61]; // decomposed MX
h q[62]; measure q[62] -> rec[6]; h q[62]; // decomposed MX
h q[63]; measure q[63] -> rec[7]; h q[63]; // decomposed MX
cx q[26], q[8];
cx q[28], q[4];
cx q[30], q[1];
cx q[31], q[20];
cx q[32], q[12];
cx q[33], q[18];
cx q[34], q[14];
cx q[35], q[17];
cx q[36], q[7];
cx q[37], q[15];
cx q[38], q[19];
cx q[39], q[23];
cx q[25], q[13];
cx q[27], q[5];
cx q[29], q[2];
cx q[56], q[40];
cx q[3], q[43];
cx q[0], q[45];
cx q[22], q[49];
cx q[10], q[53];
h q[25]; measure q[25] -> rec[8]; h q[25]; // decomposed MX
h q[26]; measure q[26] -> rec[9]; h q[26]; // decomposed MX
h q[27]; measure q[27] -> rec[10]; h q[27]; // decomposed MX
h q[28]; measure q[28] -> rec[11]; h q[28]; // decomposed MX
h q[29]; measure q[29] -> rec[12]; h q[29]; // decomposed MX
h q[30]; measure q[30] -> rec[13]; h q[30]; // decomposed MX
h q[31]; measure q[31] -> rec[14]; h q[31]; // decomposed MX
h q[32]; measure q[32] -> rec[15]; h q[32]; // decomposed MX
h q[33]; measure q[33] -> rec[16]; h q[33]; // decomposed MX
h q[34]; measure q[34] -> rec[17]; h q[34]; // decomposed MX
h q[35]; measure q[35] -> rec[18]; h q[35]; // decomposed MX
h q[36]; measure q[36] -> rec[19]; h q[36]; // decomposed MX
h q[37]; measure q[37] -> rec[20]; h q[37]; // decomposed MX
h q[38]; measure q[38] -> rec[21]; h q[38]; // decomposed MX
h q[39]; measure q[39] -> rec[22]; h q[39]; // decomposed MX
h q[56]; measure q[56] -> rec[23]; h q[56]; // decomposed MX
measure q[43] -> rec[24];
measure q[45] -> rec[25];
measure q[49] -> rec[26];
measure q[53] -> rec[27];
cx q[16], q[40];
cx q[8], q[41];
cx q[4], q[42];
cx q[1], q[44];
cx q[20], q[46];
cx q[12], q[47];
cx q[14], q[48];
cx q[17], q[50];
cx q[7], q[51];
cx q[15], q[52];
cx q[19], q[54];
cx q[23], q[55];
measure q[40] -> rec[28];
measure q[41] -> rec[29];
measure q[42] -> rec[30];
measure q[44] -> rec[31];
measure q[46] -> rec[32];
measure q[47] -> rec[33];
measure q[48] -> rec[34];
measure q[50] -> rec[35];
measure q[51] -> rec[36];
measure q[52] -> rec[37];
measure q[54] -> rec[38];
measure q[55] -> rec[39];
