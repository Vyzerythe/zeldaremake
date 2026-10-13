#!/usr/bin/env python3
"""Usage: python3 -I branch_unique.py <branch-ref> [<against-ref>=origin/cursor/kokiri-world-phase1-f65e] [--all]
For every file the branch changed since its merge-base with <against>, report whether the branch's
version of that file is:
  IN_HEAD        identical to <against>'s current version (already integrated / nothing to take)
  SUPERSEDED     appeared somewhere in <against>'s history but <against> has since changed it
  UNIQUE         never appeared in <against>'s history (genuinely new content on the branch)
  DELETED_ON_BR  branch deleted the file
Paths under art/, .agents/reviews/, gauntlet/reviews/ are summarised as counts unless --all.
"""
import subprocess, sys, collections
REPO=subprocess.run(['git','rev-parse','--show-toplevel'],capture_output=True,text=True,check=True).stdout.strip()
def git(*a): return subprocess.run(['git','-C',REPO,*a],capture_output=True,text=True,check=True).stdout
args=[a for a in sys.argv[1:] if not a.startswith('--')]
showall='--all' in sys.argv
br=args[0]; ag=args[1] if len(args)>1 else 'origin/cursor/kokiri-world-phase1-f65e'
mb=git('merge-base',br,ag).strip()
changed=[l.split('\t') for l in git('diff','--name-status','--no-renames',mb,br).splitlines()]
# blob history of <against>
hist=collections.defaultdict(set)
for l in git('log','--raw','--no-abbrev','--no-renames','--diff-merges=separate','--format=',ag).splitlines():
    if l.startswith(':'):
        meta,p=l.split('\t',1); hist[p].add(meta.split()[3])
def blob(ref,p):
    try: return git('rev-parse',f'{ref}:{p}').strip()
    except subprocess.CalledProcessError: return None
res=collections.defaultdict(list)
for st,p in changed:
    if st=='D': res['DELETED_ON_BR'].append(p); continue
    b=blob(br,p); h=blob(ag,p)
    if b==h: res['IN_HEAD'].append(p)
    elif b in hist.get(p,()): res['SUPERSEDED'].append(p)
    else: res['UNIQUE'].append(p)
print(f'branch={br} against={ag} merge-base={mb[:10]} files-changed={len(changed)}')
noisy=lambda p: p.startswith(('art/','.agents/reviews/','gauntlet/reviews/'))
for k in ['UNIQUE','SUPERSEDED','IN_HEAD','DELETED_ON_BR']:
    v=res.get(k,[])
    if not v: continue
    code=[p for p in v if not noisy(p)]; ev=[p for p in v if noisy(p)]
    print(f'{k}: {len(v)}  (code/docs {len(code)}, evidence {len(ev)})')
    for p in (v if showall else code): print('   ',p)
    if ev and not showall:
        c=collections.Counter('/'.join(p.split('/')[:3]) for p in ev)
        for d,n in c.most_common(8): print(f'    [{n} files] {d}/...')
