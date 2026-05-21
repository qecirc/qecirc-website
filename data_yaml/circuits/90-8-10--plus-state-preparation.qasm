OPENQASM 2.0;
include "qelib1.inc";

qreg q[90];

reset q[84];
reset q[80];
reset q[55];
reset q[45];
reset q[36];
reset q[89];
reset q[85];
reset q[18];
reset q[14];
reset q[13];
reset q[12];
reset q[11];
reset q[10];
reset q[9];
reset q[8];
reset q[7];
reset q[6];
reset q[5];
reset q[2];
reset q[51];
reset q[54];
reset q[4];
reset q[1];
reset q[69];
reset q[60];
reset q[72];
reset q[63];
reset q[75];
reset q[53];
reset q[66];
reset q[82];
reset q[0];
reset q[56];
reset q[68];
reset q[59];
reset q[49];
reset q[62];
reset q[65];
reset q[77];
reset q[86];
reset q[81];
reset q[44]; h q[44]; // decomposed RX
reset q[43]; h q[43]; // decomposed RX
reset q[42]; h q[42]; // decomposed RX
reset q[41]; h q[41]; // decomposed RX
reset q[40]; h q[40]; // decomposed RX
reset q[39]; h q[39]; // decomposed RX
reset q[38]; h q[38]; // decomposed RX
reset q[37]; h q[37]; // decomposed RX
reset q[33]; h q[33]; // decomposed RX
reset q[32]; h q[32]; // decomposed RX
reset q[31]; h q[31]; // decomposed RX
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
reset q[17]; h q[17]; // decomposed RX
reset q[16]; h q[16]; // decomposed RX
reset q[15]; h q[15]; // decomposed RX
reset q[20]; h q[20]; // decomposed RX
reset q[19]; h q[19]; // decomposed RX
reset q[58]; h q[58]; // decomposed RX
reset q[70]; h q[70]; // decomposed RX
reset q[48]; h q[48]; // decomposed RX
reset q[61]; h q[61]; // decomposed RX
reset q[73]; h q[73]; // decomposed RX
reset q[64]; h q[64]; // decomposed RX
reset q[76]; h q[76]; // decomposed RX
reset q[67]; h q[67]; // decomposed RX
reset q[79]; h q[79]; // decomposed RX
reset q[88]; h q[88]; // decomposed RX
reset q[83]; h q[83]; // decomposed RX
reset q[57]; h q[57]; // decomposed RX
reset q[47]; h q[47]; // decomposed RX
reset q[50]; h q[50]; // decomposed RX
reset q[78]; h q[78]; // decomposed RX
reset q[87]; h q[87]; // decomposed RX
reset q[3]; h q[3]; // decomposed RX
reset q[46]; h q[46]; // decomposed RX
reset q[71]; h q[71]; // decomposed RX
reset q[74]; h q[74]; // decomposed RX
reset q[52]; h q[52]; // decomposed RX
cx q[74], q[49];
cx q[50], q[72];
cx q[76], q[51];
cx q[73], q[9];
cx q[71], q[10];
cx q[48], q[12];
cx q[47], q[45];
cx q[46], q[56];
cx q[58], q[2];
cx q[61], q[14];
cx q[83], q[18];
cx q[79], q[6];
cx q[67], q[7];
cx q[64], q[11];
cx q[52], q[8];
cx q[3], q[55];
cx q[78], q[36];
cx q[87], q[84];
cx q[49], q[71];
cx q[10], q[72];
cx q[47], q[60];
cx q[51], q[9];
cx q[73], q[12];
cx q[48], q[13];
cx q[57], q[45];
cx q[46], q[59];
cx q[50], q[75];
cx q[58], q[14];
cx q[88], q[18];
cx q[83], q[80];
cx q[8], q[53];
cx q[55], q[4];
cx q[67], q[6];
cx q[9], q[74];
cx q[71], q[68];
cx q[45], q[56];
cx q[12], q[60];
cx q[72], q[69];
cx q[57], q[1];
cx q[10], q[76];
cx q[48], q[61];
cx q[70], q[13];
cx q[49], q[62];
cx q[50], q[63];
cx q[51], q[64];
cx q[79], q[18];
cx q[80], q[81];
cx q[88], q[85];
cx q[6], q[77];
cx q[74], q[65];
cx q[12], q[59];
cx q[13], q[68];
cx q[56], q[0];
cx q[9], q[75];
cx q[60], q[69];
cx q[14], q[1];
cx q[45], q[2];
cx q[70], q[5];
cx q[76], q[7];
cx q[61], q[11];
cx q[64], q[54];
cx q[88], q[89];
cx q[19], q[85];
cx q[36], q[6];
cx q[40], q[10];
cx q[7], q[65];
cx q[11], q[62];
cx q[59], q[68];
cx q[14], q[0];
cx q[1], q[82];
cx q[75], q[66];
cx q[60], q[63];
cx q[13], q[69];
cx q[58], q[5];
cx q[2], q[18];
cx q[74], q[52];
cx q[8], q[54];
cx q[64], q[51];
cx q[20], q[89];
cx q[15], q[45];
cx q[39], q[9];
cx q[42], q[12];
cx q[61], q[48];
cx q[34], q[85];
cx q[79], q[88];
cx q[21], q[36];
cx q[25], q[40];
cx q[0], q[81];
cx q[18], q[86];
cx q[59], q[62];
cx q[80], q[82];
cx q[7], q[66];
cx q[75], q[53];
cx q[11], q[63];
cx q[55], q[5];
cx q[69], q[57];
cx q[68], q[56];
cx q[65], q[77];
cx q[54], q[67];
cx q[44], q[14];
cx q[38], q[8];
cx q[43], q[13];
cx q[72], q[60];
cx q[76], q[64];
cx q[73], q[51];
cx q[70], q[58];
cx q[35], q[89];
cx q[24], q[39];
cx q[27], q[42];
cx q[30], q[45];
cx q[81], q[86];
cx q[62], q[52];
cx q[56], q[3];
cx q[82], q[87];
cx q[66], q[78];
cx q[63], q[53];
cx q[57], q[4];
cx q[84], q[18];
cx q[5], q[83];
cx q[16], q[55];
cx q[17], q[80];
cx q[37], q[7];
cx q[41], q[11];
cx q[71], q[59];
cx q[46], q[68];
cx q[47], q[69];
cx q[67], q[20];
cx q[23], q[38];
cx q[28], q[43];
cx q[29], q[44];
cx q[62], q[49];
cx q[18], q[87];
cx q[6], q[78];
cx q[63], q[50];
cx q[2], q[5];
cx q[83], q[19];
cx q[0], q[56];
cx q[53], q[66];
cx q[4], q[82];
cx q[1], q[57];
cx q[52], q[65];
cx q[3], q[81];
cx q[22], q[37];
cx q[26], q[41];
cx q[31], q[55];
cx q[32], q[80];
cx q[33], q[84];
