#!/usr/bin/env python3
"""Plot measured times from one complete, uniformly versioned campaign."""
import argparse
import json
from pathlib import Path


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('run', type=Path)
    args = ap.parse_args()
    manifest = json.loads((args.run/'campaign.json').read_text())
    background = manifest.get('crystalline_spin') == 'spinless'
    data = []
    for sg in range(1, 231):
        d = json.loads((args.run/('sg%d.json'%sg)).read_text())
        if d['space_group'] != sg or d['status'] != 'computed' or d['source_id'] != manifest['source_id']:
            ap.error('campaign is incomplete or contains different source versions')
        data.append(d)
    observation = json.loads((args.run/'observation.json').read_text())
    if not observation['observed_complete']:
        ap.error('campaign completion was not observed')
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    wall = [d['wall_seconds']/60 for d in data]
    classification = [d['cpu_ms']/60000 for d in data]
    stacking = [max(0, d['total_cpu_ms']-d['cpu_ms'])/60000 for d in data]
    sg = list(range(1, 231))
    fig, axes = plt.subplots(2, 1, figsize=(10, 7), constrained_layout=True)
    if background:
        # Background checkpoints follow the integrated stacking routine. A
        # split at cpu_ms would mislabel nearly all work as classification.
        from audit_background_run import audit
        report, failed = audit(args.run)
        if failed or not report['all_230_full_groups_determined']:
            ap.error('background results do not pass the full abstract-group audit')
        plotted = [d['total_cpu_ms']/60000 for d in data]
        axes[0].scatter(sg, plotted, s=15,
                        label='Full classification + stacking CPU minutes', color='#2166ac')
        axes[0].margins(y=.12)
    else:
        plotted = [max(c, s) for c, s in zip(classification, stacking)]
        axes[0].scatter(sg, classification, s=15, label='Classification CPU minutes', color='#2166ac')
        axes[0].scatter(sg, stacking, s=15, marker='x', label='Additional stacking CPU minutes', color='#b35806')
    axes[0].set(xlabel='Space-group number', ylabel='Minutes (log scale)', yscale='log', xlim=(0, 231))
    axes[0].grid(alpha=.2)
    axes[0].legend(frameon=False)
    for d in sorted(data, key=lambda x:x['wall_seconds'], reverse=True)[:5]:
        i = d['space_group']-1
        y = plotted[i]
        right_edge = i+1 > 220
        axes[0].annotate(str(i+1), (i+1, y), xytext=(-3 if right_edge else 3, 5),
                         ha='right' if right_edge else 'left',
                         textcoords='offset points', fontsize=8)
    events = observation['history']
    times = [e['elapsed_seconds']/60 for e in events]
    if not background:
        axes[1].step(times, [e['classification_checkpoints'] for e in events], where='post',
                     label='Classification checkpoints', color='#2166ac')
    axes[1].step(times, [e['full_results'] for e in events], where='post',
                 label=('Complete classification + abstract stacking group' if background
                        else 'Complete classification + stacking'), color='#b35806')
    axes[1].set(xlabel='Observed campaign elapsed minutes (including queue delays)',
                ylabel='Space groups completed', ylim=(0, 235))
    axes[1].grid(alpha=.2)
    axes[1].legend(frameon=False)
    elapsed = observation['observed_campaign_seconds']/60
    convention = 'crystalline spinless' if background else 'crystalline spin-half'
    fig.suptitle(('FSPT_AHSS: '+convention+', all 230 groups, one frozen runtime\n')+
                 'Observed elapsed %.1f min; GAP CPU %.2f h; slowest group %.1f min' %
                 (elapsed, sum(d['total_cpu_ms'] for d in data)/3600000, max(wall)))
    fig.savefig(args.run/'performance.pdf')
    fig.savefig(args.run/'performance.png', dpi=180)
    print(args.run/'performance.pdf')


if __name__ == '__main__':
    main()
