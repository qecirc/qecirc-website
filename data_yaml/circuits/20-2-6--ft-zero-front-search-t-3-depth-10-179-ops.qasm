OPENQASM 2.0;
include "qelib1.inc";

qreg q[63];
creg rec[43];

h q[4];
h q[8];
h q[7];
h q[13];
h q[14];
h q[11];
h q[18];
h q[10];
h q[2];
cx q[10], q[16];
cx q[8], q[3];
cx q[18], q[9];
cx q[18], q[12];
cx q[11], q[17];
cx q[13], q[0];
cx q[2], q[15];
cx q[14], q[1];
cx q[17], q[1];
cx q[10], q[5];
cx q[8], q[19];
cx q[13], q[11];
cx q[18], q[3];
cx q[17], q[5];
cx q[8], q[0];
cx q[10], q[12];
cx q[18], q[2];
cx q[5], q[6];
cx q[4], q[3];
cx q[8], q[1];
cx q[10], q[0];
cx q[7], q[12];
cx q[17], q[15];
cx q[2], q[16];
cx q[12], q[19];
cx q[1], q[9];
cx q[3], q[6];
cx q[14], q[18];
h q[20];
h q[21];
h q[22];
h q[23];
h q[25];
h q[28];
h q[32];
h q[33];
cx q[28], q[29];
cx q[21], q[31];
cx q[25], q[26];
cx q[20], q[35];
cx q[22], q[24];
cx q[33], q[34];
cx q[28], q[30];
cx q[32], q[35];
cx q[20], q[31];
cx q[26], q[27];
cx q[21], q[29];
cx q[22], q[25];
cx q[20], q[30];
cx q[34], q[28];
cx q[23], q[21];
cx q[33], q[27];
cx q[31], q[26];
cx q[24], q[35];
cx q[32], q[33];
cx q[21], q[24];
cx q[35], q[34];
cx q[23], q[22];
cx q[28], q[31];
cx q[20], q[36];
cx q[18], q[24];
measure q[24] -> rec[0];
cx q[4], q[5];
cx q[15], q[10];
cx q[7], q[8];
cx q[0], q[17];
cx q[11], q[20];
cx q[1], q[21];
measure q[21] -> rec[1];
cx q[9], q[22];
measure q[22] -> rec[2];
cx q[14], q[23];
measure q[23] -> rec[3];
cx q[7], q[25];
measure q[25] -> rec[4];
cx q[19], q[26];
measure q[26] -> rec[5];
cx q[8], q[27];
measure q[27] -> rec[6];
cx q[3], q[28];
measure q[28] -> rec[7];
cx q[4], q[29];
measure q[29] -> rec[8];
cx q[5], q[30];
measure q[30] -> rec[9];
cx q[6], q[31];
measure q[31] -> rec[10];
cx q[2], q[32];
measure q[32] -> rec[11];
cx q[15], q[33];
measure q[33] -> rec[12];
cx q[16], q[34];
measure q[34] -> rec[13];
cx q[10], q[35];
measure q[35] -> rec[14];
cx q[0], q[36];
cx q[17], q[20];
measure q[20] -> rec[15];
cx q[13], q[36];
measure q[36] -> rec[16];
h q[48];
h q[52];
h q[53];
h q[54];
cx q[54], q[62];
cx q[53], q[50];
cx q[54], q[44];
cx q[52], q[45];
cx q[48], q[37];
cx q[53], q[48];
cx q[45], q[49];
cx q[54], q[37];
cx q[48], q[52];
cx q[48], q[62];
cx q[37], q[49];
cx q[37], q[62];
cx q[53], q[39];
cx q[39], q[62];
measure q[62] -> rec[17];
cx q[45], q[44];
cx q[54], q[40];
cx q[45], q[46];
cx q[44], q[47];
cx q[37], q[42];
cx q[52], q[43];
cx q[49], q[51];
cx q[53], q[41];
cx q[48], q[38];
h q[56];
cx q[56], q[59];
cx q[41], q[55];
cx q[43], q[55];
cx q[44], q[55];
cx q[37], q[55];
measure q[55] -> rec[18];
cx q[45], q[60];
cx q[60], q[61];
cx q[53], q[57];
cx q[57], q[56];
cx q[56], q[61];
cx q[38], q[56];
measure q[56] -> rec[19];
cx q[39], q[57];
measure q[57] -> rec[20];
cx q[52], q[61];
measure q[61] -> rec[21];
cx q[54], q[58];
cx q[59], q[58];
cx q[58], q[60];
cx q[60], q[59];
cx q[42], q[58];
measure q[58] -> rec[22];
cx q[47], q[59];
measure q[59] -> rec[23];
cx q[51], q[60];
measure q[60] -> rec[24];
cx q[37], q[0];
h q[37]; measure q[37] -> rec[25]; h q[37]; // decomposed MX
cx q[38], q[11];
h q[38]; measure q[38] -> rec[26]; h q[38]; // decomposed MX
cx q[39], q[13];
h q[39]; measure q[39] -> rec[27]; h q[39]; // decomposed MX
cx q[40], q[17];
h q[40]; measure q[40] -> rec[28]; h q[40]; // decomposed MX
cx q[41], q[1];
h q[41]; measure q[41] -> rec[29]; h q[41]; // decomposed MX
cx q[42], q[9];
h q[42]; measure q[42] -> rec[30]; h q[42]; // decomposed MX
cx q[43], q[14];
h q[43]; measure q[43] -> rec[31]; h q[43]; // decomposed MX
cx q[44], q[18];
h q[44]; measure q[44] -> rec[32]; h q[44]; // decomposed MX
cx q[45], q[12];
h q[45]; measure q[45] -> rec[33]; h q[45]; // decomposed MX
cx q[46], q[8];
h q[46]; measure q[46] -> rec[34]; h q[46]; // decomposed MX
cx q[47], q[3];
h q[47]; measure q[47] -> rec[35]; h q[47]; // decomposed MX
cx q[48], q[4];
h q[48]; measure q[48] -> rec[36]; h q[48]; // decomposed MX
cx q[49], q[5];
h q[49]; measure q[49] -> rec[37]; h q[49]; // decomposed MX
cx q[50], q[6];
h q[50]; measure q[50] -> rec[38]; h q[50]; // decomposed MX
cx q[51], q[2];
h q[51]; measure q[51] -> rec[39]; h q[51]; // decomposed MX
cx q[52], q[15];
h q[52]; measure q[52] -> rec[40]; h q[52]; // decomposed MX
cx q[53], q[16];
h q[53]; measure q[53] -> rec[41]; h q[53]; // decomposed MX
cx q[54], q[10];
h q[54]; measure q[54] -> rec[42]; h q[54]; // decomposed MX
