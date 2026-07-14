OPENQASM 2.0;
include "qelib1.inc";

qreg q[81];

h q[19];
h q[12];
h q[23];
h q[36];
h q[65];
h q[58];
h q[69];
h q[44];
h q[30];
h q[3];
h q[32];
h q[11];
h q[22];
h q[35];
h q[57];
h q[52];
h q[60];
h q[71];
h q[46];
h q[2];
h q[48];
h q[10];
h q[21];
h q[34];
h q[53];
h q[50];
h q[55];
h q[62];
h q[73];
h q[1];
h q[42];
h q[9];
h q[20];
h q[33];
h q[49];
h q[80];
h q[77];
h q[75];
h q[66];
h q[0];
barrier q;

cx q[19], q[18];
cx q[12], q[29];
cx q[23], q[43];
cx q[36], q[68];
barrier q;

cx q[19], q[7];
cx q[12], q[17];
cx q[23], q[27];
cx q[36], q[41];
barrier q;

cx q[19], q[8];
cx q[12], q[16];
cx q[23], q[28];
cx q[36], q[40];
cx q[65], q[64];
barrier q;

cx q[58], q[39];
cx q[69], q[26];
cx q[44], q[15];
cx q[30], q[6];
barrier q;

cx q[58], q[68];
cx q[69], q[43];
cx q[44], q[29];
cx q[30], q[18];
barrier q;

cx q[58], q[65];
cx q[69], q[36];
cx q[44], q[23];
cx q[30], q[12];
cx q[3], q[19];
barrier q;

cx q[32], q[31];
cx q[11], q[45];
cx q[22], q[70];
cx q[35], q[59];
barrier q;

cx q[32], q[6];
cx q[11], q[15];
cx q[22], q[26];
cx q[35], q[39];
barrier q;

cx q[32], q[3];
cx q[11], q[30];
cx q[22], q[44];
cx q[35], q[69];
cx q[57], q[58];
barrier q;

cx q[52], q[38];
cx q[60], q[25];
cx q[71], q[14];
cx q[46], q[5];
barrier q;

cx q[52], q[59];
cx q[60], q[70];
cx q[71], q[45];
cx q[46], q[31];
barrier q;

cx q[52], q[57];
cx q[60], q[35];
cx q[71], q[22];
cx q[46], q[11];
cx q[2], q[32];
barrier q;

cx q[48], q[47];
cx q[10], q[72];
cx q[21], q[61];
cx q[34], q[54];
barrier q;

cx q[48], q[5];
cx q[10], q[14];
cx q[21], q[25];
cx q[34], q[38];
barrier q;

cx q[48], q[2];
cx q[10], q[46];
cx q[21], q[71];
cx q[34], q[60];
cx q[53], q[52];
barrier q;

cx q[50], q[37];
cx q[55], q[24];
cx q[62], q[13];
cx q[73], q[4];
barrier q;

cx q[50], q[54];
cx q[55], q[61];
cx q[62], q[72];
cx q[73], q[47];
barrier q;

cx q[50], q[53];
cx q[55], q[34];
cx q[62], q[21];
cx q[73], q[10];
cx q[1], q[48];
barrier q;

cx q[42], q[74];
cx q[9], q[63];
cx q[20], q[56];
cx q[33], q[51];
barrier q;

cx q[42], q[4];
cx q[9], q[13];
cx q[20], q[24];
cx q[33], q[37];
barrier q;

cx q[42], q[1];
cx q[9], q[73];
cx q[20], q[62];
cx q[33], q[55];
cx q[49], q[50];
barrier q;

cx q[80], q[79];
cx q[77], q[78];
cx q[75], q[76];
cx q[66], q[67];
barrier q;

cx q[80], q[51];
cx q[77], q[56];
cx q[75], q[63];
cx q[66], q[74];
barrier q;

cx q[80], q[49];
cx q[77], q[33];
cx q[75], q[20];
cx q[66], q[9];
cx q[0], q[42];
barrier q;

