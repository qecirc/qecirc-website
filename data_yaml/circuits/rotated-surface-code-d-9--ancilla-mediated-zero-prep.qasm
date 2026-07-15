OPENQASM 2.0;
include "qelib1.inc";

qreg q[161];

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
cx q[19], q[86];
cx q[12], q[104];
cx q[23], q[122];
cx q[36], q[140];
cx q[65], q[157];
barrier q;

cx q[86], q[8];
cx q[104], q[16];
cx q[122], q[28];
cx q[140], q[40];
cx q[157], q[64];
barrier q;

cx q[86], q[7];
cx q[104], q[17];
cx q[122], q[27];
cx q[140], q[41];
barrier q;

cx q[86], q[18];
cx q[104], q[29];
cx q[122], q[43];
cx q[140], q[68];
barrier q;

cx q[19], q[86];
cx q[12], q[104];
cx q[23], q[122];
cx q[36], q[140];
cx q[65], q[157];
barrier q;

cx q[58], q[149];
cx q[69], q[131];
cx q[44], q[113];
cx q[30], q[95];
cx q[3], q[81];
barrier q;

cx q[149], q[65];
cx q[131], q[36];
cx q[113], q[23];
cx q[95], q[12];
cx q[81], q[19];
barrier q;

cx q[149], q[68];
cx q[131], q[43];
cx q[113], q[29];
cx q[95], q[18];
barrier q;

cx q[149], q[39];
cx q[131], q[26];
cx q[113], q[15];
cx q[95], q[6];
barrier q;

cx q[58], q[149];
cx q[69], q[131];
cx q[44], q[113];
cx q[30], q[95];
cx q[3], q[81];
barrier q;

cx q[32], q[88];
cx q[11], q[106];
cx q[22], q[124];
cx q[35], q[142];
cx q[57], q[158];
barrier q;

cx q[88], q[3];
cx q[106], q[30];
cx q[124], q[44];
cx q[142], q[69];
cx q[158], q[58];
barrier q;

cx q[88], q[6];
cx q[106], q[15];
cx q[124], q[26];
cx q[142], q[39];
barrier q;

cx q[88], q[31];
cx q[106], q[45];
cx q[124], q[70];
cx q[142], q[59];
barrier q;

cx q[32], q[88];
cx q[11], q[106];
cx q[22], q[124];
cx q[35], q[142];
cx q[57], q[158];
barrier q;

cx q[52], q[151];
cx q[60], q[133];
cx q[71], q[115];
cx q[46], q[97];
cx q[2], q[82];
barrier q;

cx q[151], q[57];
cx q[133], q[35];
cx q[115], q[22];
cx q[97], q[11];
cx q[82], q[32];
barrier q;

cx q[151], q[59];
cx q[133], q[70];
cx q[115], q[45];
cx q[97], q[31];
barrier q;

cx q[151], q[38];
cx q[133], q[25];
cx q[115], q[14];
cx q[97], q[5];
barrier q;

cx q[52], q[151];
cx q[60], q[133];
cx q[71], q[115];
cx q[46], q[97];
cx q[2], q[82];
barrier q;

cx q[48], q[90];
cx q[10], q[108];
cx q[21], q[126];
cx q[34], q[144];
cx q[53], q[159];
barrier q;

cx q[90], q[2];
cx q[108], q[46];
cx q[126], q[71];
cx q[144], q[60];
cx q[159], q[52];
barrier q;

cx q[90], q[5];
cx q[108], q[14];
cx q[126], q[25];
cx q[144], q[38];
barrier q;

cx q[90], q[47];
cx q[108], q[72];
cx q[126], q[61];
cx q[144], q[54];
barrier q;

cx q[48], q[90];
cx q[10], q[108];
cx q[21], q[126];
cx q[34], q[144];
cx q[53], q[159];
barrier q;

cx q[50], q[153];
cx q[55], q[135];
cx q[62], q[117];
cx q[73], q[99];
cx q[1], q[83];
barrier q;

cx q[153], q[53];
cx q[135], q[34];
cx q[117], q[21];
cx q[99], q[10];
cx q[83], q[48];
barrier q;

cx q[153], q[54];
cx q[135], q[61];
cx q[117], q[72];
cx q[99], q[47];
barrier q;

cx q[153], q[37];
cx q[135], q[24];
cx q[117], q[13];
cx q[99], q[4];
barrier q;

cx q[50], q[153];
cx q[55], q[135];
cx q[62], q[117];
cx q[73], q[99];
cx q[1], q[83];
barrier q;

cx q[42], q[92];
cx q[9], q[110];
cx q[20], q[128];
cx q[33], q[146];
cx q[49], q[160];
barrier q;

cx q[92], q[1];
cx q[110], q[73];
cx q[128], q[62];
cx q[146], q[55];
cx q[160], q[50];
barrier q;

cx q[92], q[4];
cx q[110], q[13];
cx q[128], q[24];
cx q[146], q[37];
barrier q;

cx q[92], q[74];
cx q[110], q[63];
cx q[128], q[56];
cx q[146], q[51];
barrier q;

cx q[42], q[92];
cx q[9], q[110];
cx q[20], q[128];
cx q[33], q[146];
cx q[49], q[160];
barrier q;

cx q[80], q[155];
cx q[77], q[137];
cx q[75], q[119];
cx q[66], q[101];
cx q[0], q[84];
barrier q;

cx q[155], q[49];
cx q[137], q[33];
cx q[119], q[20];
cx q[101], q[9];
cx q[84], q[42];
barrier q;

cx q[155], q[51];
cx q[137], q[56];
cx q[119], q[63];
cx q[101], q[74];
barrier q;

cx q[155], q[79];
cx q[137], q[78];
cx q[119], q[76];
cx q[101], q[67];
barrier q;

cx q[80], q[155];
cx q[77], q[137];
cx q[75], q[119];
cx q[66], q[101];
cx q[0], q[84];
barrier q;

