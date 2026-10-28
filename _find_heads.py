import re, glob, os
os.chdir(r"services/api")
revs = {}
for f in glob.glob('migrations/versions/*.py'):
    text = open(f, encoding='utf-8').read()
    m = re.search(r"^revision[^=]*=\s*['\"]([^'\"]+)", text, re.M)
    d = re.search(r"^down_revision[^=]*=\s*['\"]([^'\"]+)", text, re.M)
    if m:
        revs[m.group(1)] = (d.group(1) if d else None, f)
for r in sorted(revs):
    print(r, "<-", revs[r][0], revs[r][1])
