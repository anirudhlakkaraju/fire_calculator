# Firefly - Ideas & Roadmap

**Project:** Firefly - Financial Independence Calculator
**Website:** [likeafirefly.com](https://likeafirefly.com) _(coming soon)_
**CLI Command:** `firefly`

---

## Core Insight

The single most important factor on your FIRE journey is your **savings rate**. With high savings rate (50-90%), FI is achievable **irrespective** of income level.

## Formula Solver

Given any 3 of these variables, solve for the 4th:

- `x` = savings rate (% of income saved)
- `r` = real return rate (investment return - inflation)
- `N` = FI number multiplier (25x for 4% rule, 40x for 2.5% rule)
- `t` = time to FI

## Potential Calculations

### 1. Sensitivity Analysis

- How does ±1% change in return rate affect time to FI?
- How does ±5% change in savings rate affect time to FI?
- Monte Carlo simulation with variable returns

### 2. Coast FIRE Calculation

- Given current portfolio, what age will it grow to FI target with no additional contributions?
- "How much do I need NOW to coast to FI by age X?"

### 3. Sequence of Returns Risk

- Early retirement is vulnerable to market crashes in first few years
- Visualize different withdrawal scenarios with historical data

### 4. Savings Rate vs Time to FI Graph

- Classic visualization showing the exponential relationship
- Shows FI possible in 10-15 years at 50%+ savings rate

### 5. Income vs Expenses Paths

- Show growing investment portfolio vs. stable expense needs
- Visualize the "crossover point"

### 6. Tax Optimization

- Traditional vs Roth conversions
- Tax-efficient withdrawal strategies (ladder, etc.)

### 7. Geographic Arbitrage

- Same portfolio, different locations with different costs
- LeanFIRE in LCOL vs FatFIRE in HCOL

### 8. Partial FIRE / Barista FIRE

- How much part-time income reduces portfolio withdrawal needs
- "If I make $X/year part-time, how much less do I need saved?"

## Implementation Priority

1. ✅ Simple compound interest calculator (DONE)
2. Core FIRE formula solver
3. Visualizations for key insights
4. Additional scenarios as needed

## UX/QOL Enhancements

### Phase 1 (IN PROGRESS)

- ✅ Parameter cache with defaults (in-memory)
- ✅ Summary + Edit specific fields
- ✅ Better exit instructions

### Phase 2 (Future)

- "What if" quick edits after calculation
  - "What if you doubled your contribution?"
  - "What if you started with 2x principal?"
  - "What if return was 5% instead of 7%?"
- Comparison mode - side-by-side scenarios
- Export results to CSV/JSON
- Visual improvements:
  - Show percentage of portfolio that's interest vs contributions
  - Show "money working for you" vs "money you put in"
  - Add milestones: "You'll hit $X in month Y"

### Phase 3 (Future)

- Quick presets: "First time buyer", "Retirement planning", etc.
- Save/load named scenarios
- Smart defaults based on inputs
- Better input validation with helpful messages and examples

## Architecture Roadmap

### Current (v0.1.0)

- ✅ Core business logic (pure Python, no UI dependencies)
- ✅ CLI with interactive questionary interface
- ✅ ASCII visualizations with Rich and Plotext
- ✅ Monorepo structure with clean separation

### Planned

- 🔜 TUI (Text User Interface) with live-updating graphs (Textual framework)
- 🔜 REST API for web integration
- 📅 Web UI (using API)
- 📅 Mobile app (using API)

### Architecture

**Monorepo structure with clean separation:**

- `firefly.core` - Pure business logic (models + calculators, **zero external dependencies**)
- `firefly.cli` - Terminal interface (questionary-based, optional install)
- `firefly.api` - REST API endpoints _(future, optional install)_

**Installation options:**

- `pip install firefly` - Core only (for library use)
- `pip install firefly[cli]` - Core + CLI
- `pip install firefly[api]` - Core + API _(future)_
