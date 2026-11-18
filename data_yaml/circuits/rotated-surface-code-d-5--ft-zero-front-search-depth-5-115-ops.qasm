OPENQASM 2.0;
include "qelib1.inc";

qreg q[55];
creg rec[30];

h q[10];
h q[14];
h q[22];
h q[11];
h q[19];
h q[13];
h q[24];
h q[15];
h q[1];
h q[8];
h q[17];
h q[2];
cx q[22], q[7];
cx q[14], q[23];
cx q[1], q[21];
cx q[13], q[6];
cx q[15], q[5];
cx q[10], q[0];
cx q[17], q[18];
cx q[19], q[20];
cx q[7], q[4];
cx q[22], q[9];
cx q[14], q[3];
cx q[10], q[23];
cx q[1], q[5];
cx q[24], q[3];
cx q[0], q[4];
cx q[13], q[22];
cx q[21], q[9];
cx q[14], q[6];
cx q[15], q[7];
cx q[8], q[5];
cx q[19], q[1];
cx q[20], q[10];
cx q[11], q[14];
cx q[2], q[21];
cx q[18], q[0];
cx q[17], q[3];
cx q[15], q[16];
cx q[13], q[12];
h q[25];
h q[26];
h q[27];
cx q[27], q[30];
cx q[25], q[32];
cx q[26], q[36];
cx q[30], q[31];
cx q[27], q[34];
cx q[36], q[33];
cx q[25], q[29];
cx q[32], q[31];
cx q[34], q[35];
cx q[27], q[28];
cx q[26], q[30];
cx q[25], q[2];
h q[25]; measure q[25] -> rec[0]; h q[25]; // decomposed MX
cx q[26], q[3];
h q[26]; measure q[26] -> rec[1]; h q[26]; // decomposed MX
cx q[27], q[0];
h q[27]; measure q[27] -> rec[2]; h q[27]; // decomposed MX
cx q[28], q[10];
h q[28]; measure q[28] -> rec[3]; h q[28]; // decomposed MX
cx q[29], q[1];
h q[29]; measure q[29] -> rec[4]; h q[29]; // decomposed MX
cx q[30], q[23];
h q[30]; measure q[30] -> rec[5]; h q[30]; // decomposed MX
cx q[31], q[9];
h q[31]; measure q[31] -> rec[6]; h q[31]; // decomposed MX
cx q[32], q[5];
h q[32]; measure q[32] -> rec[7]; h q[32]; // decomposed MX
cx q[33], q[6];
h q[33]; measure q[33] -> rec[8]; h q[33]; // decomposed MX
cx q[34], q[22];
h q[34]; measure q[34] -> rec[9]; h q[34]; // decomposed MX
cx q[35], q[7];
h q[35]; measure q[35] -> rec[10]; h q[35]; // decomposed MX
cx q[36], q[14];
h q[36]; measure q[36] -> rec[11]; h q[36]; // decomposed MX
h q[38];
h q[39];
h q[40];
h q[41];
h q[42];
h q[43];
h q[45];
h q[47];
cx q[42], q[46];
cx q[39], q[48];
cx q[40], q[44];
cx q[38], q[37];
cx q[43], q[40];
cx q[48], q[49];
cx q[45], q[42];
cx q[44], q[39];
cx q[46], q[48];
cx q[47], q[49];
cx q[41], q[44];
cx q[43], q[42];
h q[50];
h q[51];
cx q[50], q[52];
cx q[52], q[54];
cx q[50], q[53];
cx q[50], q[41];
h q[50]; measure q[50] -> rec[12]; h q[50]; // decomposed MX
cx q[52], q[43];
h q[52]; measure q[52] -> rec[13]; h q[52]; // decomposed MX
cx q[51], q[45];
cx q[51], q[42];
h q[51]; measure q[51] -> rec[14]; h q[51]; // decomposed MX
cx q[53], q[46];
h q[53]; measure q[53] -> rec[15]; h q[53]; // decomposed MX
cx q[54], q[47];
h q[54]; measure q[54] -> rec[16]; h q[54]; // decomposed MX
cx q[17], q[37];
measure q[37] -> rec[17];
cx q[18], q[38];
measure q[38] -> rec[18];
cx q[19], q[39];
measure q[39] -> rec[19];
cx q[10], q[40];
measure q[40] -> rec[20];
cx q[1], q[41];
measure q[41] -> rec[21];
cx q[23], q[42];
measure q[42] -> rec[22];
cx q[4], q[43];
measure q[43] -> rec[23];
cx q[9], q[44];
measure q[44] -> rec[24];
cx q[6], q[45];
measure q[45] -> rec[25];
cx q[22], q[46];
measure q[46] -> rec[26];
cx q[7], q[47];
measure q[47] -> rec[27];
cx q[13], q[48];
measure q[48] -> rec[28];
cx q[15], q[49];
measure q[49] -> rec[29];
