OPENQASM 2.0;
include "qelib1.inc";

qreg q[85];
creg rec[54];

h q[1];
h q[3];
h q[0];
h q[4];
h q[10];
h q[7];
h q[2];
h q[5];
h q[21];
h q[13];
h q[6];
h q[28];
h q[15];
h q[17];
h q[29];
h q[35];
h q[36];
h q[40];
h q[42];
h q[44];
h q[51];
h q[52];
h q[54];
h q[55];
h q[57];
h q[63];
h q[64];
h q[67];
h q[68];
h q[77];
h q[72];
h q[74];
h q[73];
cx q[10], q[19];
cx q[3], q[16];
cx q[5], q[24];
cx q[28], q[27];
cx q[4], q[22];
cx q[7], q[8];
cx q[1], q[9];
cx q[35], q[33];
cx q[57], q[49];
cx q[15], q[20];
cx q[0], q[18];
cx q[64], q[60];
cx q[55], q[61];
cx q[63], q[59];
cx q[74], q[80];
cx q[52], q[45];
cx q[73], q[81];
cx q[67], q[46];
cx q[72], q[78];
cx q[29], q[3];
cx q[10], q[23];
cx q[27], q[26];
cx q[22], q[12];
cx q[4], q[11];
cx q[1], q[25];
cx q[49], q[56];
cx q[7], q[9];
cx q[24], q[14];
cx q[18], q[19];
cx q[17], q[0];
cx q[52], q[60];
cx q[64], q[47];
cx q[55], q[62];
cx q[73], q[80];
cx q[63], q[50];
cx q[61], q[57];
cx q[59], q[66];
cx q[81], q[78];
cx q[23], q[5];
cx q[28], q[3];
cx q[10], q[8];
cx q[29], q[30];
cx q[13], q[4];
cx q[2], q[26];
cx q[22], q[1];
cx q[27], q[71];
cx q[56], q[60];
cx q[49], q[48];
cx q[12], q[7];
cx q[17], q[20];
cx q[54], q[64];
cx q[51], q[57];
cx q[62], q[53];
cx q[61], q[83];
cx q[52], q[58];
cx q[55], q[69];
cx q[47], q[66];
cx q[45], q[63];
cx q[19], q[70];
cx q[15], q[10];
cx q[28], q[25];
cx q[6], q[5];
cx q[21], q[3];
cx q[11], q[23];
cx q[2], q[14];
cx q[13], q[30];
cx q[8], q[1];
cx q[26], q[24];
cx q[4], q[29];
cx q[60], q[64];
cx q[67], q[49];
cx q[17], q[70];
cx q[48], q[63];
cx q[54], q[61];
cx q[51], q[52];
cx q[57], q[58];
cx q[9], q[31];
cx q[53], q[83];
cx q[45], q[82];
cx q[77], q[82];
cx q[82], q[80];
cx q[47], q[76];
measure q[83] -> rec[0];
cx q[28], q[71];
cx q[16], q[11];
cx q[21], q[22];
cx q[25], q[23];
cx q[5], q[27];
cx q[0], q[15];
cx q[10], q[18];
cx q[3], q[12];
cx q[2], q[32];
cx q[30], q[39];
cx q[33], q[39];
cx q[49], q[65];
cx q[64], q[69];
cx q[60], q[59];
cx q[26], q[41];
cx q[32], q[41];
cx q[41], q[34];
cx q[44], q[32];
cx q[32], q[35];
cx q[42], q[32];
cx q[40], q[32];
cx q[20], q[42];
measure q[42] -> rec[1];
cx q[54], q[75];
cx q[75], q[73];
cx q[75], q[76];
cx q[80], q[76];
cx q[76], q[79];
cx q[66], q[79];
cx q[52], q[75];
cx q[77], q[73];
cx q[63], q[79];
cx q[48], q[4];
cx q[66], q[20];
measure q[71] -> rec[2];
measure q[79] -> rec[3];
h q[66]; measure q[66] -> rec[4]; h q[66]; // decomposed MX
cx q[10], q[70];
cx q[0], q[32];
cx q[3], q[43];
cx q[39], q[43];
cx q[13], q[43];
cx q[22], q[43];
cx q[41], q[43];
cx q[29], q[39];
measure q[39] -> rec[5];
cx q[25], q[38];
cx q[38], q[31];
cx q[31], q[34];
cx q[35], q[38];
cx q[38], q[31];
cx q[1], q[31];
cx q[33], q[34];
cx q[34], q[35];
cx q[7], q[34];
cx q[8], q[35];
measure q[31] -> rec[6];
measure q[34] -> rec[7];
measure q[35] -> rec[8];
cx q[43], q[33];
cx q[11], q[33];
cx q[23], q[38];
cx q[27], q[37];
cx q[6], q[37];
cx q[37], q[44];
cx q[36], q[37];
cx q[44], q[41];
cx q[14], q[41];
cx q[24], q[44];
measure q[41] -> rec[9];
measure q[44] -> rec[10];
cx q[6], q[28];
cx q[5], q[36];
cx q[18], q[40];
cx q[16], q[43];
cx q[60], q[76];
cx q[64], q[80];
cx q[65], q[84];
cx q[72], q[84];
cx q[46], q[84];
cx q[72], q[82];
cx q[82], q[75];
cx q[84], q[77];
cx q[84], q[81];
cx q[84], q[72];
h q[84]; measure q[84] -> rec[11]; h q[84]; // decomposed MX
cx q[48], q[72];
cx q[57], q[75];
cx q[61], q[77];
cx q[69], q[82];
cx q[45], q[1];
cx q[51], q[7];
cx q[52], q[8];
cx q[53], q[2];
cx q[68], q[21];
cx q[68], q[73];
cx q[68], q[56];
cx q[55], q[68];
cx q[56], q[62];
measure q[73] -> rec[12];
cx q[56], q[74];
cx q[62], q[78];
cx q[68], q[81];
measure q[32] -> rec[13];
measure q[33] -> rec[14];
measure q[36] -> rec[15];
measure q[38] -> rec[16];
measure q[40] -> rec[17];
measure q[43] -> rec[18];
measure q[72] -> rec[19];
measure q[74] -> rec[20];
measure q[75] -> rec[21];
measure q[76] -> rec[22];
measure q[77] -> rec[23];
measure q[78] -> rec[24];
measure q[80] -> rec[25];
measure q[81] -> rec[26];
measure q[82] -> rec[27];
h q[45]; measure q[45] -> rec[28]; h q[45]; // decomposed MX
h q[48]; measure q[48] -> rec[29]; h q[48]; // decomposed MX
h q[51]; measure q[51] -> rec[30]; h q[51]; // decomposed MX
h q[52]; measure q[52] -> rec[31]; h q[52]; // decomposed MX
h q[53]; measure q[53] -> rec[32]; h q[53]; // decomposed MX
cx q[15], q[70];
cx q[28], q[37];
cx q[46], q[3];
cx q[47], q[0];
cx q[49], q[11];
cx q[50], q[10];
cx q[54], q[5];
cx q[55], q[6];
cx q[56], q[22];
cx q[57], q[25];
cx q[58], q[23];
cx q[60], q[17];
cx q[61], q[27];
cx q[62], q[29];
cx q[63], q[18];
cx q[64], q[14];
cx q[65], q[12];
cx q[67], q[16];
cx q[68], q[30];
cx q[69], q[24];
measure q[70] -> rec[33];
measure q[37] -> rec[34];
h q[46]; measure q[46] -> rec[35]; h q[46]; // decomposed MX
h q[47]; measure q[47] -> rec[36]; h q[47]; // decomposed MX
h q[49]; measure q[49] -> rec[37]; h q[49]; // decomposed MX
h q[50]; measure q[50] -> rec[38]; h q[50]; // decomposed MX
h q[54]; measure q[54] -> rec[39]; h q[54]; // decomposed MX
h q[55]; measure q[55] -> rec[40]; h q[55]; // decomposed MX
h q[56]; measure q[56] -> rec[41]; h q[56]; // decomposed MX
h q[57]; measure q[57] -> rec[42]; h q[57]; // decomposed MX
h q[58]; measure q[58] -> rec[43]; h q[58]; // decomposed MX
h q[60]; measure q[60] -> rec[44]; h q[60]; // decomposed MX
h q[61]; measure q[61] -> rec[45]; h q[61]; // decomposed MX
h q[62]; measure q[62] -> rec[46]; h q[62]; // decomposed MX
h q[63]; measure q[63] -> rec[47]; h q[63]; // decomposed MX
h q[64]; measure q[64] -> rec[48]; h q[64]; // decomposed MX
h q[65]; measure q[65] -> rec[49]; h q[65]; // decomposed MX
h q[67]; measure q[67] -> rec[50]; h q[67]; // decomposed MX
h q[68]; measure q[68] -> rec[51]; h q[68]; // decomposed MX
h q[69]; measure q[69] -> rec[52]; h q[69]; // decomposed MX
cx q[59], q[15];
h q[59]; measure q[59] -> rec[53]; h q[59]; // decomposed MX
