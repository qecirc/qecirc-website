OPENQASM 2.0;
include "qelib1.inc";

qreg q[63];
creg rec[42];

h q[1];
h q[3];
h q[0];
h q[4];
h q[11];
h q[10];
h q[7];
h q[8];
h q[2];
h q[5];
h q[21];
h q[13];
h q[6];
h q[26];
h q[17];
cx q[26], q[24];
cx q[7], q[9];
h q[31];
cx q[31], q[29];
cx q[17], q[19];
cx q[10], q[20];
cx q[6], q[14];
h q[32];
cx q[32], q[33];
h q[34];
cx q[34], q[35];
h q[36];
cx q[36], q[37];
h q[38];
cx q[38], q[39];
h q[40];
cx q[40], q[41];
h q[42];
cx q[42], q[25];
cx q[1], q[23];
h q[43];
cx q[43], q[44];
cx q[26], q[29];
cx q[4], q[9];
cx q[7], q[19];
cx q[10], q[18];
h q[45];
cx q[45], q[35];
h q[46];
cx q[46], q[36];
cx q[37], q[47];
cx q[1], q[25];
h q[48];
cx q[48], q[41];
cx q[17], q[20];
cx q[13], q[29];
cx q[4], q[30];
cx q[26], q[28];
cx q[0], q[19];
cx q[10], q[15];
cx q[7], q[14];
cx q[40], q[46];
cx q[36], q[35];
h q[49];
cx q[49], q[1];
cx q[9], q[23];
h q[50];
cx q[50], q[41];
cx q[4], q[16];
cx q[11], q[29];
cx q[28], q[27];
cx q[0], q[15];
cx q[5], q[14];
cx q[7], q[10];
h q[51];
cx q[51], q[40];
cx q[35], q[37];
cx q[19], q[18];
cx q[23], q[52];
cx q[46], q[50];
cx q[11], q[16];
cx q[27], q[53];
h q[54];
cx q[54], q[0];
cx q[4], q[12];
cx q[7], q[55];
h q[56];
cx q[56], q[37];
h q[57];
cx q[57], q[51];
cx q[21], q[29];
cx q[28], q[1];
cx q[2], q[14];
cx q[32], q[11];
cx q[5], q[27];
cx q[39], q[0];
cx q[4], q[22];
cx q[3], q[12];
cx q[7], q[58];
cx q[54], q[59];
h q[60];
cx q[60], q[51];
h q[61];
cx q[61], q[37];
cx q[24], q[53];
cx q[28], q[62];
cx q[2], q[26];
cx q[44], q[1];
cx q[43], q[21];
cx q[57], q[46];
measure q[53] -> rec[0];
h q[57]; measure q[57] -> rec[1]; h q[57]; // decomposed MX
reset q[53];
cx q[11], q[53];
cx q[39], q[5];
cx q[22], q[55];
cx q[15], q[58];
cx q[8], q[7];
cx q[3], q[29];
cx q[54], q[25];
cx q[61], q[60];
cx q[24], q[62];
cx q[43], q[26];
cx q[6], q[28];
measure q[62] -> rec[2];
reset q[57]; h q[57]; // decomposed RX
cx q[57], q[53];
reset q[62];
cx q[5], q[62];
cx q[9], q[55];
cx q[20], q[58];
cx q[31], q[29];
cx q[8], q[1];
cx q[54], q[18];
cx q[33], q[3];
cx q[32], q[7];
cx q[61], q[52];
cx q[14], q[24];
cx q[43], q[27];
cx q[21], q[22];
cx q[44], q[6];
cx q[15], q[51];
measure q[55] -> rec[3];
h q[31]; measure q[31] -> rec[4]; h q[31]; // decomposed MX
measure q[51] -> rec[5];
reset q[31]; h q[31]; // decomposed RX
cx q[31], q[53];
cx q[29], q[30];
cx q[4], q[8];
cx q[1], q[9];
cx q[54], q[20];
cx q[33], q[25];
cx q[39], q[7];
cx q[56], q[52];
cx q[43], q[14];
cx q[32], q[21];
cx q[19], q[58];
measure q[58] -> rec[6];
cx q[53], q[36];
cx q[31], q[62];
cx q[59], q[8];
cx q[54], q[9];
cx q[33], q[30];
cx q[38], q[1];
cx q[39], q[25];
reset q[51]; h q[51]; // decomposed RX
cx q[51], q[7];
cx q[52], q[47];
cx q[13], q[4];
cx q[43], q[44];
cx q[19], q[46];
h q[43]; measure q[43] -> rec[7]; h q[43]; // decomposed MX
measure q[44] -> rec[8];
measure q[46] -> rec[9];
reset q[43]; h q[43]; // decomposed RX
cx q[43], q[53];
cx q[62], q[41];
cx q[59], q[14];
cx q[33], q[9];
cx q[39], q[27];
cx q[49], q[1];
cx q[51], q[8];
cx q[45], q[52];
cx q[56], q[36];
cx q[32], q[13];
cx q[42], q[25];
cx q[7], q[35];
h q[42]; measure q[42] -> rec[10]; h q[42]; // decomposed MX
measure q[35] -> rec[11];
reset q[35]; h q[35]; // decomposed RX
cx q[35], q[53];
cx q[34], q[62];
reset q[42]; h q[42]; // decomposed RX
cx q[42], q[41];
reset q[44]; h q[44]; // decomposed RX
cx q[44], q[43];
cx q[54], q[59];
cx q[39], q[18];
cx q[49], q[9];
cx q[51], q[1];
cx q[47], q[45];
cx q[32], q[33];
cx q[8], q[37];
measure q[59] -> rec[12];
h q[32]; measure q[32] -> rec[13]; h q[32]; // decomposed MX
measure q[33] -> rec[14];
h q[49]; measure q[49] -> rec[15]; h q[49]; // decomposed MX
measure q[37] -> rec[16];
cx q[34], q[53];
cx q[42], q[50];
cx q[57], q[44];
cx q[54], q[24];
cx q[39], q[20];
cx q[51], q[9];
cx q[56], q[45];
cx q[6], q[41];
cx q[25], q[47];
cx q[27], q[62];
cx q[12], q[43];
cx q[30], q[35];
h q[54]; measure q[54] -> rec[17]; h q[54]; // decomposed MX
h q[51]; measure q[51] -> rec[18]; h q[51]; // decomposed MX
h q[42]; measure q[42] -> rec[19]; h q[42]; // decomposed MX
h q[56]; measure q[56] -> rec[20]; h q[56]; // decomposed MX
measure q[41] -> rec[21];
measure q[47] -> rec[22];
measure q[62] -> rec[23];
measure q[43] -> rec[24];
measure q[35] -> rec[25];
cx q[48], q[34];
reset q[32]; h q[32]; // decomposed RX
cx q[32], q[53];
cx q[61], q[50];
cx q[57], q[36];
cx q[38], q[39];
cx q[9], q[45];
h q[38]; measure q[38] -> rec[26]; h q[38]; // decomposed MX
measure q[39] -> rec[27];
h q[57]; measure q[57] -> rec[28]; h q[57]; // decomposed MX
measure q[45] -> rec[29];
cx q[31], q[34];
cx q[32], q[44];
cx q[61], q[52];
cx q[4], q[53];
cx q[26], q[50];
cx q[16], q[36];
cx q[24], q[48];
h q[32]; measure q[32] -> rec[30]; h q[32]; // decomposed MX
h q[61]; measure q[61] -> rec[31]; h q[61]; // decomposed MX
measure q[53] -> rec[32];
measure q[50] -> rec[33];
measure q[36] -> rec[34];
measure q[48] -> rec[35];
cx q[31], q[40];
cx q[22], q[44];
cx q[1], q[52];
cx q[14], q[34];
h q[31]; measure q[31] -> rec[36]; h q[31]; // decomposed MX
measure q[52] -> rec[37];
measure q[44] -> rec[38];
measure q[34] -> rec[39];
cx q[60], q[40];
h q[60]; measure q[60] -> rec[40]; h q[60]; // decomposed MX
cx q[20], q[40];
measure q[40] -> rec[41];
