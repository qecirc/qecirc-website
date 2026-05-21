OPENQASM 2.0;
include "qelib1.inc";

qreg q[72];

reset q[70];
reset q[71];
reset q[46];
reset q[67];
reset q[31];
reset q[33];
reset q[27];
reset q[30];
reset q[20];
reset q[21];
reset q[16];
reset q[19];
reset q[57];
reset q[40];
reset q[63];
reset q[25];
reset q[62];
reset q[56];
reset q[58];
reset q[59];
reset q[64];
reset q[60];
reset q[32];
reset q[61];
reset q[66];
reset q[38];
reset q[36];
reset q[54];
reset q[48];
reset q[68];
reset q[55];
reset q[69];
reset q[44];
reset q[65];
reset q[51];
reset q[52];
reset q[37];
reset q[49];
reset q[45];
reset q[42];
reset q[35];
reset q[53];
reset q[50]; h q[50]; // decomposed RX
reset q[47]; h q[47]; // decomposed RX
reset q[43]; h q[43]; // decomposed RX
reset q[41]; h q[41]; // decomposed RX
reset q[39]; h q[39]; // decomposed RX
reset q[34]; h q[34]; // decomposed RX
reset q[29]; h q[29]; // decomposed RX
reset q[28]; h q[28]; // decomposed RX
reset q[26]; h q[26]; // decomposed RX
reset q[24]; h q[24]; // decomposed RX
reset q[23]; h q[23]; // decomposed RX
reset q[22]; h q[22]; // decomposed RX
reset q[18]; h q[18]; // decomposed RX
reset q[17]; h q[17]; // decomposed RX
reset q[15]; h q[15]; // decomposed RX
reset q[14]; h q[14]; // decomposed RX
reset q[13]; h q[13]; // decomposed RX
reset q[12]; h q[12]; // decomposed RX
reset q[11]; h q[11]; // decomposed RX
reset q[10]; h q[10]; // decomposed RX
reset q[9]; h q[9]; // decomposed RX
reset q[8]; h q[8]; // decomposed RX
reset q[7]; h q[7]; // decomposed RX
reset q[6]; h q[6]; // decomposed RX
reset q[5]; h q[5]; // decomposed RX
reset q[4]; h q[4]; // decomposed RX
reset q[3]; h q[3]; // decomposed RX
reset q[2]; h q[2]; // decomposed RX
reset q[1]; h q[1]; // decomposed RX
reset q[0]; h q[0]; // decomposed RX
cx q[0], q[66];
cx q[1], q[44];
cx q[2], q[42];
cx q[4], q[35];
cx q[5], q[68];
cx q[7], q[16];
cx q[8], q[53];
cx q[9], q[45];
cx q[10], q[52];
cx q[14], q[56];
cx q[18], q[54];
cx q[22], q[48];
cx q[23], q[49];
cx q[34], q[61];
cx q[6], q[19];
cx q[11], q[70];
cx q[28], q[58];
cx q[66], q[51];
cx q[0], q[63];
cx q[1], q[55];
cx q[2], q[56];
cx q[5], q[25];
cx q[8], q[32];
cx q[9], q[35];
cx q[10], q[71];
cx q[12], q[16];
cx q[14], q[20];
cx q[15], q[48];
cx q[18], q[64];
cx q[22], q[27];
cx q[23], q[69];
cx q[26], q[53];
cx q[29], q[68];
cx q[34], q[60];
cx q[47], q[45];
cx q[50], q[52];
cx q[3], q[49];
cx q[7], q[62];
cx q[55], q[69];
cx q[0], q[61];
cx q[1], q[36];
cx q[4], q[51];
cx q[5], q[40];
cx q[8], q[25];
cx q[9], q[57];
cx q[10], q[42];
cx q[13], q[16];
cx q[17], q[20];
cx q[22], q[63];
cx q[23], q[27];
cx q[24], q[56];
cx q[26], q[45];
cx q[29], q[32];
cx q[34], q[71];
cx q[47], q[64];
cx q[48], q[54];
cx q[12], q[19];
cx q[28], q[35];
cx q[52], q[53];
cx q[15], q[62];
cx q[1], q[60];
cx q[2], q[55];
cx q[6], q[40];
cx q[8], q[30];
cx q[9], q[59];
cx q[10], q[57];
cx q[11], q[36];
cx q[17], q[66];
cx q[18], q[20];
cx q[23], q[37];
cx q[34], q[70];
cx q[39], q[42];
cx q[43], q[71];
cx q[50], q[54];
cx q[63], q[44];
cx q[68], q[61];
cx q[25], q[38];
cx q[69], q[32];
cx q[51], q[58];
cx q[27], q[64];
cx q[16], q[48];
cx q[56], q[45];
cx q[3], q[53];
cx q[24], q[31];
cx q[2], q[65];
cx q[8], q[40];
cx q[9], q[27];
cx q[10], q[51];
cx q[11], q[63];
cx q[13], q[59];
cx q[14], q[16];
cx q[18], q[68];
cx q[23], q[33];
cx q[26], q[57];
cx q[29], q[58];
cx q[34], q[37];
cx q[39], q[70];
cx q[41], q[42];
cx q[47], q[69];
cx q[50], q[71];
cx q[61], q[60];
cx q[66], q[52];
cx q[19], q[54];
cx q[55], q[25];
cx q[36], q[38];
cx q[49], q[48];
cx q[56], q[32];
cx q[20], q[44];
cx q[22], q[30];
cx q[35], q[64];
cx q[5], q[42];
cx q[6], q[69];
cx q[9], q[25];
cx q[10], q[37];
cx q[11], q[51];
cx q[12], q[55];
cx q[15], q[49];
cx q[23], q[30];
cx q[24], q[66];
cx q[26], q[59];
cx q[28], q[33];
cx q[34], q[38];
cx q[39], q[67];
cx q[41], q[46];
cx q[43], q[44];
cx q[47], q[68];
cx q[50], q[61];
cx q[16], q[20];
cx q[19], q[21];
cx q[36], q[65];
cx q[60], q[63];
cx q[52], q[54];
cx q[70], q[64];
cx q[40], q[62];
cx q[35], q[32];
cx q[71], q[56];
cx q[58], q[53];
cx q[45], q[48];
cx q[3], q[57];
cx q[31], q[27];
cx q[3], q[52];
cx q[6], q[55];
cx q[7], q[49];
cx q[10], q[61];
cx q[12], q[59];
cx q[13], q[19];
cx q[15], q[21];
cx q[17], q[60];
cx q[22], q[38];
cx q[23], q[36];
cx q[24], q[25];
cx q[26], q[33];
cx q[28], q[31];
cx q[29], q[30];
cx q[34], q[62];
cx q[43], q[67];
cx q[47], q[51];
cx q[50], q[57];
cx q[16], q[44];
cx q[69], q[45];
cx q[27], q[66];
cx q[70], q[46];
cx q[40], q[56];
cx q[42], q[65];
cx q[58], q[37];
cx q[71], q[68];
cx q[20], q[32];
cx q[53], q[54];
cx q[63], q[35];
cx q[48], q[64];
cx q[11], q[42];
cx q[15], q[52];
cx q[17], q[21];
cx q[18], q[19];
cx q[34], q[35];
cx q[39], q[40];
cx q[41], q[66];
cx q[43], q[60];
cx q[47], q[70];
cx q[50], q[51];
cx q[30], q[33];
cx q[16], q[55];
cx q[71], q[67];
cx q[27], q[31];
cx q[69], q[49];
cx q[46], q[58];
cx q[45], q[59];
cx q[61], q[64];
cx q[20], q[36];
cx q[62], q[57];
cx q[25], q[37];
cx q[53], q[63];
cx q[44], q[56];
cx q[32], q[38];
cx q[48], q[68];
cx q[54], q[65];
cx q[14], q[19];
cx q[15], q[16];
cx q[18], q[21];
cx q[23], q[25];
cx q[24], q[30];
cx q[26], q[27];
cx q[29], q[31];
cx q[39], q[63];
cx q[41], q[67];
cx q[43], q[46];
cx q[47], q[71];
cx q[50], q[70];
cx q[20], q[61];
cx q[33], q[49];
cx q[35], q[36];
cx q[44], q[45];
cx q[53], q[62];
cx q[37], q[42];
cx q[57], q[59];
cx q[48], q[51];
cx q[54], q[55];
cx q[32], q[52];
cx q[68], q[60];
cx q[56], q[69];
cx q[38], q[40];
cx q[65], q[58];
cx q[64], q[66];
