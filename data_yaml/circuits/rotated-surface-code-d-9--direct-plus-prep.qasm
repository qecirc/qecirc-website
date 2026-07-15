OPENQASM 2.0;
include "qelib1.inc";

qreg q[81];

h q[8];
h q[19];
h q[3];
h q[32];
h q[2];
h q[48];
h q[1];
h q[42];
h q[0];
h q[18];
h q[31];
h q[47];
h q[74];
h q[12];
h q[11];
h q[10];
h q[9];
h q[29];
h q[45];
h q[72];
h q[63];
h q[23];
h q[22];
h q[21];
h q[20];
h q[43];
h q[70];
h q[61];
h q[56];
h q[36];
h q[35];
h q[34];
h q[33];
h q[68];
h q[59];
h q[54];
h q[51];
h q[65];
h q[57];
h q[53];
h q[49];
barrier q;

cx q[18], q[6];
cx q[31], q[5];
cx q[47], q[4];
cx q[74], q[67];
barrier q;

cx q[19], q[6];
cx q[32], q[5];
cx q[48], q[4];
cx q[42], q[67];
barrier q;

cx q[8], q[7];
cx q[3], q[6];
cx q[2], q[5];
cx q[1], q[4];
cx q[0], q[67];
barrier q;

cx q[9], q[73];
cx q[10], q[46];
cx q[11], q[30];
cx q[12], q[16];
barrier q;

cx q[74], q[73];
cx q[47], q[46];
cx q[31], q[30];
cx q[18], q[16];
barrier q;

cx q[67], q[66];
cx q[4], q[73];
cx q[5], q[46];
cx q[6], q[30];
cx q[7], q[16];
barrier q;

cx q[29], q[15];
cx q[45], q[14];
cx q[72], q[13];
cx q[63], q[76];
barrier q;

cx q[12], q[15];
cx q[11], q[14];
cx q[10], q[13];
cx q[9], q[76];
barrier q;

cx q[16], q[17];
cx q[30], q[15];
cx q[46], q[14];
cx q[73], q[13];
cx q[66], q[76];
barrier q;

cx q[20], q[62];
cx q[21], q[71];
cx q[22], q[44];
cx q[23], q[28];
barrier q;

cx q[63], q[62];
cx q[72], q[71];
cx q[45], q[44];
cx q[29], q[28];
barrier q;

cx q[76], q[75];
cx q[13], q[62];
cx q[14], q[71];
cx q[15], q[44];
cx q[17], q[28];
barrier q;

cx q[43], q[26];
cx q[70], q[25];
cx q[61], q[24];
cx q[56], q[78];
barrier q;

cx q[23], q[26];
cx q[22], q[25];
cx q[21], q[24];
cx q[20], q[78];
barrier q;

cx q[28], q[27];
cx q[44], q[26];
cx q[71], q[25];
cx q[62], q[24];
cx q[75], q[78];
barrier q;

cx q[33], q[55];
cx q[34], q[60];
cx q[35], q[69];
cx q[36], q[40];
barrier q;

cx q[56], q[55];
cx q[61], q[60];
cx q[70], q[69];
cx q[43], q[40];
barrier q;

cx q[78], q[77];
cx q[24], q[55];
cx q[25], q[60];
cx q[26], q[69];
cx q[27], q[40];
barrier q;

cx q[68], q[39];
cx q[59], q[38];
cx q[54], q[37];
cx q[51], q[79];
barrier q;

cx q[36], q[39];
cx q[35], q[38];
cx q[34], q[37];
cx q[33], q[79];
barrier q;

cx q[40], q[41];
cx q[69], q[39];
cx q[60], q[38];
cx q[55], q[37];
cx q[77], q[79];
barrier q;

cx q[49], q[50];
cx q[53], q[52];
cx q[57], q[58];
cx q[65], q[64];
barrier q;

cx q[51], q[50];
cx q[54], q[52];
cx q[59], q[58];
cx q[68], q[64];
barrier q;

cx q[79], q[80];
cx q[37], q[50];
cx q[38], q[52];
cx q[39], q[58];
cx q[41], q[64];
barrier q;

