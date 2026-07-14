OPENQASM 2.0;
include "qelib1.inc";

qreg q[94];

h q[5];
h q[2];
h q[15];
h q[27];
h q[1];
h q[0];
h q[23];
h q[14];
h q[26];
h q[44];
h q[9];
h q[8];
h q[7];
h q[24];
h q[42];
h q[35];
h q[18];
h q[17];
h q[16];
h q[40];
h q[33];
h q[30];
h q[37];
h q[32];
h q[28];
h q[52];
h q[66];
h q[80];
h q[65];
h q[79];
h q[93];
h q[54];
h q[56];
h q[58];
h q[59];
h q[61];
h q[63];
h q[68];
h q[70];
h q[72];
h q[73];
h q[75];
h q[77];
h q[82];
h q[84];
h q[86];
h q[87];
h q[89];
h q[91];
barrier q;

cx q[52], q[6];
cx q[54], q[4];
cx q[56], q[3];
cx q[58], q[38];
barrier q;

cx q[5], q[52];
cx q[15], q[54];
cx q[1], q[56];
cx q[23], q[58];
barrier q;

cx q[2], q[54];
cx q[27], q[56];
cx q[0], q[58];
barrier q;

cx q[14], q[54];
cx q[26], q[56];
cx q[44], q[58];
barrier q;

cx q[52], q[6];
cx q[54], q[4];
cx q[56], q[3];
cx q[58], q[38];
barrier q;

cx q[65], q[39];
cx q[63], q[43];
cx q[61], q[25];
cx q[59], q[13];
barrier q;

cx q[38], q[65];
cx q[3], q[63];
cx q[4], q[61];
cx q[6], q[59];
barrier q;

cx q[44], q[63];
cx q[26], q[61];
cx q[14], q[59];
barrier q;

cx q[7], q[63];
cx q[8], q[61];
cx q[9], q[59];
barrier q;

cx q[65], q[39];
cx q[63], q[43];
cx q[61], q[25];
cx q[59], q[13];
barrier q;

cx q[66], q[12];
cx q[68], q[11];
cx q[70], q[10];
cx q[72], q[45];
barrier q;

cx q[13], q[66];
cx q[25], q[68];
cx q[43], q[70];
cx q[39], q[72];
barrier q;

cx q[9], q[68];
cx q[8], q[70];
cx q[7], q[72];
barrier q;

cx q[24], q[68];
cx q[42], q[70];
cx q[35], q[72];
barrier q;

cx q[66], q[12];
cx q[68], q[11];
cx q[70], q[10];
cx q[72], q[45];
barrier q;

cx q[79], q[46];
cx q[77], q[34];
cx q[75], q[41];
cx q[73], q[22];
barrier q;

cx q[45], q[79];
cx q[10], q[77];
cx q[11], q[75];
cx q[12], q[73];
barrier q;

cx q[35], q[77];
cx q[42], q[75];
cx q[24], q[73];
barrier q;

cx q[16], q[77];
cx q[17], q[75];
cx q[18], q[73];
barrier q;

cx q[79], q[46];
cx q[77], q[34];
cx q[75], q[41];
cx q[73], q[22];
barrier q;

cx q[80], q[21];
cx q[82], q[20];
cx q[84], q[19];
cx q[86], q[48];
barrier q;

cx q[22], q[80];
cx q[41], q[82];
cx q[34], q[84];
cx q[46], q[86];
barrier q;

cx q[18], q[82];
cx q[17], q[84];
cx q[16], q[86];
barrier q;

cx q[40], q[82];
cx q[33], q[84];
cx q[30], q[86];
barrier q;

cx q[80], q[21];
cx q[82], q[20];
cx q[84], q[19];
cx q[86], q[48];
barrier q;

cx q[93], q[47];
cx q[91], q[29];
cx q[89], q[31];
cx q[87], q[36];
barrier q;

cx q[48], q[93];
cx q[19], q[91];
cx q[20], q[89];
cx q[21], q[87];
barrier q;

cx q[30], q[91];
cx q[33], q[89];
cx q[40], q[87];
barrier q;

cx q[28], q[91];
cx q[32], q[89];
cx q[37], q[87];
barrier q;

cx q[93], q[47];
cx q[91], q[29];
cx q[89], q[31];
cx q[87], q[36];
barrier q;

