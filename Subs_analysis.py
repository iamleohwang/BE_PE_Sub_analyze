import os, argparse
import matplotlib.pyplot as plt
import numpy as np 
import seaborn as sns

def main():
    # ref result

    wt_rm_dict = {}
    wt_dict = {}
    for i in list(range(1, 23)) + ['MT', 'X', 'Y']:
        wt_rm_dict[str(i)] = []
        wt_dict[str(i)] = {}

    c = 0
    cc = 0
    
    with open(ref_fn) as f:
        next(f)
        for line in f:
            line_sp = line.split()
            if float(line_sp[2]) > 10:
                p = line_sp[1]
                p_4 = line_sp[1][:4]
                p_after = line_sp[1][4:]
                if p_4 not in wt_dict[line_sp[0]]:
                    wt_dict[line_sp[0]][p_4] = [p_after]
                else:
                    wt_dict[line_sp[0]][p_4].append(p_after)
                cc += 1
                if float(line_sp[4]) > 1:
                    wt_rm_dict[line_sp[0]].append(line_sp[1])
                    c += 1

    print(c)
    print(cc)
    
    # mut result analysis

    data = []

    for fn in mut_fn_list:
        print(fn)
        data.append([])
        c= 0
        with open(fn) as f:
            next(f)
            for line in f:
                line_sp = line.split()
                if 10 < float(line_sp[2]) and 1 < float(line_sp[4]) and line_sp[1] not in wt_rm_dict[line_sp[0]]:
                    c += 1
                    p = line_sp[1]
                    p_4 = p[:4]
                    p_after = p[4:]
                    if p_4 not in wt_dict[line_sp[0]]:
                        continue
                    if p_after not in wt_dict[line_sp[0]][p_4]:
                        continue
                    data[-1].append(float(line_sp[4]))
        print(c)
        
    plt.figure(figsize=(3,5))
    
    sns.stripplot(data=data, jitter=0.5, dodge=False, size=2.5, edgecolor='none', linewidth=0.7, alpha=0.5)
    plt.subplots_adjust(left=0.2)
    plt.ylim(0,100)

    plt.savefig(output_fn + '.pdf')

    plt.figure(figsize=(3,5))

    plt.boxplot(data, positions=[1,2], widths = 0.5)
    jitter_strength = 0.1
    for i, group_data in enumerate(data, start=1):
        jittered_x = np.random.normal(i, jitter_strength, size=len(group_data))
        plt.scatter(jittered_x, group_data, alpha=0.1, edgecolor='k', label=f'Group {i} Data', s=5, c='gray')

    plt.savefig(output_fn + '_box_jitter.pdf')

    return 0;


if __name__ == '__main__':
    ref_fn = 'result_C_to_T_EP.txt'
    mut_fn_list = ['result_C_to_T_BE4.txt', 'result_C_to_T_BESTEM.txt']
    output_fn = 'BE'

    parser = argparse.ArgumentParser(description='Calculate substitution from REDitools2 result files')
    parser.add_argument('Control_file', type=str, help='Reditools control file')
    parser.add_argument('Treated_file1', type=str, help='Reditools treated file 1')
    parser.add_argument('Treated_file2', type=str, help='Reditools treated file 2')
    parser.add_argument('output_file_name', type=str, help='output file name')

    args = parser.parse_args()

    ref_fn = args.Control_file
    mut_fn_list = [args.Treated_file1, args.Treated_file2]
    output_fn = args.output_file_name

    main()
