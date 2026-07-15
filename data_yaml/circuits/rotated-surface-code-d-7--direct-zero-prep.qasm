OPENQASM 2.0;
include "qelib1.inc";

qreg q[49];

h q[2];
h q[9];
h q[18];
h q[37];
h q[31];
h q[41];
h q[25];
h q[15];
h q[27];
h q[8];
h q[17];
h q[32];
h q[29];
h q[34];
h q[43];
h q[1];
h q[0];
h q[7];
h q[16];
h q[28];
h q[47];
h q[46];
h q[39];
h q[23];
barrier q;

cx q[2], q[14];
cx q[9], q[24];
cx q[18], q[40];
barrier q;

cx q[2], q[6];
cx q[9], q[12];
cx q[18], q[21];
barrier q;

cx q[2], q[5];
cx q[9], q[13];
cx q[18], q[22];
cx q[37], q[36];
barrier q;

cx q[31], q[20];
cx q[41], q[11];
cx q[25], q[4];
barrier q;

cx q[31], q[40];
cx q[41], q[24];
cx q[25], q[14];
barrier q;

cx q[31], q[37];
cx q[41], q[18];
cx q[25], q[9];
cx q[15], q[2];
barrier q;

cx q[27], q[26];
cx q[8], q[42];
cx q[17], q[33];
barrier q;

cx q[27], q[4];
cx q[8], q[11];
cx q[17], q[20];
barrier q;

cx q[27], q[15];
cx q[8], q[25];
cx q[17], q[41];
cx q[32], q[31];
barrier q;

cx q[29], q[19];
cx q[34], q[10];
cx q[43], q[3];
barrier q;

cx q[29], q[33];
cx q[34], q[42];
cx q[43], q[26];
barrier q;

cx q[29], q[32];
cx q[34], q[17];
cx q[43], q[8];
cx q[1], q[27];
barrier q;

cx q[0], q[44];
cx q[7], q[35];
cx q[16], q[30];
barrier q;

cx q[0], q[3];
cx q[7], q[10];
cx q[16], q[19];
barrier q;

cx q[0], q[1];
cx q[7], q[43];
cx q[16], q[34];
cx q[28], q[29];
barrier q;

cx q[47], q[48];
cx q[46], q[45];
cx q[39], q[38];
barrier q;

cx q[47], q[30];
cx q[46], q[35];
cx q[39], q[44];
barrier q;

cx q[47], q[28];
cx q[46], q[16];
cx q[39], q[7];
cx q[23], q[0];
barrier q;

