OPENQASM 2.0;
include "qelib1.inc";

qreg q[49];

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
barrier q;

cx q[14], q[4];
cx q[26], q[3];
cx q[44], q[38];
barrier q;

cx q[2], q[4];
cx q[27], q[3];
cx q[0], q[38];
barrier q;

cx q[5], q[6];
cx q[15], q[4];
cx q[1], q[3];
cx q[23], q[38];
barrier q;

cx q[7], q[43];
cx q[8], q[25];
cx q[9], q[13];
barrier q;

cx q[44], q[43];
cx q[26], q[25];
cx q[14], q[13];
barrier q;

cx q[38], q[39];
cx q[3], q[43];
cx q[4], q[25];
cx q[6], q[13];
barrier q;

cx q[24], q[11];
cx q[42], q[10];
cx q[35], q[45];
barrier q;

cx q[9], q[11];
cx q[8], q[10];
cx q[7], q[45];
barrier q;

cx q[13], q[12];
cx q[25], q[11];
cx q[43], q[10];
cx q[39], q[45];
barrier q;

cx q[16], q[34];
cx q[17], q[41];
cx q[18], q[22];
barrier q;

cx q[35], q[34];
cx q[42], q[41];
cx q[24], q[22];
barrier q;

cx q[45], q[46];
cx q[10], q[34];
cx q[11], q[41];
cx q[12], q[22];
barrier q;

cx q[40], q[20];
cx q[33], q[19];
cx q[30], q[48];
barrier q;

cx q[18], q[20];
cx q[17], q[19];
cx q[16], q[48];
barrier q;

cx q[22], q[21];
cx q[41], q[20];
cx q[34], q[19];
cx q[46], q[48];
barrier q;

cx q[28], q[29];
cx q[32], q[31];
cx q[37], q[36];
barrier q;

cx q[30], q[29];
cx q[33], q[31];
cx q[40], q[36];
barrier q;

cx q[48], q[47];
cx q[19], q[29];
cx q[20], q[31];
cx q[21], q[36];
barrier q;

