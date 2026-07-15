OPENQASM 2.0;
include "qelib1.inc";

qreg q[97];

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
cx q[2], q[53];
cx q[9], q[67];
cx q[18], q[81];
cx q[37], q[94];
barrier q;

cx q[53], q[5];
cx q[67], q[13];
cx q[81], q[22];
cx q[94], q[36];
barrier q;

cx q[53], q[6];
cx q[67], q[12];
cx q[81], q[21];
barrier q;

cx q[53], q[14];
cx q[67], q[24];
cx q[81], q[40];
barrier q;

cx q[2], q[53];
cx q[9], q[67];
cx q[18], q[81];
cx q[37], q[94];
barrier q;

cx q[31], q[88];
cx q[41], q[74];
cx q[25], q[60];
cx q[15], q[49];
barrier q;

cx q[88], q[37];
cx q[74], q[18];
cx q[60], q[9];
cx q[49], q[2];
barrier q;

cx q[88], q[40];
cx q[74], q[24];
cx q[60], q[14];
barrier q;

cx q[88], q[20];
cx q[74], q[11];
cx q[60], q[4];
barrier q;

cx q[31], q[88];
cx q[41], q[74];
cx q[25], q[60];
cx q[15], q[49];
barrier q;

cx q[27], q[55];
cx q[8], q[69];
cx q[17], q[83];
cx q[32], q[95];
barrier q;

cx q[55], q[15];
cx q[69], q[25];
cx q[83], q[41];
cx q[95], q[31];
barrier q;

cx q[55], q[4];
cx q[69], q[11];
cx q[83], q[20];
barrier q;

cx q[55], q[26];
cx q[69], q[42];
cx q[83], q[33];
barrier q;

cx q[27], q[55];
cx q[8], q[69];
cx q[17], q[83];
cx q[32], q[95];
barrier q;

cx q[29], q[90];
cx q[34], q[76];
cx q[43], q[62];
cx q[1], q[50];
barrier q;

cx q[90], q[32];
cx q[76], q[17];
cx q[62], q[8];
cx q[50], q[27];
barrier q;

cx q[90], q[33];
cx q[76], q[42];
cx q[62], q[26];
barrier q;

cx q[90], q[19];
cx q[76], q[10];
cx q[62], q[3];
barrier q;

cx q[29], q[90];
cx q[34], q[76];
cx q[43], q[62];
cx q[1], q[50];
barrier q;

cx q[0], q[57];
cx q[7], q[71];
cx q[16], q[85];
cx q[28], q[96];
barrier q;

cx q[57], q[1];
cx q[71], q[43];
cx q[85], q[34];
cx q[96], q[29];
barrier q;

cx q[57], q[3];
cx q[71], q[10];
cx q[85], q[19];
barrier q;

cx q[57], q[44];
cx q[71], q[35];
cx q[85], q[30];
barrier q;

cx q[0], q[57];
cx q[7], q[71];
cx q[16], q[85];
cx q[28], q[96];
barrier q;

cx q[47], q[92];
cx q[46], q[78];
cx q[39], q[64];
cx q[23], q[51];
barrier q;

cx q[92], q[28];
cx q[78], q[16];
cx q[64], q[7];
cx q[51], q[0];
barrier q;

cx q[92], q[30];
cx q[78], q[35];
cx q[64], q[44];
barrier q;

cx q[92], q[48];
cx q[78], q[45];
cx q[64], q[38];
barrier q;

cx q[47], q[92];
cx q[46], q[78];
cx q[39], q[64];
cx q[23], q[51];
barrier q;

