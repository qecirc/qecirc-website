OPENQASM 2.0;
include "qelib1.inc";

qreg q[55];
creg rec[35];

h q[19];
h q[3];
h q[15];
h q[7];
h q[0];
h q[11];
h q[1];
h q[5];
h q[18];
h q[20];
h q[21];
h q[23];
h q[24];
h q[31];
h q[33];
h q[38];
h q[41];
h q[47];
h q[50];
h q[51];
h q[54];
cx q[19], q[8];
cx q[0], q[17];
cx q[1], q[6];
cx q[18], q[14];
cx q[15], q[16];
cx q[3], q[4];
cx q[11], q[2];
cx q[7], q[12];
cx q[54], q[48];
cx q[20], q[25];
cx q[31], q[30];
cx q[33], q[39];
cx q[23], q[22];
cx q[51], q[52];
cx q[38], q[43];
cx q[21], q[27];
cx q[41], q[35];
cx q[50], q[53];
cx q[19], q[17];
cx q[5], q[6];
cx q[3], q[18];
cx q[47], q[54];
cx q[4], q[7];
cx q[1], q[9];
cx q[15], q[10];
cx q[8], q[2];
cx q[11], q[13];
cx q[25], q[22];
cx q[39], q[49];
cx q[30], q[37];
cx q[20], q[26];
cx q[41], q[31];
cx q[50], q[52];
cx q[33], q[43];
cx q[38], q[28];
cx q[24], q[27];
cx q[19], q[16];
cx q[9], q[7];
cx q[11], q[18];
cx q[1], q[15];
cx q[54], q[53];
cx q[3], q[17];
cx q[2], q[6];
cx q[33], q[37];
cx q[38], q[31];
cx q[21], q[25];
cx q[41], q[43];
cx q[24], q[20];
cx q[13], q[10];
cx q[14], q[22];
cx q[28], q[44];
cx q[30], q[42];
cx q[5], q[23];
cx q[12], q[8];
cx q[16], q[26];
cx q[5], q[3];
cx q[18], q[9];
cx q[14], q[1];
cx q[2], q[46];
cx q[6], q[4];
cx q[37], q[35];
cx q[49], q[54];
cx q[43], q[40];
cx q[31], q[34];
cx q[0], q[11];
cx q[7], q[19];
cx q[38], q[32];
cx q[41], q[29];
cx q[10], q[27];
cx q[17], q[13];
cx q[12], q[24];
cx q[44], q[53];
cx q[30], q[48];
measure q[48] -> rec[0];
measure q[53] -> rec[1];
cx q[26], q[27];
cx q[10], q[46];
cx q[4], q[23];
cx q[35], q[45];
cx q[1], q[21];
cx q[3], q[25];
cx q[37], q[36];
cx q[15], q[2];
cx q[52], q[49];
cx q[18], q[22];
cx q[17], q[20];
cx q[7], q[24];
cx q[40], q[5];
cx q[34], q[14];
cx q[30], q[13];
cx q[29], q[11];
measure q[27] -> rec[2];
measure q[22] -> rec[3];
measure q[23] -> rec[4];
measure q[24] -> rec[5];
h q[30]; measure q[30] -> rec[6]; h q[30]; // decomposed MX
cx q[6], q[25];
cx q[16], q[46];
cx q[15], q[26];
cx q[47], q[49];
cx q[9], q[21];
cx q[0], q[20];
cx q[45], q[54];
cx q[35], q[18];
cx q[37], q[51];
cx q[40], q[52];
cx q[39], q[4];
cx q[38], q[3];
cx q[31], q[17];
cx q[32], q[1];
cx q[42], q[2];
cx q[34], q[50];
cx q[36], q[7];
measure q[46] -> rec[7];
measure q[26] -> rec[8];
measure q[20] -> rec[9];
measure q[21] -> rec[10];
measure q[25] -> rec[11];
measure q[50] -> rec[12];
measure q[51] -> rec[13];
measure q[52] -> rec[14];
measure q[54] -> rec[15];
h q[31]; measure q[31] -> rec[16]; h q[31]; // decomposed MX
h q[34]; measure q[34] -> rec[17]; h q[34]; // decomposed MX
h q[35]; measure q[35] -> rec[18]; h q[35]; // decomposed MX
h q[36]; measure q[36] -> rec[19]; h q[36]; // decomposed MX
h q[38]; measure q[38] -> rec[20]; h q[38]; // decomposed MX
h q[39]; measure q[39] -> rec[21]; h q[39]; // decomposed MX
h q[40]; measure q[40] -> rec[22]; h q[40]; // decomposed MX
h q[42]; measure q[42] -> rec[23]; h q[42]; // decomposed MX
cx q[28], q[0];
cx q[32], q[49];
cx q[29], q[47];
cx q[45], q[10];
cx q[41], q[6];
cx q[44], q[16];
cx q[33], q[9];
cx q[37], q[8];
cx q[43], q[15];
measure q[47] -> rec[24];
measure q[49] -> rec[25];
h q[28]; measure q[28] -> rec[26]; h q[28]; // decomposed MX
h q[29]; measure q[29] -> rec[27]; h q[29]; // decomposed MX
h q[32]; measure q[32] -> rec[28]; h q[32]; // decomposed MX
h q[33]; measure q[33] -> rec[29]; h q[33]; // decomposed MX
h q[37]; measure q[37] -> rec[30]; h q[37]; // decomposed MX
h q[41]; measure q[41] -> rec[31]; h q[41]; // decomposed MX
h q[43]; measure q[43] -> rec[32]; h q[43]; // decomposed MX
h q[44]; measure q[44] -> rec[33]; h q[44]; // decomposed MX
h q[45]; measure q[45] -> rec[34]; h q[45]; // decomposed MX
