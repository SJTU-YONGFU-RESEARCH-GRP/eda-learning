# Rip-up and reroute — step-by-step (for slides / transcript)

**Module:** `module03-03-ripup-reroute`  
**Lab / algo:** `ripup-reroute`  
**Viewer:** `/tools/algorithm-walkthrough/?algo=ripup-reroute&step=1`

Use each **Caption** as spoken prose (or a shortened slide note).
Use **Bullets** on the PPT; pair with the PNG in `assets/steps/`.

## Step 1 — Sequential L first

![Step 1](steps/01-seq.png)

**Caption (transcript):** Route L-HV; some edges exceed Cap.

**Slide bullets:**

- Overflow appears
- Before rip

**On-screen metrics:**

```
total≈2
```

## Step 2 — Pick hot edge

![Step 2](steps/02-pick.png)

**Caption (transcript):** Find worst overflowing edge; mark nets using it.

**Slide bullets:**

- Shared corridor
- Toy rip order

**On-screen metrics:**

```
Worst edge first
```

## Step 3 — Rip nets

![Step 3](steps/03-rip.png)

**Caption (transcript):** Remove those nets from usage.

**Slide bullets:**

- Subtract paths
- Ready to reroute

**On-screen metrics:**

```
Usage drops
```

## Step 4 — Maze reroute

![Step 4](steps/04-maze-r.png)

**Caption (transcript):** Ripped nets maze-route with updated usage.

**Slide bullets:**

- May improve
- GOLDENS.ripupImproves

**On-screen metrics:**

```
After ripup
```

## Step 5 — Iterate

![Step 5](steps/05-loop.png)

**Caption (transcript):** Real routers loop estimate→route→rip until clean or budget.

**Slide bullets:**

- Detailed route next
- learn_routing

**On-screen metrics:**

```
Course arc
```

