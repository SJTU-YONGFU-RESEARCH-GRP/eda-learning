# Examples — Offline benchmark compare

1. Export the same tiny netlist used in critical-path / incremental modules.
2. Run your toy STA; record WNS, TNS, worst path delay, wall time.
3. If available, run an open timer (e.g. OpenSTA-style flow) on the same instance.
4. Fill a comparison table: WNS, TNS, path agreement, runtime, notes.
5. If the external tool is missing, document install blockers and still validate your harness I/O.
