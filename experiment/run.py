"""Build two small C# programs with each supplied compiler and check the full byte domain. SPDX-License-Identifier: MIT"""
import argparse
import csv
import hashlib
import io
import json
import os
from pathlib import Path
import platform
import re
import subprocess
import sys
import tempfile


def require(condition, message):
    if not condition:
        raise ValueError(message)


def version(exe):
    for flag in ('-version', '/help'):
        probe = subprocess.run([str(exe), flag], capture_output=True, timeout=25)
        output = (probe.stdout + probe.stderr).decode('utf-8', 'replace')
        for line in output.splitlines():
            hit = re.search(r'(?:Compiler version\s+|^\s*)(\d+\.\d+(?:\.\d+){0,3}(?:[-+][A-Za-z0-9.]+)?)', line, re.I)
            if hit:
                return hit.group(1)
    raise ValueError('Unable to identify the compiler version from public version/help output.')


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def run(args):
    if os.name != 'nt':
        raise ValueError('This reproduction targets Windows .NET Framework. Do not substitute another host silently.')
    compilers = [('framework', Path(args.framework_csc).resolve(strict=True)),
                 ('roslyn', Path(args.roslyn_csc).resolve(strict=True))]
    ref = Path(args.mscorlib).resolve(strict=True)
    src = Path(__file__).with_name('Field.cs').resolve(strict=True)
    require(ref.name.lower() == 'mscorlib.dll', 'Expected a single explicit .NET Framework core assembly.')
    require(digest(compilers[0][1]) != digest(compilers[1][1]), 'Two distinct compiler driver binaries are required.')
    out = Path(args.out)
    require(not out.exists(), 'Choose a new output directory.')
    rows, descriptions, observations = [], {}, {}
    with tempfile.TemporaryDirectory() as tmp:
        tmp = Path(tmp)
        for label, exe in compilers:
            descriptions[label] = {'compiler_version': version(exe), 'driver_sha256': digest(exe)}
            for optimization in ('off','on'):
                for variant in ('unsigned','signed-control'):
                    flags = ['/nologo', '/noconfig', '/nostdlib+', '/target:exe','/platform:anycpu',
                             '/optimize' + ('+' if optimization == 'on' else '-'), '/reference:' + str(ref)]
                    if variant == 'signed-control':
                        flags.append('/define:SIGNED_CONTROL')
                    bin_file = tmp / ('field-' + label + '-' + optimization + '-' + variant + '.exe')
                    subprocess.run([str(exe), *flags, '/out:' + str(bin_file), str(src)], check=True, stdout=subprocess.PIPE, timeout=40)
                    raw = subprocess.run([str(bin_file)], check=True, capture_output=True, timeout=25).stdout.decode('ascii').splitlines()
                    require(len(raw)==256 and all(re.fullmatch(r'-?\d+',x) for x in raw), 'Executable did not return 256 integers.')
                    actual = list(map(int, raw)); failures = [i for i,n in enumerate(actual) if n != i // 16]
                    # This SECOND check tests the entire control, independently of its C# shift expression.
                    predicted = [((i - 256) if variant == 'signed-control' and i >= 128 else i) // 16 for i in range(256)]
                    require(actual == predicted, 'Unexpected return value: inspect this compiler and variant.')
                    require(failures == ([] if variant=='unsigned' else list(range(128,256))), 'Unexpected mismatch pattern.')
                    observations[(label, optimization, variant)] = actual
                    rows.append({'compiler': label, 'optimization': optimization, 'variant': variant, 'inputs': len(actual),
                                 'oracle_mismatches': len(failures), 'first_mismatch': failures[0] if failures else None,
                                 'last_mismatch': failures[-1] if failures else None})
    for variant in ('unsigned','signed-control'):
        all_targets=[v for (_, _, k),v in observations.items() if k == variant]
        require(all(v == all_targets[0] for v in all_targets), 'Build outputs differed within a variant.')
    out.mkdir(parents=True, exist_ok=False)
    buf=io.StringIO(newline=''); w=csv.writer(buf,lineterminator='\n')
    w.writerow(['input_byte','specified_upper_field'] + ['_'.join(key) for key in observations])
    for index in range(256): w.writerow([index, index // 16]+[v[index] for v in observations.values()])
    (out/'observations.csv').write_bytes(buf.getvalue().encode('ascii'))
    result={'schema':'compiler-field-survey/v1','host':'Windows '+platform.version(),'machine':platform.machine(),'python':platform.python_version(),
            'shared_target':'AnyCPU .NET Framework executable; one Windows host and the same mscorlib.dll',
            'source_sha256':digest(src),'mscorlib_sha256':digest(ref),'compilers':descriptions,'rows':rows,
            'within_variant_outputs_identical':True,'observations_sha256':digest(out/'observations.csv')}
    (out/'results.json').write_bytes((json.dumps(result,indent=2)+'\n').encode('utf8'))
    print('Checked eight builds, 256 inputs per build. All unsigned outputs match; each signed control differs on 128 inputs.')


if __name__=='__main__':
    ap=argparse.ArgumentParser(description=__doc__)
    for arg in ['framework-csc','roslyn-csc','mscorlib','out']: ap.add_argument('--'+arg,required=True)
    try: run(ap.parse_args())
    except (ValueError,OSError,subprocess.SubprocessError) as e: print('Run failed:',e,file=sys.stderr); sys.exit(1)
