OPENQASM 2.0;
include "qelib1.inc";

qreg q[63];
creg rec[40];

h q[15];
h q[11];
h q[8];
h q[7];
h q[6];
h q[5];
h q[4];
h q[3];
h q[2];
h q[1];
h q[0];
h q[24];
h q[25];
h q[26];
h q[31];
h q[32];
h q[33];
h q[34];
h q[36];
h q[37];
h q[38];
h q[39];
h q[40];
h q[41];
h q[42];
h q[43];
h q[44];
h q[45];
h q[46];
h q[47];
h q[49];
h q[51];
h q[56];
h q[57];
h q[58];
h q[60];
h q[61];
h q[62];
cx q[7], q[13];
cx q[11], q[10];
cx q[8], q[12];
cx q[3], q[16];
cx q[4], q[21];
cx q[6], q[14];
cx q[0], q[19];
cx q[15], q[23];
cx q[26], q[29];
cx q[62], q[59];
cx q[58], q[55];
cx q[40], q[52];
cx q[1], q[13];
cx q[8], q[18];
cx q[7], q[20];
cx q[12], q[9];
cx q[5], q[11];
cx q[0], q[16];
cx q[14], q[10];
cx q[15], q[17];
cx q[7], q[19];
cx q[18], q[22];
cx q[5], q[0];
cx q[21], q[9];
cx q[1], q[4];
cx q[6], q[20];
cx q[2], q[17];
cx q[37], q[14];
cx q[0], q[1];
cx q[5], q[8];
cx q[4], q[16];
cx q[3], q[18];
cx q[15], q[21];
cx q[17], q[20];
cx q[2], q[12];
cx q[19], q[14];
cx q[6], q[28];
cx q[3], q[7];
cx q[11], q[17];
cx q[16], q[12];
cx q[21], q[19];
cx q[9], q[14];
cx q[1], q[27];
cx q[8], q[30];
cx q[26], q[2];
cx q[31], q[28];
cx q[6], q[53];
cx q[0], q[54];
cx q[7], q[5];
cx q[20], q[16];
cx q[4], q[11];
cx q[17], q[22];
cx q[10], q[21];
cx q[19], q[27];
cx q[32], q[1];
cx q[25], q[2];
cx q[47], q[53];
cx q[44], q[54];
cx q[0], q[52];
cx q[13], q[17];
cx q[11], q[3];
cx q[12], q[10];
cx q[21], q[18];
cx q[16], q[27];
cx q[38], q[19];
cx q[32], q[35];
cx q[33], q[4];
cx q[25], q[15];
cx q[51], q[53];
cx q[42], q[54];
cx q[41], q[44];
cx q[10], q[13];
cx q[21], q[27];
cx q[19], q[30];
cx q[32], q[8];
cx q[33], q[22];
cx q[25], q[1];
cx q[24], q[15];
cx q[2], q[54];
cx q[18], q[27];
cx q[9], q[30];
cx q[38], q[19];
cx q[32], q[14];
cx q[26], q[8];
cx q[15], q[23];
cx q[1], q[53];
cx q[3], q[27];
cx q[16], q[30];
cx q[37], q[14];
cx q[32], q[20];
cx q[26], q[5];
cx q[25], q[19];
cx q[22], q[53];
cx q[15], q[59];
cx q[10], q[27];
cx q[7], q[30];
h q[37]; measure q[37] -> rec[0]; h q[37]; // decomposed MX
cx q[32], q[11];
cx q[26], q[12];
cx q[33], q[14];
cx q[24], q[19];
cx q[49], q[53];
cx q[15], q[55];
cx q[60], q[59];
measure q[27] -> rec[1];
cx q[21], q[30];
cx q[32], q[13];
cx q[26], q[11];
cx q[33], q[5];
cx q[25], q[14];
cx q[24], q[9];
cx q[56], q[55];
cx q[19], q[54];
cx q[22], q[59];
cx q[15], q[48];
cx q[38], q[30];
cx q[32], q[10];
cx q[26], q[18];
cx q[33], q[3];
cx q[25], q[7];
cx q[24], q[14];
cx q[21], q[28];
cx q[4], q[55];
cx q[8], q[59];
h q[38]; measure q[38] -> rec[2]; h q[38]; // decomposed MX
cx q[17], q[30];
cx q[26], q[10];
cx q[33], q[12];
cx q[24], q[5];
cx q[36], q[28];
cx q[21], q[53];
cx q[1], q[55];
cx q[44], q[4];
cx q[61], q[59];
cx q[43], q[8];
measure q[30] -> rec[3];
cx q[32], q[17];
cx q[26], q[29];
cx q[33], q[11];
cx q[24], q[3];
cx q[14], q[28];
cx q[51], q[53];
cx q[57], q[55];
cx q[4], q[54];
cx q[8], q[50];
cx q[32], q[35];
measure q[29] -> rec[4];
cx q[26], q[17];
cx q[33], q[18];
cx q[25], q[11];
cx q[24], q[12];
cx q[34], q[28];
h q[51]; measure q[51] -> rec[5]; h q[51]; // decomposed MX
cx q[3], q[53];
cx q[58], q[55];
cx q[1], q[54];
cx q[14], q[59];
cx q[4], q[52];
cx q[8], q[48];
h q[32]; measure q[32] -> rec[6]; h q[32]; // decomposed MX
measure q[35] -> rec[7];
h q[26]; measure q[26] -> rec[8]; h q[26]; // decomposed MX
h q[33]; measure q[33] -> rec[9]; h q[33]; // decomposed MX
cx q[25], q[13];
cx q[36], q[34];
cx q[7], q[28];
cx q[12], q[53];
h q[58]; measure q[58] -> rec[10]; h q[58]; // decomposed MX
cx q[16], q[55];
cx q[41], q[54];
cx q[3], q[59];
cx q[44], q[4];
cx q[1], q[50];
cx q[43], q[8];
cx q[45], q[48];
cx q[25], q[23];
cx q[24], q[13];
h q[36]; measure q[36] -> rec[11]; h q[36]; // decomposed MX
cx q[11], q[28];
cx q[47], q[53];
cx q[9], q[55];
h q[41]; measure q[41] -> rec[12]; h q[41]; // decomposed MX
cx q[60], q[59];
cx q[16], q[52];
cx q[42], q[50];
cx q[21], q[48];
cx q[39], q[43];
h q[25]; measure q[25] -> rec[13]; h q[25]; // decomposed MX
cx q[24], q[23];
cx q[31], q[28];
h q[47]; measure q[47] -> rec[14]; h q[47]; // decomposed MX
cx q[49], q[53];
cx q[56], q[55];
h q[60]; measure q[60] -> rec[15]; h q[60]; // decomposed MX
cx q[46], q[52];
cx q[14], q[50];
cx q[10], q[48];
measure q[23] -> rec[16];
h q[24]; measure q[24] -> rec[17]; h q[24]; // decomposed MX
h q[31]; measure q[31] -> rec[18]; h q[31]; // decomposed MX
cx q[17], q[28];
h q[49]; measure q[49] -> rec[19]; h q[49]; // decomposed MX
cx q[11], q[53];
h q[56]; measure q[56] -> rec[20]; h q[56]; // decomposed MX
cx q[18], q[55];
cx q[7], q[52];
cx q[16], q[50];
cx q[43], q[48];
cx q[13], q[28];
measure q[53] -> rec[21];
cx q[17], q[55];
cx q[11], q[59];
cx q[44], q[52];
cx q[42], q[18];
cx q[43], q[50];
cx q[14], q[48];
cx q[34], q[28];
cx q[57], q[55];
cx q[62], q[59];
h q[44]; measure q[44] -> rec[22]; h q[44]; // decomposed MX
cx q[12], q[52];
cx q[18], q[54];
h q[43]; measure q[43] -> rec[23]; h q[43]; // decomposed MX
cx q[7], q[50];
h q[34]; measure q[34] -> rec[24]; h q[34]; // decomposed MX
measure q[28] -> rec[25];
measure q[55] -> rec[26];
h q[57]; measure q[57] -> rec[27]; h q[57]; // decomposed MX
h q[62]; measure q[62] -> rec[28]; h q[62]; // decomposed MX
cx q[13], q[59];
cx q[17], q[52];
cx q[18], q[50];
cx q[61], q[59];
cx q[46], q[52];
cx q[13], q[54];
cx q[42], q[18];
cx q[39], q[50];
h q[61]; measure q[61] -> rec[29]; h q[61]; // decomposed MX
measure q[59] -> rec[30];
h q[46]; measure q[46] -> rec[31]; h q[46]; // decomposed MX
measure q[54] -> rec[32];
cx q[13], q[52];
h q[42]; measure q[42] -> rec[33]; h q[42]; // decomposed MX
cx q[18], q[48];
cx q[40], q[52];
cx q[13], q[50];
cx q[45], q[48];
measure q[52] -> rec[34];
h q[40]; measure q[40] -> rec[35]; h q[40]; // decomposed MX
measure q[50] -> rec[36];
cx q[17], q[48];
h q[45]; measure q[45] -> rec[37]; h q[45]; // decomposed MX
cx q[39], q[48];
measure q[48] -> rec[38];
h q[39]; measure q[39] -> rec[39]; h q[39]; // decomposed MX
