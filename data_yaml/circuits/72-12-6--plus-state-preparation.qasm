OPENQASM 2.0;
include "qelib1.inc";

qreg q[72];

reset q[50];
reset q[47];
reset q[43];
reset q[41];
reset q[39];
reset q[34];
reset q[29];
reset q[28];
reset q[26];
reset q[24];
reset q[23];
reset q[22];
reset q[18];
reset q[17];
reset q[15];
reset q[14];
reset q[13];
reset q[12];
reset q[11];
reset q[10];
reset q[70];
reset q[71];
reset q[46];
reset q[67];
reset q[5];
reset q[4];
reset q[3];
reset q[2];
reset q[1];
reset q[0];
reset q[9]; h q[9]; // decomposed RX
reset q[8]; h q[8]; // decomposed RX
reset q[31]; h q[31]; // decomposed RX
reset q[33]; h q[33]; // decomposed RX
reset q[27]; h q[27]; // decomposed RX
reset q[30]; h q[30]; // decomposed RX
reset q[7]; h q[7]; // decomposed RX
reset q[6]; h q[6]; // decomposed RX
reset q[20]; h q[20]; // decomposed RX
reset q[21]; h q[21]; // decomposed RX
reset q[16]; h q[16]; // decomposed RX
reset q[19]; h q[19]; // decomposed RX
reset q[57]; h q[57]; // decomposed RX
reset q[40]; h q[40]; // decomposed RX
reset q[63]; h q[63]; // decomposed RX
reset q[25]; h q[25]; // decomposed RX
reset q[62]; h q[62]; // decomposed RX
reset q[56]; h q[56]; // decomposed RX
reset q[58]; h q[58]; // decomposed RX
reset q[59]; h q[59]; // decomposed RX
reset q[64]; h q[64]; // decomposed RX
reset q[60]; h q[60]; // decomposed RX
reset q[32]; h q[32]; // decomposed RX
reset q[61]; h q[61]; // decomposed RX
reset q[66]; h q[66]; // decomposed RX
reset q[38]; h q[38]; // decomposed RX
reset q[36]; h q[36]; // decomposed RX
reset q[54]; h q[54]; // decomposed RX
reset q[48]; h q[48]; // decomposed RX
reset q[68]; h q[68]; // decomposed RX
reset q[55]; h q[55]; // decomposed RX
reset q[69]; h q[69]; // decomposed RX
reset q[44]; h q[44]; // decomposed RX
reset q[65]; h q[65]; // decomposed RX
reset q[51]; h q[51]; // decomposed RX
reset q[52]; h q[52]; // decomposed RX
reset q[37]; h q[37]; // decomposed RX
reset q[49]; h q[49]; // decomposed RX
reset q[45]; h q[45]; // decomposed RX
reset q[42]; h q[42]; // decomposed RX
reset q[35]; h q[35]; // decomposed RX
reset q[53]; h q[53]; // decomposed RX
cx q[52], q[0];
cx q[44], q[1];
cx q[25], q[3];
cx q[69], q[4];
cx q[42], q[18];
cx q[68], q[2];
cx q[55], q[10];
cx q[53], q[11];
cx q[30], q[12];
cx q[20], q[15];
cx q[27], q[17];
cx q[21], q[24];
cx q[6], q[46];
cx q[19], q[70];
cx q[62], q[14];
cx q[40], q[22];
cx q[66], q[0];
cx q[65], q[1];
cx q[49], q[3];
cx q[35], q[4];
cx q[42], q[5];
cx q[25], q[71];
cx q[37], q[18];
cx q[52], q[26];
cx q[69], q[28];
cx q[44], q[47];
cx q[45], q[68];
cx q[57], q[2];
cx q[30], q[15];
cx q[55], q[41];
cx q[21], q[50];
cx q[16], q[10];
cx q[6], q[13];
cx q[53], q[34];
cx q[31], q[70];
cx q[61], q[0];
cx q[54], q[4];
cx q[25], q[5];
cx q[7], q[71];
cx q[52], q[11];
cx q[66], q[17];
cx q[48], q[18];
cx q[65], q[23];
cx q[20], q[26];
cx q[27], q[28];
cx q[37], q[29];
cx q[64], q[69];
cx q[49], q[44];
cx q[36], q[1];
cx q[38], q[2];
cx q[68], q[3];
cx q[19], q[15];
cx q[30], q[22];
cx q[40], q[42];
cx q[53], q[10];
cx q[8], q[13];
cx q[56], q[50];
cx q[31], q[12];
cx q[59], q[0];
cx q[55], q[4];
cx q[44], q[71];
cx q[9], q[11];
cx q[7], q[14];
cx q[35], q[17];
cx q[57], q[18];
cx q[48], q[23];
cx q[25], q[26];
cx q[61], q[29];
cx q[64], q[39];
cx q[66], q[41];
cx q[52], q[43];
cx q[69], q[47];
cx q[54], q[65];
cx q[21], q[37];
cx q[32], q[20];
cx q[63], q[27];
cx q[58], q[1];
cx q[38], q[5];
cx q[51], q[30];
cx q[56], q[3];
cx q[65], q[0];
cx q[32], q[71];
cx q[36], q[11];
cx q[9], q[14];
cx q[16], q[17];
cx q[33], q[18];
cx q[54], q[22];
cx q[6], q[23];
cx q[55], q[24];
cx q[62], q[26];
cx q[20], q[34];
cx q[40], q[41];
cx q[59], q[43];
cx q[48], q[47];
cx q[61], q[27];
cx q[45], q[7];
cx q[69], q[15];
cx q[57], q[21];
cx q[52], q[68];
cx q[63], q[37];
cx q[64], q[42];
cx q[25], q[35];
cx q[66], q[49];
cx q[51], q[1];
cx q[38], q[4];
cx q[44], q[13];
cx q[30], q[67];
cx q[35], q[0];
cx q[60], q[71];
cx q[65], q[10];
cx q[55], q[15];
cx q[54], q[17];
cx q[9], q[18];
cx q[19], q[22];
cx q[36], q[23];
cx q[7], q[24];
cx q[6], q[28];
cx q[32], q[29];
cx q[69], q[34];
cx q[25], q[39];
cx q[57], q[41];
cx q[58], q[43];
cx q[27], q[47];
cx q[33], q[50];
cx q[45], q[59];
cx q[8], q[16];
cx q[62], q[68];
cx q[42], q[20];
cx q[48], q[64];
cx q[21], q[11];
cx q[63], q[66];
cx q[53], q[52];
cx q[61], q[5];
cx q[56], q[67];
cx q[51], q[26];
cx q[69], q[3];
cx q[68], q[4];
cx q[31], q[15];
cx q[16], q[23];
cx q[8], q[28];
cx q[45], q[29];
cx q[54], q[34];
cx q[61], q[39];
cx q[59], q[41];
cx q[62], q[43];
cx q[58], q[47];
cx q[63], q[50];
cx q[40], q[0];
cx q[42], q[1];
cx q[20], q[30];
cx q[27], q[6];
cx q[38], q[57];
cx q[32], q[25];
cx q[33], q[7];
cx q[49], q[19];
cx q[52], q[21];
cx q[60], q[9];
cx q[36], q[35];
cx q[37], q[65];
cx q[44], q[48];
cx q[55], q[53];
cx q[66], q[64];
cx q[58], q[2];
cx q[68], q[5];
cx q[59], q[10];
cx q[31], q[26];
cx q[16], q[28];
cx q[9], q[29];
cx q[40], q[34];
cx q[6], q[39];
cx q[7], q[41];
cx q[19], q[43];
cx q[56], q[47];
cx q[62], q[50];
cx q[65], q[8];
cx q[42], q[30];
cx q[32], q[27];
cx q[44], q[33];
cx q[53], q[36];
cx q[60], q[37];
cx q[25], q[45];
cx q[63], q[55];
cx q[51], q[69];
cx q[61], q[20];
cx q[35], q[21];
cx q[38], q[66];
cx q[64], q[49];
cx q[57], q[48];
cx q[54], q[52];
cx q[58], q[11];
cx q[19], q[26];
cx q[7], q[29];
cx q[31], q[34];
cx q[8], q[39];
cx q[9], q[41];
cx q[30], q[43];
cx q[16], q[47];
cx q[36], q[21];
cx q[55], q[66];
cx q[60], q[53];
cx q[45], q[27];
cx q[65], q[51];
cx q[40], q[52];
cx q[42], q[6];
cx q[35], q[20];
cx q[49], q[33];
cx q[37], q[64];
cx q[62], q[44];
cx q[69], q[25];
cx q[56], q[61];
cx q[68], q[38];
cx q[59], q[57];
cx q[32], q[63];
cx q[48], q[54];
