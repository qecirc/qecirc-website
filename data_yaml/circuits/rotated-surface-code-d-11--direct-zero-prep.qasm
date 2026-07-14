OPENQASM 2.0;
include "qelib1.inc";

qreg q[121];

h q[90];
h q[103];
h q[58];
h q[42];
h q[28];
h q[16];
h q[3];
h q[13];
h q[25];
h q[39];
h q[55];
h q[89];
h q[82];
h q[92];
h q[105];
h q[60];
h q[44];
h q[30];
h q[2];
h q[12];
h q[24];
h q[38];
h q[54];
h q[81];
h q[76];
h q[84];
h q[94];
h q[107];
h q[62];
h q[46];
h q[1];
h q[11];
h q[23];
h q[37];
h q[53];
h q[75];
h q[72];
h q[78];
h q[86];
h q[96];
h q[109];
h q[64];
h q[0];
h q[10];
h q[22];
h q[36];
h q[52];
h q[71];
h q[70];
h q[74];
h q[80];
h q[88];
h q[98];
h q[111];
h q[102];
h q[113];
h q[115];
h q[117];
h q[119];
h q[120];
barrier q;

cx q[90], q[69];
cx q[103], q[51];
cx q[58], q[35];
cx q[42], q[21];
cx q[28], q[9];
barrier q;

cx q[90], q[99];
cx q[103], q[56];
cx q[58], q[40];
cx q[42], q[26];
cx q[28], q[14];
barrier q;

cx q[90], q[100];
cx q[103], q[57];
cx q[58], q[41];
cx q[42], q[27];
cx q[28], q[15];
cx q[16], q[4];
barrier q;

cx q[3], q[29];
cx q[13], q[43];
cx q[25], q[59];
cx q[39], q[104];
cx q[55], q[91];
barrier q;

cx q[3], q[9];
cx q[13], q[21];
cx q[25], q[35];
cx q[39], q[51];
cx q[55], q[69];
barrier q;

cx q[3], q[16];
cx q[13], q[28];
cx q[25], q[42];
cx q[39], q[58];
cx q[55], q[103];
cx q[89], q[90];
barrier q;

cx q[82], q[68];
cx q[92], q[50];
cx q[105], q[34];
cx q[60], q[20];
cx q[44], q[8];
barrier q;

cx q[82], q[91];
cx q[92], q[104];
cx q[105], q[59];
cx q[60], q[43];
cx q[44], q[29];
barrier q;

cx q[82], q[89];
cx q[92], q[55];
cx q[105], q[39];
cx q[60], q[25];
cx q[44], q[13];
cx q[30], q[3];
barrier q;

cx q[2], q[45];
cx q[12], q[61];
cx q[24], q[106];
cx q[38], q[93];
cx q[54], q[83];
barrier q;

cx q[2], q[8];
cx q[12], q[20];
cx q[24], q[34];
cx q[38], q[50];
cx q[54], q[68];
barrier q;

cx q[2], q[30];
cx q[12], q[44];
cx q[24], q[60];
cx q[38], q[105];
cx q[54], q[92];
cx q[81], q[82];
barrier q;

cx q[76], q[67];
cx q[84], q[49];
cx q[94], q[33];
cx q[107], q[19];
cx q[62], q[7];
barrier q;

cx q[76], q[83];
cx q[84], q[93];
cx q[94], q[106];
cx q[107], q[61];
cx q[62], q[45];
barrier q;

cx q[76], q[81];
cx q[84], q[54];
cx q[94], q[38];
cx q[107], q[24];
cx q[62], q[12];
cx q[46], q[2];
barrier q;

cx q[1], q[63];
cx q[11], q[108];
cx q[23], q[95];
cx q[37], q[85];
cx q[53], q[77];
barrier q;

cx q[1], q[7];
cx q[11], q[19];
cx q[23], q[33];
cx q[37], q[49];
cx q[53], q[67];
barrier q;

cx q[1], q[46];
cx q[11], q[62];
cx q[23], q[107];
cx q[37], q[94];
cx q[53], q[84];
cx q[75], q[76];
barrier q;

cx q[72], q[66];
cx q[78], q[48];
cx q[86], q[32];
cx q[96], q[18];
cx q[109], q[6];
barrier q;

cx q[72], q[77];
cx q[78], q[85];
cx q[86], q[95];
cx q[96], q[108];
cx q[109], q[63];
barrier q;

cx q[72], q[75];
cx q[78], q[53];
cx q[86], q[37];
cx q[96], q[23];
cx q[109], q[11];
cx q[64], q[1];
barrier q;

cx q[0], q[110];
cx q[10], q[97];
cx q[22], q[87];
cx q[36], q[79];
cx q[52], q[73];
barrier q;

cx q[0], q[6];
cx q[10], q[18];
cx q[22], q[32];
cx q[36], q[48];
cx q[52], q[66];
barrier q;

cx q[0], q[64];
cx q[10], q[109];
cx q[22], q[96];
cx q[36], q[86];
cx q[52], q[78];
cx q[71], q[72];
barrier q;

cx q[70], q[65];
cx q[74], q[47];
cx q[80], q[31];
cx q[88], q[17];
cx q[98], q[5];
barrier q;

cx q[70], q[73];
cx q[74], q[79];
cx q[80], q[87];
cx q[88], q[97];
cx q[98], q[110];
barrier q;

cx q[70], q[71];
cx q[74], q[52];
cx q[80], q[36];
cx q[88], q[22];
cx q[98], q[10];
cx q[111], q[0];
barrier q;

cx q[102], q[101];
cx q[113], q[112];
cx q[115], q[114];
cx q[117], q[116];
cx q[119], q[118];
barrier q;

cx q[102], q[5];
cx q[113], q[17];
cx q[115], q[31];
cx q[117], q[47];
cx q[119], q[65];
barrier q;

cx q[102], q[111];
cx q[113], q[98];
cx q[115], q[88];
cx q[117], q[80];
cx q[119], q[74];
cx q[120], q[70];
barrier q;

