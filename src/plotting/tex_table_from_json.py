import argparse
import json
import os


if __name__ == '__main__':
    """Reads a collection of json stats files and produces latex"""
    parser = argparse.ArgumentParser(description='Plot survival of models.')
    parser.add_argument('config_dirs', type=str, nargs='+',
                        help='path to exp_out config')
    args = parser.parse_args()

    config_dirs = args.config_dirs

    name_to_stats = {}
    for config_dir in config_dirs:
        name = config_dir.split('/')[2]
        stats_f = os.path.join(config_dir, 'results', 'stats.json')
        with open(stats_f, 'r') as f:
            name_to_stats[name] = json.load(f)

    stats_to_plot = ['time', 'q1med', 'q5med', 'std_pap_score']
    print('Method & Time (s) & Q1 Med. & Q5 Med. & Pap Score std\\\\')
    print('\\hline')
    for name, stats in name_to_stats.items():
        print('%s & %.2f & %.2f & %.2f & %.2f\\\\' % (
            name, stats[stats_to_plot[0]], stats[stats_to_plot[1]],
            stats[stats_to_plot[2]], stats[stats_to_plot[3]]))
