OPENQASM 2.0;
include "qelib1.inc";

qreg q[72];

reset q[29];
reset q[15];
reset q[11];
reset q[31];
reset q[27];
reset q[6];
reset q[20];
reset q[5];
reset q[57];
reset q[40];
reset q[0];
reset q[63];
reset q[25];
reset q[62];
reset q[56];
reset q[59];
reset q[64];
reset q[60];
reset q[66];
reset q[38];
reset q[54];
reset q[48];
reset q[68];
reset q[55];
reset q[65];
reset q[37];
reset q[45];
reset q[42];
reset q[35];
reset q[53];
reset q[50]; h q[50]; // decomposed RX
reset q[47]; h q[47]; // decomposed RX
reset q[41]; h q[41]; // decomposed RX
reset q[34]; h q[34]; // decomposed RX
reset q[23]; h q[23]; // decomposed RX
reset q[22]; h q[22]; // decomposed RX
reset q[18]; h q[18]; // decomposed RX
reset q[17]; h q[17]; // decomposed RX
reset q[12]; h q[12]; // decomposed RX
reset q[10]; h q[10]; // decomposed RX
reset q[70]; h q[70]; // decomposed RX
reset q[71]; h q[71]; // decomposed RX
reset q[46]; h q[46]; // decomposed RX
reset q[67]; h q[67]; // decomposed RX
reset q[9]; h q[9]; // decomposed RX
reset q[30]; h q[30]; // decomposed RX
reset q[21]; h q[21]; // decomposed RX
reset q[16]; h q[16]; // decomposed RX
reset q[19]; h q[19]; // decomposed RX
reset q[4]; h q[4]; // decomposed RX
reset q[2]; h q[2]; // decomposed RX
reset q[58]; h q[58]; // decomposed RX
reset q[32]; h q[32]; // decomposed RX
reset q[61]; h q[61]; // decomposed RX
reset q[36]; h q[36]; // decomposed RX
reset q[69]; h q[69]; // decomposed RX
reset q[44]; h q[44]; // decomposed RX
reset q[51]; h q[51]; // decomposed RX
reset q[52]; h q[52]; // decomposed RX
reset q[49]; h q[49]; // decomposed RX
cx q[21], q[64];
cx q[70], q[54];
cx q[14], q[20];
cx q[43], q[56];
cx q[67], q[65];
cx q[71], q[42];
cx q[10], q[38];
cx q[17], q[25];
cx q[23], q[60];
cx q[34], q[11];
cx q[41], q[55];
cx q[4], q[35];
cx q[3], q[62];
cx q[26], q[57];
cx q[30], q[68];
cx q[46], q[45];
cx q[22], q[48];
cx q[58], q[53];
cx q[9], q[66];
cx q[21], q[63];
cx q[70], q[37];
cx q[12], q[54];
cx q[39], q[14];
cx q[43], q[0];
cx q[36], q[64];
cx q[25], q[20];
cx q[10], q[5];
cx q[11], q[71];
cx q[17], q[34];
cx q[41], q[60];
cx q[51], q[35];
cx q[26], q[6];
cx q[58], q[59];
cx q[0], q[63];
cx q[21], q[40];
cx q[67], q[37];
cx q[70], q[55];
cx q[12], q[65];
cx q[23], q[54];
cx q[39], q[29];
cx q[43], q[15];
cx q[36], q[56];
cx q[25], q[60];
cx q[4], q[17];
cx q[10], q[34];
cx q[13], q[71];
cx q[9], q[58];
cx q[42], q[65];
cx q[38], q[23];
cx q[32], q[39];
cx q[40], q[20];
cx q[21], q[70];
cx q[8], q[0];
cx q[67], q[5];
cx q[12], q[11];
cx q[29], q[43];
cx q[41], q[15];
cx q[61], q[56];
cx q[3], q[25];
cx q[50], q[10];
cx q[42], q[41];
cx q[36], q[67];
cx q[38], q[43];
cx q[40], q[29];
cx q[4], q[21];
cx q[8], q[17];
cx q[13], q[12];
cx q[39], q[62];
cx q[1], q[0];
cx q[50], q[71];
cx q[10], q[57];
cx q[33], q[25];
cx q[59], q[11];
cx q[49], q[4];
cx q[51], q[38];
cx q[44], q[36];
cx q[61], q[40];
cx q[3], q[29];
cx q[13], q[39];
cx q[18], q[42];
cx q[28], q[21];
cx q[43], q[62];
cx q[5], q[8];
cx q[32], q[50];
cx q[46], q[71];
cx q[53], q[10];
cx q[41], q[66];
cx q[51], q[67];
cx q[44], q[13];
cx q[69], q[38];
cx q[61], q[3];
cx q[1], q[4];
cx q[18], q[5];
cx q[28], q[12];
cx q[43], q[57];
cx q[2], q[42];
cx q[33], q[40];
cx q[49], q[28];
cx q[51], q[39];
cx q[44], q[61];
cx q[69], q[32];
cx q[1], q[50];
cx q[7], q[57];
cx q[18], q[21];
cx q[43], q[5];
cx q[63], q[13];
cx q[2], q[55];
cx q[6], q[4];
cx q[26], q[33];
cx q[49], q[51];
cx q[44], q[28];
cx q[69], q[15];
cx q[68], q[61];
cx q[1], q[18];
cx q[20], q[13];
cx q[7], q[3];
cx q[30], q[63];
cx q[34], q[43];
cx q[50], q[0];
cx q[2], q[26];
cx q[22], q[32];
cx q[8], q[5];
cx q[45], q[44];
cx q[69], q[17];
cx q[68], q[1];
cx q[6], q[34];
cx q[7], q[18];
cx q[30], q[23];
cx q[47], q[49];
cx q[50], q[4];
cx q[51], q[31];
cx q[21], q[20];
cx q[2], q[46];
cx q[61], q[28];
cx q[15], q[63];
cx q[32], q[0];
cx q[45], q[68];
cx q[7], q[34];
cx q[30], q[26];
cx q[67], q[31];
cx q[23], q[1];
cx q[29], q[21];
cx q[47], q[69];
cx q[50], q[71];
cx q[17], q[6];
cx q[22], q[46];
cx q[3], q[28];
cx q[33], q[15];
cx q[16], q[51];
cx q[45], q[43];
cx q[65], q[67];
cx q[2], q[30];
cx q[20], q[6];
cx q[12], q[21];
cx q[23], q[26];
cx q[24], q[7];
cx q[29], q[39];
cx q[47], q[48];
cx q[70], q[50];
cx q[18], q[1];
cx q[25], q[17];
cx q[19], q[68];
cx q[16], q[59];
cx q[52], q[45];
cx q[8], q[23];
cx q[12], q[67];
cx q[13], q[20];
cx q[24], q[71];
cx q[47], q[2];
cx q[70], q[22];
cx q[7], q[29];
cx q[40], q[50];
cx q[34], q[1];
cx q[14], q[39];
cx q[17], q[0];
cx q[16], q[48];
cx q[10], q[59];
cx q[54], q[22];
cx q[12], q[13];
cx q[18], q[7];
cx q[28], q[29];
cx q[47], q[71];
cx q[33], q[8];
cx q[45], q[27];
cx q[30], q[24];
cx q[52], q[2];
cx q[25], q[1];
cx q[3], q[40];
cx q[31], q[23];
cx q[4], q[50];
cx q[19], q[17];
cx q[11], q[34];
cx q[37], q[10];
cx q[56], q[67];
cx q[46], q[27];
cx q[12], q[22];
cx q[47], q[70];
cx q[14], q[28];
cx q[24], q[33];
cx q[6], q[7];
cx q[52], q[3];
cx q[25], q[13];
cx q[9], q[23];
cx q[43], q[71];
cx q[57], q[4];
cx q[19], q[64];
cx q[8], q[5];
cx q[11], q[58];
cx q[18], q[21];
cx q[40], q[41];
cx q[42], q[46];
cx q[27], q[33];
cx q[15], q[7];
cx q[22], q[29];
cx q[45], q[47];
cx q[26], q[24];
cx q[12], q[14];
cx q[53], q[52];
cx q[25], q[43];
cx q[9], q[28];
cx q[19], q[18];
cx q[35], q[11];
cx q[57], q[41];
cx q[8], q[10];
cx q[4], q[50];
cx q[32], q[46];
cx q[27], q[26];
cx q[12], q[34];
cx q[15], q[17];
cx q[29], q[33];
cx q[3], q[47];
cx q[23], q[24];
cx q[7], q[14];
cx q[53], q[39];
cx q[25], q[5];
cx q[40], q[22];
cx q[21], q[11];
cx q[19], q[52];
cx q[16], q[12];
cx q[31], q[29];
cx q[9], q[26];
cx q[6], q[46];
cx q[30], q[24];
cx q[3], q[2];
cx q[28], q[23];
cx q[43], q[47];
cx q[62], q[34];
cx q[13], q[14];
cx q[15], q[63];
cx q[53], q[36];
cx q[7], q[41];
cx q[16], q[18];
cx q[9], q[25];
cx q[28], q[24];
cx q[46], q[71];
cx q[22], q[26];
cx q[34], q[39];
cx q[47], q[2];
cx q[23], q[29];
cx q[57], q[43];
cx q[15], q[14];
