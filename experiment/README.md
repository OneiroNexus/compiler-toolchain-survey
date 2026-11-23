# Reproduce the finite byte-field experiment

The test uses two installed C# compilers on one Windows .NET Framework host. Python 3 (standard library only) runs each compiler with the same explicit mscorlib reference, AnyCPU target, optimization on/off, and both source variants. Compilers and runtime libraries are not distributed in this repository.

From the repository root in PowerShell, use a new output directory and adjust the two paths if the installations differ:

```powershell
$fx = Join-Path $env:WINDIR 'Microsoft.NET/Framework64/v4.0.30319'
$roslyn = Join-Path ${env:ProgramFiles(x86)} 'Microsoft Visual Studio/2022/BuildTools/MSBuild/Current/Bin/Roslyn/csc.exe'
python -B experiment/run.py --framework-csc (Join-Path $fx 'csc.exe') --roslyn-csc $roslyn --mscorlib (Join-Path $fx 'mscorlib.dll') --out 'my-byte-field-results'
```

The program takes no outside data. Each binary writes 256 decimal integers. The checker compares every value with an independent unsigned field definition (integer division by 16) and verifies the signed control against its predicted range and values. An unexpected result, missing tool or pre-existing output directory stops the run. Executables are temporary. Compare the resulting `observations.csv` with [the archived observations](recorded/observations.csv). The [recorded summary](recorded/results.json) identifies the compiler versions, driver and reference assembly digests, source digest and host. Compiler hashes and environment values can differ on other systems; the specified numeric values are fixed.

Two compiler drivers, two optimization settings, two source variants: eight executions. These are repeated evaluations on one host, not eight independent machines. The signed variant is deliberately wrong for the specified input field. It tests the checker; it does not identify a compiler defect.
