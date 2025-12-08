# LikeAFirefly - Ideas & Roadmap

**Project:** LikeAFirefly - Financial Independence Calculator
**Website:** [likeafirefly.com](https://likeafirefly.com) _(coming soon)_

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

## Implementation Roadmap

### ✅ Foundation (COMPLETE)

- ✅ Core calculator engine (compound interest with contributions)
- ✅ Clean architecture (core/api separation)
- ✅ FastAPI backend with auto-generated docs
- ✅ Type-safe models with Pydantic
- ✅ CLI interface (kept for fun)

### 🚀 Phase 1: Launch Calculators (IN PROGRESS)

**Goal:** Beautiful, functional web app with core FIRE calculators

#### 1. **"When Can I Quit?" Calculator** (Hero/Landing Page)

- **Inputs:** Current portfolio, monthly expenses, safe withdrawal rate (4% default)
- **Outputs:**
  - Exact date you can retire
  - Countdown timer
  - Visual timeline showing "You are X% there"
- **Status:** Next to build

#### 2. **"One More Year" Syndrome Calculator**

- **Inputs:** Current portfolio, savings rate, monthly expenses, withdrawal rate (if still getting paycheck + portfolio)
- **Outputs:**
  - Table showing marginal utility of each additional year
  - "Year 1: +$X safety, -12 months freedom"
  - "Year 2: +$Y safety, -24 months freedom (diminishing returns)"
  - Visualization of diminishing marginal returns
- **Status:** Backlog

#### 3. **"Real Return Reality Check"** (Global Toggle)

- **Feature:** Toggle on ALL calculators showing "Nominal vs Real Returns"
- **Shows:**
  - Nominal: 10% market return = "$1M → $2.5M"
  - Real: After 3% inflation + 2% taxes = "$1M → $1.6M in today's dollars"
- **Status:** Core feature to build into calculator engine

### 🔥 Phase 2: Power User Features

#### 4. **"F-You Money" Calculator**

- **Concept:** Not full FIRE, but enough runway to quit toxic job
- **Inputs:** Monthly expenses, risk tolerance
- **Outputs:**
  - 1-2 year runway amount
  - "You need $X to walk away tomorrow"
- **Why:** Everyone's definition is different, personalized approach

#### 5. **"Still Working After FI" Calculator**

- **Concept:** Reached FI but still working (visa, commitments, choice)
- **Inputs:** FI number, current portfolio, current income, expenses
- **Outputs:**
  - How portfolio grows while still earning
  - "Fat FIRE" acceleration timeline
  - Flexibility score

#### 6. **"Side Hustle Impact" Calculator**

- **Inputs:** Current savings, side hustle monthly income
- **Outputs:**
  - Years saved by investing side income
  - "Extra $500/month = retire X years earlier"

### 📊 Phase 3: Advanced Features

#### 7. **"Sequence of Returns Risk" Visualizer**

- **Concept:** Monte Carlo simulation with historical data
- **Shows:** How retiring in 2008 vs 2010 affects outcomes
- **Why:** Educational + learn Monte Carlo implementation
- **Status:** Learning project

#### 8. **Comparison Mode**

- Side-by-side scenario comparison
- "What if I save 10% more?"
- Export to CSV/JSON

#### 9. **Visual Enhancements**

- Show % of portfolio that's interest vs contributions
- "Money working for you" vs "Money you put in"
- Milestone markers: "You'll hit $X in month Y"

## Architecture

### Current Stack (v0.2.0)

**Backend:**

- `firefly.core` - Pure Python business logic (zero UI dependencies)
- `firefly.api` - FastAPI REST API with auto-docs
- Stateless, serverless-ready

**Frontend (To Build):**

- Next.js 14 + TypeScript
- Tailwind CSS + shadcn/ui (beautiful components)
- Recharts (gorgeous interactive graphs)
- Deployed on Vercel (free tier)

**Hosting:**

- Frontend: Vercel (free)
- Backend: Vercel/Fly.io (free tier)
- **Total cost: $0-5/month** (vs $30 EC2)

### Installation Options

- `pip install firefly` - Core only (for library use)
- `pip install firefly[cli]` - Core + CLI
- `pip install firefly[api]` - Core + API (FastAPI)

### Domain

- **likeafirefly.com** (acquired! 🎉)
