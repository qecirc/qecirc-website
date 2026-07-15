OPENQASM 2.0;
include "qelib1.inc";

qreg q[77];

h q[31];
h q[26];
h q[21];
h q[16];
h q[36];
h q[15];
h q[14];
h q[13];
h q[12];
h q[11];
h q[10];
h q[9];
h q[8];
h q[7];
h q[6];
h q[5];
h q[4];
h q[3];
h q[2];
h q[1];
h q[0];
h q[45];
h q[54];
h q[63];
h q[72];
h q[49];
h q[58];
h q[67];
h q[76];
h q[46];
h q[55];
h q[64];
h q[73];
h q[47];
h q[56];
h q[65];
h q[74];
h q[48];
h q[57];
h q[66];
h q[75];
barrier q;

cx q[45], q[32];
cx q[46], q[27];
cx q[47], q[22];
cx q[48], q[17];
cx q[49], q[37];
barrier q;

cx q[15], q[45];
cx q[14], q[46];
cx q[13], q[47];
cx q[12], q[48];
barrier q;

cx q[31], q[45];
cx q[26], q[46];
cx q[21], q[47];
cx q[16], q[48];
cx q[36], q[49];
barrier q;

cx q[15], q[46];
cx q[14], q[47];
cx q[13], q[48];
cx q[12], q[49];
barrier q;

cx q[45], q[32];
cx q[46], q[27];
cx q[47], q[22];
cx q[48], q[17];
cx q[49], q[37];
barrier q;

cx q[54], q[33];
cx q[55], q[28];
cx q[56], q[23];
cx q[57], q[18];
cx q[58], q[38];
barrier q;

cx q[11], q[54];
cx q[10], q[55];
cx q[9], q[56];
cx q[8], q[57];
barrier q;

cx q[32], q[54];
cx q[27], q[55];
cx q[22], q[56];
cx q[17], q[57];
cx q[37], q[58];
barrier q;

cx q[11], q[55];
cx q[10], q[56];
cx q[9], q[57];
cx q[8], q[58];
barrier q;

cx q[54], q[33];
cx q[55], q[28];
cx q[56], q[23];
cx q[57], q[18];
cx q[58], q[38];
barrier q;

cx q[63], q[34];
cx q[64], q[29];
cx q[65], q[24];
cx q[66], q[19];
cx q[67], q[39];
barrier q;

cx q[7], q[63];
cx q[6], q[64];
cx q[5], q[65];
cx q[4], q[66];
barrier q;

cx q[33], q[63];
cx q[28], q[64];
cx q[23], q[65];
cx q[18], q[66];
cx q[38], q[67];
barrier q;

cx q[7], q[64];
cx q[6], q[65];
cx q[5], q[66];
cx q[4], q[67];
barrier q;

cx q[63], q[34];
cx q[64], q[29];
cx q[65], q[24];
cx q[66], q[19];
cx q[67], q[39];
barrier q;

cx q[72], q[35];
cx q[73], q[30];
cx q[74], q[25];
cx q[75], q[20];
cx q[76], q[40];
barrier q;

cx q[3], q[72];
cx q[2], q[73];
cx q[1], q[74];
cx q[0], q[75];
barrier q;

cx q[34], q[72];
cx q[29], q[73];
cx q[24], q[74];
cx q[19], q[75];
cx q[39], q[76];
barrier q;

cx q[3], q[73];
cx q[2], q[74];
cx q[1], q[75];
cx q[0], q[76];
barrier q;

cx q[72], q[35];
cx q[73], q[30];
cx q[74], q[25];
cx q[75], q[20];
cx q[76], q[40];
barrier q;

