OPENQASM 2.0;
include "qelib1.inc";

qreg q[81];

h q[26];
h q[27];
h q[28];
h q[29];
h q[30];
h q[21];
h q[22];
h q[23];
h q[24];
h q[25];
h q[16];
h q[17];
h q[18];
h q[19];
h q[20];
h q[36];
h q[37];
h q[38];
h q[39];
h q[40];
barrier q;

cx q[26], q[41];
cx q[27], q[50];
cx q[28], q[59];
cx q[29], q[68];
cx q[30], q[77];
barrier q;

cx q[41], q[15];
cx q[50], q[11];
cx q[59], q[7];
cx q[68], q[3];
barrier q;

cx q[41], q[31];
cx q[50], q[32];
cx q[59], q[33];
cx q[68], q[34];
cx q[77], q[35];
barrier q;

cx q[50], q[15];
cx q[59], q[11];
cx q[68], q[7];
cx q[77], q[3];
barrier q;

cx q[26], q[41];
cx q[27], q[50];
cx q[28], q[59];
cx q[29], q[68];
cx q[30], q[77];
barrier q;

cx q[21], q[42];
cx q[22], q[51];
cx q[23], q[60];
cx q[24], q[69];
cx q[25], q[78];
barrier q;

cx q[42], q[14];
cx q[51], q[10];
cx q[60], q[6];
cx q[69], q[2];
barrier q;

cx q[42], q[26];
cx q[51], q[27];
cx q[60], q[28];
cx q[69], q[29];
cx q[78], q[30];
barrier q;

cx q[51], q[14];
cx q[60], q[10];
cx q[69], q[6];
cx q[78], q[2];
barrier q;

cx q[21], q[42];
cx q[22], q[51];
cx q[23], q[60];
cx q[24], q[69];
cx q[25], q[78];
barrier q;

cx q[16], q[43];
cx q[17], q[52];
cx q[18], q[61];
cx q[19], q[70];
cx q[20], q[79];
barrier q;

cx q[43], q[13];
cx q[52], q[9];
cx q[61], q[5];
cx q[70], q[1];
barrier q;

cx q[43], q[21];
cx q[52], q[22];
cx q[61], q[23];
cx q[70], q[24];
cx q[79], q[25];
barrier q;

cx q[52], q[13];
cx q[61], q[9];
cx q[70], q[5];
cx q[79], q[1];
barrier q;

cx q[16], q[43];
cx q[17], q[52];
cx q[18], q[61];
cx q[19], q[70];
cx q[20], q[79];
barrier q;

cx q[36], q[44];
cx q[37], q[53];
cx q[38], q[62];
cx q[39], q[71];
cx q[40], q[80];
barrier q;

cx q[44], q[12];
cx q[53], q[8];
cx q[62], q[4];
cx q[71], q[0];
barrier q;

cx q[44], q[16];
cx q[53], q[17];
cx q[62], q[18];
cx q[71], q[19];
cx q[80], q[20];
barrier q;

cx q[53], q[12];
cx q[62], q[8];
cx q[71], q[4];
cx q[80], q[0];
barrier q;

cx q[36], q[44];
cx q[37], q[53];
cx q[38], q[62];
cx q[39], q[71];
cx q[40], q[80];
barrier q;

