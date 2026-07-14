OPENQASM 2.0;
include "qelib1.inc";

qreg q[121];

h q[100];
h q[90];
h q[89];
h q[82];
h q[81];
h q[76];
h q[75];
h q[72];
h q[71];
h q[70];
h q[120];
h q[69];
h q[68];
h q[67];
h q[66];
h q[65];
h q[103];
h q[92];
h q[84];
h q[78];
h q[74];
h q[51];
h q[50];
h q[49];
h q[48];
h q[47];
h q[58];
h q[105];
h q[94];
h q[86];
h q[80];
h q[35];
h q[34];
h q[33];
h q[32];
h q[31];
h q[42];
h q[60];
h q[107];
h q[96];
h q[88];
h q[21];
h q[20];
h q[19];
h q[18];
h q[17];
h q[28];
h q[44];
h q[62];
h q[109];
h q[98];
h q[9];
h q[8];
h q[7];
h q[6];
h q[5];
h q[16];
h q[30];
h q[46];
h q[64];
h q[111];
barrier q;

cx q[69], q[91];
cx q[68], q[83];
cx q[67], q[77];
cx q[66], q[73];
cx q[65], q[118];
barrier q;

cx q[90], q[91];
cx q[82], q[83];
cx q[76], q[77];
cx q[72], q[73];
cx q[70], q[118];
barrier q;

cx q[100], q[99];
cx q[89], q[91];
cx q[81], q[83];
cx q[75], q[77];
cx q[71], q[73];
cx q[120], q[118];
barrier q;

cx q[74], q[52];
cx q[78], q[53];
cx q[84], q[54];
cx q[92], q[55];
cx q[103], q[57];
barrier q;

cx q[65], q[52];
cx q[66], q[53];
cx q[67], q[54];
cx q[68], q[55];
cx q[69], q[57];
barrier q;

cx q[118], q[119];
cx q[73], q[52];
cx q[77], q[53];
cx q[83], q[54];
cx q[91], q[55];
cx q[99], q[57];
barrier q;

cx q[51], q[104];
cx q[50], q[93];
cx q[49], q[85];
cx q[48], q[79];
cx q[47], q[116];
barrier q;

cx q[103], q[104];
cx q[92], q[93];
cx q[84], q[85];
cx q[78], q[79];
cx q[74], q[116];
barrier q;

cx q[57], q[56];
cx q[55], q[104];
cx q[54], q[93];
cx q[53], q[85];
cx q[52], q[79];
cx q[119], q[116];
barrier q;

cx q[80], q[36];
cx q[86], q[37];
cx q[94], q[38];
cx q[105], q[39];
cx q[58], q[41];
barrier q;

cx q[47], q[36];
cx q[48], q[37];
cx q[49], q[38];
cx q[50], q[39];
cx q[51], q[41];
barrier q;

cx q[116], q[117];
cx q[79], q[36];
cx q[85], q[37];
cx q[93], q[38];
cx q[104], q[39];
cx q[56], q[41];
barrier q;

cx q[35], q[59];
cx q[34], q[106];
cx q[33], q[95];
cx q[32], q[87];
cx q[31], q[114];
barrier q;

cx q[58], q[59];
cx q[105], q[106];
cx q[94], q[95];
cx q[86], q[87];
cx q[80], q[114];
barrier q;

cx q[41], q[40];
cx q[39], q[59];
cx q[38], q[106];
cx q[37], q[95];
cx q[36], q[87];
cx q[117], q[114];
barrier q;

cx q[88], q[22];
cx q[96], q[23];
cx q[107], q[24];
cx q[60], q[25];
cx q[42], q[27];
barrier q;

cx q[31], q[22];
cx q[32], q[23];
cx q[33], q[24];
cx q[34], q[25];
cx q[35], q[27];
barrier q;

cx q[114], q[115];
cx q[87], q[22];
cx q[95], q[23];
cx q[106], q[24];
cx q[59], q[25];
cx q[40], q[27];
barrier q;

cx q[21], q[43];
cx q[20], q[61];
cx q[19], q[108];
cx q[18], q[97];
cx q[17], q[112];
barrier q;

cx q[42], q[43];
cx q[60], q[61];
cx q[107], q[108];
cx q[96], q[97];
cx q[88], q[112];
barrier q;

cx q[27], q[26];
cx q[25], q[43];
cx q[24], q[61];
cx q[23], q[108];
cx q[22], q[97];
cx q[115], q[112];
barrier q;

cx q[98], q[10];
cx q[109], q[11];
cx q[62], q[12];
cx q[44], q[13];
cx q[28], q[15];
barrier q;

cx q[17], q[10];
cx q[18], q[11];
cx q[19], q[12];
cx q[20], q[13];
cx q[21], q[15];
barrier q;

cx q[112], q[113];
cx q[97], q[10];
cx q[108], q[11];
cx q[61], q[12];
cx q[43], q[13];
cx q[26], q[15];
barrier q;

cx q[9], q[29];
cx q[8], q[45];
cx q[7], q[63];
cx q[6], q[110];
cx q[5], q[101];
barrier q;

cx q[28], q[29];
cx q[44], q[45];
cx q[62], q[63];
cx q[109], q[110];
cx q[98], q[101];
barrier q;

cx q[15], q[14];
cx q[13], q[29];
cx q[12], q[45];
cx q[11], q[63];
cx q[10], q[110];
cx q[113], q[101];
barrier q;

cx q[111], q[0];
cx q[64], q[1];
cx q[46], q[2];
cx q[30], q[3];
cx q[16], q[4];
barrier q;

cx q[5], q[0];
cx q[6], q[1];
cx q[7], q[2];
cx q[8], q[3];
cx q[9], q[4];
barrier q;

cx q[101], q[102];
cx q[110], q[0];
cx q[63], q[1];
cx q[45], q[2];
cx q[29], q[3];
cx q[14], q[4];
barrier q;

