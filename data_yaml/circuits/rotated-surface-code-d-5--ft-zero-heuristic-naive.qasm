OPENQASM 2.0;
include "qelib1.inc";

qreg q[89];
creg rec[64];

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
h q[49];
h q[50];
h q[51];
h q[52];
h q[53];
h q[54];
h q[55];
h q[56];
h q[57];
h q[58];
h q[59];
h q[60];
h q[61];
h q[62];
h q[63];
h q[64];
h q[65];
h q[66];
h q[67];
h q[68];
h q[69];
h q[70];
h q[71];
h q[72];
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
cx q[3], q[26];
cx q[18], q[27];
cx q[13], q[6];
cx q[17], q[0];
cx q[12], q[22];
cx q[16], q[7];
cx q[19], q[1];
cx q[15], q[5];
cx q[11], q[25];
cx q[24], q[26];
cx q[3], q[38];
cx q[18], q[39];
cx q[14], q[25];
cx q[23], q[26];
cx q[17], q[27];
cx q[11], q[37];
cx q[24], q[38];
cx q[13], q[25];
cx q[0], q[26];
cx q[14], q[37];
cx q[49], q[11];
measure q[27] -> rec[0]; reset q[27]; // decomposed MR
cx q[6], q[25];
cx q[13], q[28];
cx q[0], q[30];
cx q[49], q[14];
cx q[61], q[11];
measure q[26] -> rec[1]; reset q[26]; // decomposed MR
cx q[12], q[28];
cx q[6], q[29];
cx q[17], q[30];
cx q[13], q[37];
h q[49];
cx q[50], q[14];
measure q[25] -> rec[2]; reset q[25]; // decomposed MR
cx q[23], q[29];
cx q[10], q[30];
cx q[12], q[31];
cx q[6], q[37];
cx q[17], q[39];
cx q[13], q[40];
cx q[61], q[14];
cx q[50], q[73];
measure q[28] -> rec[3]; reset q[28]; // decomposed MR
measure q[49] -> rec[4]; reset q[49]; // decomposed MR
cx q[22], q[29];
cx q[20], q[30];
cx q[23], q[38];
cx q[12], q[40];
cx q[6], q[41];
cx q[50], q[3];
cx q[53], q[13];
h q[61];
cx q[62], q[14];
measure q[37] -> rec[5]; reset q[37]; // decomposed MR
measure q[39] -> rec[6]; reset q[39]; // decomposed MR
cx q[4], q[29];
cx q[22], q[31];
cx q[20], q[33];
cx q[0], q[38];
cx q[23], q[41];
cx q[12], q[43];
cx q[50], q[6];
cx q[51], q[3];
cx q[65], q[13];
cx q[53], q[75];
cx q[62], q[81];
measure q[30] -> rec[7]; reset q[30]; // decomposed MR
measure q[40] -> rec[8]; reset q[40]; // decomposed MR
measure q[61] -> rec[9]; reset q[61]; // decomposed MR
cx q[16], q[31];
cx q[4], q[32];
cx q[19], q[33];
cx q[22], q[41];
cx q[0], q[42];
cx q[51], q[24];
cx q[53], q[6];
cx q[62], q[3];
cx q[50], q[73];
cx q[65], q[83];
measure q[29] -> rec[10]; reset q[29]; // decomposed MR
measure q[38] -> rec[11]; reset q[38]; // decomposed MR
cx q[7], q[31];
cx q[10], q[32];
cx q[16], q[34];
cx q[4], q[41];
cx q[17], q[42];
cx q[22], q[43];
cx q[50], q[23];
h q[51];
cx q[52], q[24];
cx q[53], q[12];
cx q[62], q[6];
cx q[63], q[3];
measure q[33] -> rec[12]; reset q[33]; // decomposed MR
measure q[73] -> rec[13]; reset q[73]; // decomposed MR
cx q[9], q[32];
cx q[15], q[34];
cx q[7], q[35];
cx q[10], q[42];
cx q[16], q[43];
cx q[4], q[44];
h q[50];
cx q[54], q[23];
cx q[63], q[24];
cx q[65], q[6];
cx q[52], q[74];
cx q[53], q[75];
cx q[62], q[81];
measure q[31] -> rec[14]; reset q[31]; // decomposed MR
measure q[41] -> rec[15]; reset q[41]; // decomposed MR
measure q[51] -> rec[16]; reset q[51]; // decomposed MR
cx q[1], q[32];
cx q[9], q[35];
cx q[20], q[42];
cx q[7], q[43];
cx q[10], q[44];
cx q[16], q[46];
cx q[52], q[18];
cx q[53], q[22];
cx q[62], q[23];
h q[63];
cx q[64], q[24];
cx q[65], q[12];
cx q[54], q[76];
measure q[34] -> rec[17]; reset q[34]; // decomposed MR
measure q[50] -> rec[18]; reset q[50]; // decomposed MR
measure q[75] -> rec[19]; reset q[75]; // decomposed MR
measure q[81] -> rec[20]; reset q[81]; // decomposed MR
cx q[5], q[35];
cx q[1], q[36];
cx q[9], q[44];
cx q[20], q[45];
cx q[15], q[46];
cx q[7], q[47];
cx q[52], q[0];
h q[53];
cx q[55], q[22];
cx q[57], q[16];
h q[62];
cx q[66], q[23];
cx q[64], q[82];
cx q[65], q[83];
measure q[32] -> rec[21]; reset q[32]; // decomposed MR
measure q[42] -> rec[22]; reset q[42]; // decomposed MR
measure q[43] -> rec[23]; reset q[43]; // decomposed MR
measure q[63] -> rec[24]; reset q[63]; // decomposed MR
cx q[8], q[35];
cx q[19], q[36];
cx q[1], q[44];
cx q[9], q[47];
cx q[54], q[0];
cx q[64], q[18];
cx q[65], q[22];
cx q[69], q[16];
cx q[52], q[74];
cx q[55], q[77];
cx q[57], q[79];
cx q[66], q[84];
measure q[46] -> rec[25]; reset q[46]; // decomposed MR
measure q[53] -> rec[26]; reset q[53]; // decomposed MR
measure q[62] -> rec[27]; reset q[62]; // decomposed MR
measure q[83] -> rec[28]; reset q[83]; // decomposed MR
cx q[21], q[36];
cx q[19], q[45];
cx q[5], q[47];
cx q[1], q[48];
cx q[52], q[17];
cx q[54], q[4];
cx q[64], q[0];
h q[65];
cx q[67], q[22];
cx q[69], q[87];
measure q[35] -> rec[29]; reset q[35]; // decomposed MR
measure q[44] -> rec[30]; reset q[44]; // decomposed MR
measure q[74] -> rec[31]; reset q[74]; // decomposed MR
cx q[2], q[36];
cx q[8], q[47];
cx q[19], q[48];
h q[52];
cx q[55], q[4];
cx q[66], q[0];
cx q[54], q[76];
cx q[64], q[82];
cx q[67], q[85];
measure q[45] -> rec[32]; reset q[45]; // decomposed MR
measure q[65] -> rec[33]; reset q[65]; // decomposed MR
cx q[21], q[48];
cx q[54], q[10];
cx q[55], q[7];
cx q[64], q[17];
cx q[66], q[4];
measure q[36] -> rec[34]; reset q[36]; // decomposed MR
measure q[47] -> rec[35]; reset q[47]; // decomposed MR
measure q[52] -> rec[36]; reset q[52]; // decomposed MR
measure q[76] -> rec[37]; reset q[76]; // decomposed MR
measure q[82] -> rec[38]; reset q[82]; // decomposed MR
cx q[2], q[48];
h q[54];
cx q[56], q[10];
cx q[57], q[7];
h q[64];
cx q[67], q[4];
cx q[55], q[77];
cx q[66], q[84];
cx q[55], q[9];
cx q[57], q[15];
cx q[66], q[10];
cx q[67], q[7];
cx q[56], q[78];
measure q[48] -> rec[39]; reset q[48]; // decomposed MR
measure q[54] -> rec[40]; reset q[54]; // decomposed MR
measure q[64] -> rec[41]; reset q[64]; // decomposed MR
measure q[77] -> rec[42]; reset q[77]; // decomposed MR
measure q[84] -> rec[43]; reset q[84]; // decomposed MR
h q[55];
cx q[56], q[20];
cx q[58], q[9];
h q[66];
cx q[68], q[10];
cx q[69], q[7];
cx q[57], q[79];
cx q[67], q[85];
cx q[56], q[1];
cx q[57], q[5];
cx q[67], q[9];
cx q[69], q[15];
cx q[58], q[80];
cx q[68], q[86];
measure q[55] -> rec[44]; reset q[55]; // decomposed MR
measure q[66] -> rec[45]; reset q[66]; // decomposed MR
measure q[79] -> rec[46]; reset q[79]; // decomposed MR
measure q[85] -> rec[47]; reset q[85]; // decomposed MR
h q[57];
cx q[58], q[1];
cx q[59], q[5];
h q[67];
cx q[68], q[20];
cx q[70], q[9];
cx q[56], q[78];
cx q[69], q[87];
cx q[56], q[19];
cx q[58], q[8];
cx q[68], q[1];
cx q[69], q[5];
cx q[70], q[88];
measure q[57] -> rec[48]; reset q[57]; // decomposed MR
measure q[67] -> rec[49]; reset q[67]; // decomposed MR
measure q[78] -> rec[50]; reset q[78]; // decomposed MR
measure q[87] -> rec[51]; reset q[87]; // decomposed MR
h q[56];
cx q[59], q[8];
h q[69];
cx q[70], q[1];
cx q[71], q[5];
cx q[58], q[80];
cx q[68], q[86];
cx q[58], q[21];
h q[59];
cx q[68], q[19];
cx q[70], q[8];
measure q[56] -> rec[52]; reset q[56]; // decomposed MR
measure q[69] -> rec[53]; reset q[69]; // decomposed MR
measure q[80] -> rec[54]; reset q[80]; // decomposed MR
measure q[86] -> rec[55]; reset q[86]; // decomposed MR
h q[58];
cx q[60], q[21];
h q[68];
cx q[71], q[8];
cx q[70], q[88];
measure q[59] -> rec[56]; reset q[59]; // decomposed MR
cx q[60], q[2];
cx q[70], q[21];
h q[71];
measure q[58] -> rec[57]; reset q[58]; // decomposed MR
measure q[68] -> rec[58]; reset q[68]; // decomposed MR
measure q[88] -> rec[59]; reset q[88]; // decomposed MR
h q[60];
h q[70];
cx q[72], q[21];
measure q[71] -> rec[60]; reset q[71]; // decomposed MR
cx q[72], q[2];
measure q[60] -> rec[61]; reset q[60]; // decomposed MR
measure q[70] -> rec[62]; reset q[70]; // decomposed MR
h q[72];
measure q[72] -> rec[63]; reset q[72]; // decomposed MR
