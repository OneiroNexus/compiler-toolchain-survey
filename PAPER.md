# Compilers, Codecs and Language Toolchains: What Agreement Between Builds Can Establish

Aaron Michael Weis · Oneiron Holdings LLC · [ORCID 0009-0002-1906-148X](https://orcid.org/0009-0002-1906-148X)
Research preprint · v0.1.0 · 23 November 2026

## Abstract

Two builds of a program return the same answer. What has been checked? This paper develops that question from a purposive catalogue of 73 compilers, build tools, formats and codecs. The catalogue separates a change in how a program is translated from a change in how its data are stored. Its 43 compiler and toolchain entries show why the language front end, generated target and execution host matter when judging agreement. A worked example tests the high four bits of every possible byte against a reference derived from the specification. All four builds of the unsigned program matched the specification on all 256 inputs. All four deliberately signed controls agreed with one another while returning wrong values for the same 128 inputs. A final proposal applies the distinction to sensor-event replay for an augmented-reality game engine. The software example and the proposed physical measurements answer different questions.

**Keywords:** compilers; differential testing; test oracles; software portability; lossless compression; sensor-event replay.

## 1. The question a second build can answer

A programmer receives a status byte whose high four bits encode a value between zero and fifteen. For the byte 0x80, the field is 8. A program that first reads the byte as a signed value can return -8 instead. Rebuilding the same mistaken program with a second compiler may reproduce -8 perfectly. A useful test must ask two questions: did the builds agree, and which answer did the field definition require?

Let A(x) and B(x) be two builds' observable outputs, and let R(x) be the answer fixed independently for input x. Agreement tests A(x) = B(x). Conformance tests A(x) = R(x) and B(x) = R(x). The first relation does not imply the other two. This is the established test-oracle problem in a particularly small setting [1]. Differential compiler testing has a substantial history; Csmith, for example, generates C programs and compares their behaviour across compilers [2]. This study contributes a documented catalogue and an inspectable teaching case. It does not claim to introduce either technique.



## 2. Building a catalogue that answers a question

The starting point was a working list of tools assembled by the author. Its entries were chosen for their relevance to portability, storage or verification. This is a purposive survey: counts describe this collection and cannot estimate how common a technology is. The November 18 source pass examined project descriptions, manuals, specifications and bibliographic records with AI-assisted retrieval. That workflow returned summaries for some pages; two historical Scala.js release notes were accessible only as search extracts. No release-specific speed, size or license recommendation here depends on those extracts.

| Catalogue family | Entries | What an entry can help identify |
|---|---:|---|
| General and structure-aware compression | 13 | The data format, library or binding that handles bytes |
| Genomic file tools and formats | 17 | Where a file specification, program or paper applies |
| Scala, JVM and JavaScript toolchain | 5 | Compiler, build driver, linker or optimizer |
| Hardware-description toolchains | 3 | Simulation model or synthesizable design output |
| GNU front ends and related listings | 7 | Language entry point or documented list of front ends |
| Other language compilers and toolchains | 24 | Native, virtual-machine, browser or data-parallel target |
| Verification-oriented languages | 4 | The boundary between a property and executed code |

Thirty entries concern codecs and formats; 43 concern compilers and the surrounding toolchain. A row is one catalogue entry, not necessarily one distinct compiler executable. For example, the GNU front-end list is itself a row. The appendix identifies a public source for all 73 entries. Sixty-nine entries point to project or specification sources, three to articles, and one to a bibliographic record only. The FQC bibliographic entry is distinct from LFQC. For LFQC the catalogue follows the publisher's designation of the definitive 2015 article; the withdrawn duplicate is not evidence [3].

A compiler translates a program into another representation. A lossless codec is judged instead by whether decoding recovers the intended input bytes. Two correct compilers may emit different binaries; two lossless encoders may emit different compressed streams. A byte comparison makes sense only after choosing which bytes must be preserved. In this study no compression performance is ranked. The accompanying CSV supplies stable entry labels, source links and short descriptions so a reader can follow or challenge any classification.



## 3. Choose the point of comparison

**Source and front end.** A difference between compiler names need not imply an independent language implementation. LDC documents that it uses the DMD front end and LLVM for code generation [4]. DMD and LDC can therefore give useful evidence about different output paths while sharing part of the interpretation of the source. GDC provides another D compiler in GCC [5]. A meaningful comparison fixes the source, inputs and defined behaviour, records the exact builds, and compares program results. Its interpretation should name any shared component it knows about.

**Target and host.** Scala.js illustrates a different separation. The same source language can feed a JavaScript target, while the Scala.js WebAssembly backend has its own configuration and host requirements [6]. If a test browser cannot load the generated module, that is a host-compatibility result. It is not a numerical disagreement. If two targets load but return different answers on the same input, retain that input and compare the language and runtime rules before blaming either compiler.

**Model and device.** XLS can produce synthesizable hardware descriptions; Verilator can turn a Verilog or SystemVerilog design into an executable model [7, 8]. Comparing a model trace with a software reference is informative about modeled behaviour. A passing trace cannot measure a physical clock, sensor delay or drift. Those require a separate observation.

| Claim | Comparator | What would count against the claim? |
|---|---|---|
| Two builds agree on a stated domain | Same specified inputs and outputs | A single unequal output on that domain |
| An implementation satisfies a field definition | Independently calculated expected value | A build differs from the prescribed value |
| A lossless round trip restores the intended record | Retained original bytes | Any restored byte differs, even if two decoders agree |
| A physical timing path meets a requirement | Independent timing reference and declared tolerance | A measured error outside the stated tolerance |

A proof-oriented language introduces another boundary. A property proved about a source definition and the behaviour of an extracted executable are distinct observations unless the extraction and execution steps are also covered. The four verification-oriented entries in the catalogue identify places to investigate that boundary. This paper proves no compiler correct.



## 4. One byte, two compilers, an independent answer

**Specification.** The input x is an integer in the closed interval 0 through 255. Return its upper four bits as a nonnegative integer. The independent reference is the integer quotient of x divided by 16. This gives easily checked boundary pairs: 15 maps to 0 and 16 maps to 1; 127 maps to 7 and 128 maps to 8; 255 maps to 15. The complete domain is small enough to enumerate.

**Positive and negative controls.** The C# source first treats the byte as unsigned and shifts it right four positions. The deliberately incorrect version interprets it as a signed eight-bit value before shifting. C# promotes small integer operands before applying the shift; right shifting a negative signed integer sign-extends it [9]. The prediction is exact: the signed control should agree with the reference for 0 through 127 and disagree for 128 through 255. Disagreement with that prediction is a failed experiment, even if compiler outputs agree.

**Execution.** The .NET Framework C# compiler (14.8.10001.0) and Visual Studio Roslyn (4.14.0-3.25412.6) compiled both variants with optimization on and off. Each build explicitly targeted AnyCPU and the same .NET Framework core assembly. All eight executions used the same Windows x64 host. A Python checker calculated the reference by integer division and compared each emitted integer. It also checked which inputs should fail in the negative control.

| Program variant | Builds | Inputs per build | Disagreements between builds | Errors against specification, per build |
|---|---:|---:|---:|---:|
| Unsigned input | 4 | 256 | 0 | 0 / 256 |
| Signed reinterpretation | 4 | 256 | 0 | 128 / 256 |

**Result.** At 127, both variants returned 7 in every build. At 128 the unsigned variant returned 8 and the signed variant returned -8; at 255 the two values were 15 and -1. All 128 errors in each signed build fell in the upper half of the domain. Comparing compiler outputs alone would have passed the control in all four configurations. The independent specification rejected it in all four. [Read the 256 input rows](https://github.com/OneiroNexus/compiler-toolchain-survey/blob/v0.1.0/experiment/recorded/observations.csv) or [rerun the example](https://github.com/OneiroNexus/compiler-toolchain-survey/blob/v0.1.0/experiment/README.md).

An exhaustive check here covers exactly one finite input domain under the recorded execution environment. It neither samples a distribution of production inputs nor estimates a general compiler failure rate. The negative control is an error in the test program's interpretation of the byte. It is not a compiler defect. A smaller or faster executable would not alter that conclusion.



## 5. A proposed use in the Omega Game Sphere

In an augmented-reality game, two sensor events can be captured in one order and arrive at the engine in another. Aaron Michael Weis's public Omega Game Sphere brief identifies this as a proposed timing problem for the OneiroNexus game engine [10]. The compiler question has a narrow, practical place here: before interpreting a reversal as a sensor effect, check whether two software builds order the same input differently.

A first experiment needs only synthetic observations. Specify an event identifier, integer capture time and integer arrival time in a single named unit. Choose the tie rule before running the builds. For example, a toy trace might contain event A captured at 100 and arriving at 108, and event B captured at 103 and arriving at 106. Capture order is A then B; arrival order is B then A. Compare each build's output with the prescribed order and with the other build. Repeat with equal capture times, late arrivals and a declared boundary case. Those numbers define an illustrative fixture, not measurements from a game or a facility.

Only a second, separately agreed experiment needs a physical testbed. The Colorado Quantum Incubator (COQI) describes its Quantum Timing Testbed as an open-access facility for evaluating timing technology [11]. Weis proposes it as a possible site for comparing sensor timestamps with an independent reference. If access, equipment and the test plan are agreed, record capture-time error against that reference and capture-to-arrival latency separately. Then replay the recorded events through the same builds. This would help distinguish a disagreement that already exists in software from one that appears only with measured inputs.

The author proposes COQI as the test site. The work reported in this paper used no COQI equipment, participants or sensor records. It establishes no partnership, endorsement, site approval or measured sensor performance.

## 6. What to report next time

Publish the input definition, the output that matters, the reference that could contradict the builds, and the exact scope of the run. Record failures to load separately from wrong answers. Where agreement is the only evidence, report agreement. A future reader can then tell whether another compiler, another runtime or an actual measurement would add information.



## Sources and reproducibility

[1] Barr, E. T., Harman, M., McMinn, P., Shahbaz, M. and Yoo, S. (2015). [The Oracle Problem in Software Testing: A Survey](https://doi.org/10.1109/TSE.2014.2372785). IEEE Transactions on Software Engineering 41(5), 507-525.

[2] Yang, X., Chen, Y., Eide, E. and Regehr, J. (2011). [Finding and Understanding Bugs in C Compilers](https://www.flux.utah.edu/paper/yang-pldi11). ACM SIGPLAN Conference on Programming Language Design and Implementation.

[3] Oxford University Press (2020). [Publisher's correction identifying the definitive LFQC article](https://doi.org/10.1093/bioinformatics/btaa1035). [Definitive article](https://doi.org/10.1093/bioinformatics/btv384).

[4] LDC developers. [LDC: the LLVM-based D compiler](https://github.com/ldc-developers/ldc). See the project description of the DMD frontend.

[5] GNU Project. [GDC: the GNU D compiler](https://gcc.gnu.org/onlinedocs/gdc/).

[6] Scala.js project. [Scala.js](https://www.scala-js.org/) and [WebAssembly backend and host requirements](https://www.scala-js.org/doc/project/webassembly.html).

[7] XLS project. [XLS: Accelerated Hardware Synthesis](https://google.github.io/xls/).

[8] Verilator project. [Overview: from hardware description to executable model](https://verilator.org/guide/latest/overview.html).

[9] Microsoft. [C# bitwise and shift operators](https://learn.microsoft.com/en-us/dotnet/csharp/language-reference/operators/bitwise-and-shift-operators).

[10] Weis, A. M. (2026). [Sensor timing for the Omega Game Sphere AR engine, v0.1.0](https://doi.org/10.5281/zenodo.24357940). Separately archived proposal.

[11] Colorado Quantum Incubator. [Open-access Quantum Timing Testbed](https://quantumincubator.org/quantum-testbed/). Facility description; no participation in the present study is asserted.

**Contributions and interests.** Aaron Michael Weis assembled the research collection, framed the portability questions and proposed the game-engine application. He is affiliated with Oneiron Holdings LLC, which develops the project discussed in section 5. Claude assisted the original source collection and drafting. Codex prepared this edition, implemented the worked example and checked its outputs. The named tools and cited prior work belong to their respective authors.

**Availability and reuse.** The versioned repository includes this paper, the complete source-linked catalogue and the worked example. The paper and original catalogue descriptions are CC BY 4.0 International. The original example code is MIT licensed. Cited projects and other third-party materials retain their own terms. [Edition and citation links](https://github.com/OneiroNexus/compiler-toolchain-survey/releases/tag/v0.1.0).

## Appendix. The source-linked catalogue

The following 73 entries retain the catalogue order. Select a project or paper name to open its source. Descriptions identify the role of each entry; they do not certify current builds, validate performance, or grant rights in third-party tools.

### General-purpose and structure-aware compression

C01 · [Zstandard (zstd)](https://github.com/meta/zstd) — Zstandard defines a lossless compression format and provides a library and command-line tool for working with it.

C02 · [Zstandard for the JVM (zstd-jni)](https://github.com/luben/zstd-jni) — This library exposes Zstandard compression and decompression to programs running on the Java Virtual Machine.

C03 · [Aircompressor](https://github.com/airlift/aircompressor) — Aircompressor provides compression codecs for Java applications.

C04 · [Snappy Java (snappy-java)](https://github.com/xerial/snappy-java) — Snappy Java connects Java programs to the Snappy compression library and packages native binaries.

C05 · [LZ4 Java](https://github.com/lz4/lz4-java) — LZ4 Java provides Java interfaces for LZ4 compression and xxHash checksums.

C06 · [Java GZIP and Deflate](https://docs.oracle.com/en/java/javase/21/docs/api/java.base/java/util/zip/package-summary.html) — The Java standard library provides GZIP streams and classes for deflating and inflating byte streams.

C07 · [PAQ (paq8px)](https://github.com/hxim/paq8px) — paq8px is an experimental program for lossless file compression.

C08 · [cmix](https://github.com/byronknoll/cmix) — cmix is a lossless compressor designed to favor compressed size over encoding speed.

C09 · [ZPAQ](https://mattmahoney.net/dc/zpaq.html) — ZPAQ is a command-line archiver that can append changed files to an existing backup.

C10 · [OpenZL](https://github.com/meta/openzl) — OpenZL is a framework for building lossless compressors that use the structure of a data format.

C11 · [JPEG XL (libjxl, cjxl and djxl)](https://github.com/libjxl/libjxl) — The libjxl implementation supplies the cjxl encoder and djxl decoder for JPEG XL images.

C12 · [FSE and Huff0](https://github.com/Cyan4973/FiniteStateEntropy) — The FiniteStateEntropy project contains implementations of the FSE and Huff0 entropy coders.

C13 · [LZAV](https://github.com/avaneev/lzav) — LZAV provides an in-memory lossless compressor in a C header.


### Genomic-sequence compressors and file formats

C14 · [GeCo3](https://github.com/cobilab/geco3) — GeCo3 is research software for compressing files of DNA sequence data.

C15 · [CRAM](https://samtools.github.io/hts-specs/CRAMv3.pdf) — CRAM specifies a compact file format for storing sequencing alignment records.

C16 · [SAMtools](https://www.htslib.org/) — SAMtools supplies command-line utilities for reading and working with SAM, BAM and CRAM alignment files.

C17 · [HTSlib](https://github.com/samtools/htslib) — HTSlib gives C programs a common interface to several sequencing file formats.

C18 · [HTSJDK](https://github.com/samtools/htsjdk) — HTSJDK provides Java interfaces for reading and writing several sequencing data formats.

C19 · [Picard](https://github.com/broadinstitute/picard) — Picard is a collection of Java command-line tools for processing sequencing data files.

C20 · [Slimfastq](https://github.com/Infinidat/slimfastq) — Slimfastq is a command-line compressor and decompressor for FASTQ files.

C21 · [FQC](https://pubmed.ncbi.nlm.nih.gov/25790783/) — Dutta and colleagues published FQC as a method for archiving FASTQ data in 2015.

C22 · [LFQC](https://doi.org/10.1093/bioinformatics/btv384) — Nicolae, Pathak and Rajasekaran describe LFQC as a lossless compression method for FASTQ files in their 2015 article.

C23 · [DSRC 2](https://github.com/refresh-bio/DSRC) — DSRC 2 provides software for compressing reads stored in FASTQ files.

C24 · [SPRING](https://github.com/shubhamchandak94/Spring) — SPRING is a compression tool for sequencing data stored in FASTQ files.

C25 · [Fqzcomp](https://github.com/jkbonfield/fqzcomp) — Fqzcomp is a command-line program for compressing FASTQ files.

C26 · [Quip](https://github.com/dcjones/quip) — Quip compresses sequencing records in FASTQ, SAM and BAM formats.

C27 · [FaStore](https://github.com/refresh-bio/FaStore) — FaStore is an archival tool for collections of short reads in FASTQ files.

C28 · [MFCompress](https://academic.oup.com/bioinformatics/article/30/1/117/236841) — Pinho and Pratas describe MFCompress as a compression program for FASTA data.

C29 · [JARVIS3](https://github.com/cobilab/jarvis3) — JARVIS3 is a research compressor for DNA sequence files.

C30 · [DNAzip](https://academic.oup.com/bioinformatics/article/25/2/274/218156) — Christley and colleagues describe DNAzip as a research method for storing individual genome data in compressed form.


### The Scala, JVM and JavaScript toolchain

T01 · [Scala 3 compiler](https://github.com/scala/scala3) — The Scala 3 implementation includes the compiler developed under the name Dotty.

T02 · [Scala CLI](https://github.com/VirtusLab/scala-cli) — Scala CLI provides command-line operations to compile, run, test and package Scala projects.

T03 · [sbt](https://www.scala-sbt.org/) — sbt manages builds and dependencies for Scala and Java projects.

T04 · [Scala.js](https://www.scala-js.org/doc/internals/compile-opt-pipeline.html) — Scala.js compiles Scala sources to intermediate files and links them into JavaScript.

T05 · [Google Closure Compiler](https://github.com/google/closure-compiler) — Closure Compiler checks JavaScript source and transforms it into optimized JavaScript.


### Compilers for hardware-description languages

T06 · [GHDL](https://github.com/ghdl/ghdl) — GHDL analyzes and simulates designs written in VHDL.

T07 · [Verilator](https://verilator.org/guide/latest/overview.html) — Verilator translates Verilog and SystemVerilog designs into C++ or SystemC models.

T08 · [XLS](https://google.github.io/xls/) — XLS provides a high-level synthesis toolchain that can generate hardware descriptions from DSLX programs.


### The GNU Compiler Collection and its front ends

T09 · [GCC front-end list](https://gcc.gnu.org/frontends.html) — GCC maintains a list of language front ends included in the main compiler collection.

T10 · [GNAT (Ada)](https://gcc.gnu.org/onlinedocs/gnat_ugn/) — GNAT supplies the Ada compiler and tools documented in the GNU Ada development environment.

T11 · [GDC (D)](https://gcc.gnu.org/onlinedocs/gdc/) — GDC is the D language compiler in the GNU Compiler Collection.

T12 · [GNU Modula-2 (gm2)](https://gcc.gnu.org/onlinedocs/gm2/) — GNU Modula-2 provides a Modula-2 compiler as part of GCC.

T13 · [ALGOL 68 (ga68)](https://gcc.gnu.org/gcc-16/changes.html) — The GCC 16 release notes describe ga68 as an experimental compiler for ALGOL 68.

T14 · [gccrs (Rust)](https://github.com/rust-gcc/gccrs) — The gccrs project develops a Rust compiler front end for GCC.

T15 · [Front ends maintained outside GCC](https://gcc.gnu.org/frontends.html) — GCC separately lists independently maintained front ends associated with its compiler infrastructure.


### Systems and native-code languages

T16 · [DMD](https://github.com/dlang/dmd) — DMD is the reference compiler for the D programming language.

T17 · [LDC](https://github.com/ldc-developers/ldc) — LDC combines the D language front end with LLVM for code generation.

T18 · [Nim](https://nim-lang.org/) — The Nim compiler can translate programs to C, C++ or JavaScript.

T19 · [Crystal](https://github.com/crystal-lang/crystal) — Crystal is a statically typed language whose compiler produces native executables.

T20 · [Odin](https://github.com/odin-lang/Odin) — The Odin project maintains a compiler for the Odin programming language.

T21 · [Zig](https://ziglang.org/) — The Zig toolchain supports cross-compilation and includes drivers for compiling C and C++.

T22 · [V](https://vlang.io/) — The V compiler can translate V programs to C source code.

T23 · [Pony](https://www.ponylang.io/) — Pony is a statically typed programming language that uses actors for concurrency.

T24 · [Red](https://www.red-lang.org/p/documentation.html) — The Red toolchain includes the Red language and the lower-level Red/System dialect.

T25 · [Seed7](https://seed7.sourceforge.net/) — Seed7 supplies an interpreter and a compiler that translates programs into C.


### Functional, logic and effect-typed languages

T26 · [Mercury](https://www.mercurylang.org/) — Mercury is a statically typed language for logic and functional programming.

T27 · [ATS](https://github.com/githwxi/ATS-Postiats) — ATS/Postiats implements the ATS programming language and generates C code.

T28 · [PureScript](https://github.com/purescript/purescript) — The PureScript compiler translates programs written in a strongly typed functional language to JavaScript.

T29 · [Koka](https://github.com/koka-lang/koka) — Koka is a programming language whose type system can express computational effects.

T30 · [Unison](https://github.com/unisonweb/unison) — Unison identifies code definitions by hashes of their syntax trees.

T31 · [Gleam](https://github.com/gleam-lang/gleam) — The Gleam project develops a statically typed language and its compiler.

T32 · [Roc](https://github.com/roc-lang/roc) — The Roc project develops a compiler for the Roc functional programming language.


### Data-parallel compilers

T33 · [Futhark](https://futhark-lang.org/) — Futhark compiles a functional array language into code for parallel computation.

T34 · [ISPC](https://ispc.github.io/) — ISPC compiles a C-like language with single-program, multiple-data extensions for parallel execution.


### The Oberon and Pascal family

T35 · [Oberon+ toolkit](https://github.com/rochus-keller/Oberon) — The Oberon+ toolkit includes a compiler and multiple code-generation back ends.

T36 · [Oxford Oberon-2 compiler](https://spivey.oriel.ox.ac.uk/corner/Oxford_Oberon-2_compiler) — The Oxford Oberon-2 compiler produces bytecode for its runtime to execute.

T37 · [Gardens Point Component Pascal (GPCP)](https://github.com/k-john-gough/gpcp) — Gardens Point Component Pascal compiles Component Pascal for the JVM or the .NET runtime.


### Embeddable and multi-backend languages

T38 · [Rakudo](https://github.com/rakudo/rakudo) — Rakudo is a compiler implementation of the Raku programming language.

T39 · [Janet](https://janet-lang.org/) — Janet is an embeddable language with a compiler and a bytecode interpreter.


### Verification-oriented languages

T40 · [F*](https://github.com/FStarLang/FStar) — F* is a proof-oriented programming language that supports checking programs against specifications.

T41 · [Lean 4](https://github.com/leanprover/lean4) — Lean 4 combines a theorem prover with a functional programming language.

T42 · [Idris 2](https://idris2.readthedocs.io/en/latest/) — Idris 2 documents several compiler back ends, including Chez Scheme and JavaScript.

T43 · [Rocq](https://rocq-prover.org/) — Rocq is an interactive proof assistant for developing and checking formal proofs.
