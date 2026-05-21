OPENQASM 2.0;
include "qelib1.inc";

qreg q[90];

reset q[45];
reset q[42];
reset q[39];
reset q[36];
reset q[31];
reset q[2];
reset q[70];
reset q[48];
reset q[61];
reset q[73];
reset q[51];
reset q[64];
reset q[76];
reset q[54];
reset q[67];
reset q[79];
reset q[88];
reset q[83];
reset q[1];
reset q[69];
reset q[47];
reset q[60];
reset q[72];
reset q[50];
reset q[63];
reset q[75];
reset q[53];
reset q[66];
reset q[78];
reset q[87];
reset q[82];
reset q[3];
reset q[56];
reset q[68];
reset q[71];
reset q[49];
reset q[74];
reset q[52];
reset q[65];
reset q[77];
reset q[86];
reset q[84]; h q[84]; // decomposed RX
reset q[80]; h q[80]; // decomposed RX
reset q[44]; h q[44]; // decomposed RX
reset q[43]; h q[43]; // decomposed RX
reset q[41]; h q[41]; // decomposed RX
reset q[40]; h q[40]; // decomposed RX
reset q[38]; h q[38]; // decomposed RX
reset q[37]; h q[37]; // decomposed RX
reset q[89]; h q[89]; // decomposed RX
reset q[85]; h q[85]; // decomposed RX
reset q[33]; h q[33]; // decomposed RX
reset q[30]; h q[30]; // decomposed RX
reset q[29]; h q[29]; // decomposed RX
reset q[28]; h q[28]; // decomposed RX
reset q[27]; h q[27]; // decomposed RX
reset q[26]; h q[26]; // decomposed RX
reset q[25]; h q[25]; // decomposed RX
reset q[24]; h q[24]; // decomposed RX
reset q[23]; h q[23]; // decomposed RX
reset q[22]; h q[22]; // decomposed RX
reset q[21]; h q[21]; // decomposed RX
reset q[35]; h q[35]; // decomposed RX
reset q[34]; h q[34]; // decomposed RX
reset q[18]; h q[18]; // decomposed RX
reset q[17]; h q[17]; // decomposed RX
reset q[16]; h q[16]; // decomposed RX
reset q[15]; h q[15]; // decomposed RX
reset q[14]; h q[14]; // decomposed RX
reset q[13]; h q[13]; // decomposed RX
reset q[12]; h q[12]; // decomposed RX
reset q[11]; h q[11]; // decomposed RX
reset q[10]; h q[10]; // decomposed RX
reset q[9]; h q[9]; // decomposed RX
reset q[8]; h q[8]; // decomposed RX
reset q[20]; h q[20]; // decomposed RX
reset q[19]; h q[19]; // decomposed RX
reset q[0]; h q[0]; // decomposed RX
reset q[46]; h q[46]; // decomposed RX
reset q[59]; h q[59]; // decomposed RX
reset q[62]; h q[62]; // decomposed RX
reset q[81]; h q[81]; // decomposed RX
cx q[38], q[52];
cx q[40], q[71];
cx q[80], q[3];
cx q[30], q[56];
cx q[37], q[74];
cx q[41], q[49];
cx q[43], q[42];
cx q[55], q[31];
cx q[57], q[87];
cx q[20], q[65];
cx q[58], q[54];
cx q[5], q[79];
cx q[89], q[77];
cx q[84], q[86];
cx q[33], q[3];
cx q[38], q[36];
cx q[40], q[39];
cx q[80], q[45];
cx q[8], q[52];
cx q[42], q[68];
cx q[44], q[56];
cx q[11], q[49];
cx q[4], q[87];
cx q[57], q[82];
cx q[85], q[65];
cx q[58], q[88];
cx q[5], q[54];
cx q[74], q[38];
cx q[6], q[36];
cx q[31], q[33];
cx q[37], q[39];
cx q[41], q[40];
cx q[43], q[45];
cx q[55], q[80];
cx q[71], q[42];
cx q[28], q[68];
cx q[4], q[75];
cx q[24], q[49];
cx q[87], q[47];
cx q[81], q[82];
cx q[57], q[63];
cx q[35], q[65];
cx q[85], q[89];
cx q[88], q[83];
cx q[58], q[64];
cx q[5], q[73];
cx q[16], q[56];
cx q[21], q[52];
cx q[3], q[84];
cx q[54], q[2];
cx q[62], q[38];
cx q[59], q[43];
cx q[46], q[41];
cx q[0], q[80];
cx q[7], q[37];
cx q[8], q[6];
cx q[9], q[74];
cx q[30], q[31];
cx q[44], q[55];
cx q[27], q[71];
cx q[32], q[33];
cx q[14], q[68];
cx q[75], q[78];
cx q[4], q[69];
cx q[47], q[50];
cx q[81], q[85];
cx q[63], q[66];
cx q[57], q[60];
cx q[89], q[36];
cx q[86], q[87];
cx q[79], q[88];
cx q[64], q[67];
cx q[73], q[76];
cx q[58], q[61];
cx q[5], q[70];
cx q[2], q[48];
cx q[54], q[51];
cx q[82], q[83];
cx q[62], q[40];
cx q[59], q[44];
cx q[46], q[43];
cx q[9], q[7];
cx q[11], q[8];
cx q[28], q[30];
cx q[29], q[0];
cx q[12], q[71];
cx q[23], q[74];
cx q[77], q[37];
cx q[69], q[72];
cx q[18], q[4];
cx q[34], q[78];
cx q[50], q[1];
cx q[47], q[53];
cx q[81], q[84];
cx q[80], q[55];
cx q[86], q[89];
cx q[65], q[66];
cx q[56], q[57];
cx q[87], q[88];
cx q[10], q[62];
cx q[11], q[9];
cx q[13], q[59];
cx q[26], q[46];
cx q[27], q[28];
cx q[29], q[30];
cx q[17], q[0];
cx q[19], q[77];
cx q[20], q[7];
cx q[43], q[42];
cx q[3], q[4];
cx q[52], q[53];
cx q[74], q[75];
cx q[71], q[72];
cx q[49], q[50];
cx q[68], q[69];
cx q[89], q[85];
cx q[40], q[39];
cx q[55], q[45];
cx q[36], q[37];
cx q[57], q[58];
cx q[81], q[80];
cx q[66], q[67];
cx q[10], q[9];
cx q[12], q[11];
cx q[22], q[62];
cx q[25], q[59];
cx q[26], q[27];
cx q[29], q[32];
cx q[15], q[46];
cx q[19], q[20];
cx q[6], q[7];
cx q[77], q[78];
cx q[0], q[1];
cx q[42], q[41];
cx q[43], q[44];
cx q[69], q[70];
cx q[4], q[5];
cx q[75], q[76];
cx q[72], q[73];
cx q[53], q[54];
cx q[50], q[51];
cx q[13], q[10];
cx q[14], q[12];
cx q[22], q[23];
cx q[25], q[27];
cx q[26], q[29];
cx q[33], q[32];
cx q[59], q[60];
cx q[62], q[63];
cx q[46], q[47];
cx q[9], q[8];
cx q[20], q[6];
cx q[78], q[79];
cx q[1], q[2];
cx q[13], q[11];
cx q[15], q[14];
cx q[22], q[25];
cx q[24], q[26];
cx q[30], q[29];
cx q[32], q[31];
cx q[33], q[84];
cx q[63], q[64];
cx q[60], q[61];
cx q[47], q[48];
cx q[17], q[15];
cx q[35], q[22];
cx q[14], q[13];
cx q[23], q[24];
cx q[27], q[26];
cx q[11], q[10];
cx q[16], q[14];
cx q[18], q[17];
cx q[34], q[35];
cx q[21], q[23];
cx q[13], q[12];
cx q[26], q[25];
cx q[27], q[28];
cx q[18], q[3];
cx q[34], q[77];
cx q[17], q[16];
cx q[35], q[21];
cx q[14], q[15];
cx q[23], q[22];
