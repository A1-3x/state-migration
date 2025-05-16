
*From ChatGPT:*
---

# 📦 Using ACS PUMS to Study Migration Reasons

The **American Community Survey (ACS) Public Use Microdata Sample (PUMS)** provides person- and household-level data that can be used to study patterns and inferred reasons behind migration.

---

## 1. 🧠 What Does ACS PUMS Offer?

### **Key Migration-Related Variables**

| Variable  | Description                                 |
| --------- | ------------------------------------------- |
| `MIG`     | Migration status (moved in the last year)   |
| `MIGSP`   | State of residence 1 year ago               |
| `MIGPUMA` | PUMA of residence 1 year ago                |
| `POBP`    | Place of birth                              |
| `YOEP`    | Year of entry (foreign-born individuals)    |
| `RESMODE` | Mode of transportation to current residence |

### **Demographic/Economic Variables (Proxies for Motivation)**

* `AGEP`: Age
* `SEX`: Sex
* `MAR`: Marital status
* `SCHL`: Educational attainment
* `ESR`: Employment status
* `HINCP`: Household income
* `WAGP`: Wages or salary income
* `HINS1-5`: Health insurance coverage indicators

---

## 2. ❓ Define Your Research Questions

Sample research questions:

* Why do people move across states or PUMAs?
* Are job-related moves more common than housing-related moves?
* Do younger adults move more for education?
* Do retirees move to different climates?

### **Inferred Reason → Proxy Variables**

| Inferred Reason | Proxy Variables                                            |
| --------------- | ---------------------------------------------------------- |
| **Employment**  | `ESR`, industry, occupation, income                        |
| **Education**   | Enrollment status (`SCHG`), age group                      |
| **Housing**     | Change in PUMA, rent/mortgage, household size              |
| **Family**      | Marital status, presence of children                       |
| **Retirement**  | Age 65+, not in labor force, moving to "retirement" states |

---

## 3. 🔧 Prepare the Data

1. **Download ACS PUMS**:

   * [data.census.gov](https://data.census.gov)
   * [IPUMS-USA](https://usa.ipums.org/usa/) (preferred for labeled variables)

2. **Choose Sample**:

   * 1-Year PUMS: Year-over-year moves
   * 5-Year PUMS: Small-area analysis, more stability

3. **Use Software**:

   * Python (Pandas), R, Stata, or SAS
   * Or use [IPUMS Online Analysis Tool](https://usa.ipums.org/usa/sda/)

---

## 4. 🧮 Construct Migration Measures

### **Identify Movers**

```python
# Pseudocode
recent_mover = MIG != 1  # 1 = Same house last year
```

### **Distance of Move**

| Move Type       | Determination              |
| --------------- | -------------------------- |
| Local Move      | Same PUMA, different house |
| Regional Move   | Different PUMA, same state |
| Interstate Move | `MIGSP` ≠ current state    |

---

## 5. 📊 Analyze with Proxy Indicators

### **Examples**

* **Logistic Regression**: Predict probability of migrating
* **Cross-tabulations**: Movers vs. non-movers by education/income
* **Cluster Analysis**: Segment movers into groups (e.g. students, workers, retirees)

---

## 6. ⚠️ Limitations

* **No direct reason** for migration — must infer using proxy variables
* **Geography limited** to PUMAs (\~100,000+ people)
* **Use weights**: `PWGTP` for person-level, `WGTP` for household-level analysis

---

## 🧪 Example Research Use Case

**Question**: *Do college graduates move across states for jobs more than non-graduates?*

**Steps**:

1. Filter age 25–64
2. Identify interstate movers: `MIGSP ≠ current state`
3. Compare `SCHL` (education) and `ESR` (employment status)
4. Run logistic regression:

   ```python
   outcome = migration_status  
   predictors = education + age + income + employment_status
   ```

---

Let me know if you want R or Python code templates, or a guide to downloading the right data from IPUMS.

Great! Below are **code templates in both R and Python** to help you analyze ACS PUMS data for migration-related questions.

---

## 📁 Data Assumptions

These templates assume you are working with **ACS PUMS CSV files** downloaded from [IPUMS-USA](https://usa.ipums.org/usa/), which include:

* **Person-level data** (e.g., `usa_00001.csv`)
* Corresponding **codebook** (usually `*.do` or `*.xml`) for variable meanings

---

## 🐍 Python Template (Using `pandas`)

```python
import pandas as pd

# Load the data
df = pd.read_csv("usa_00001.csv")

# Convert missing values (IPUMS codes missing as specific integers like 9999999)
df.replace({9999999: pd.NA, 999999: pd.NA, 999: pd.NA}, inplace=True)

# Subset working-age population
df = df[(df['AGE'] >= 25) & (df['AGE'] <= 64)]

# Create migration flag (moved from different state)
df['interstate_mover'] = df['MIGSP'] != df['STATEFIP']  # MIGSP = state 1 year ago, STATEFIP = current

# Create binary education variable (college degree or higher)
df['college_grad'] = df['EDUC'].apply(lambda x: 1 if x >= 101 else 0)  # IPUMS code 101+ = Bachelor's+

# Drop missing values in key columns
df = df.dropna(subset=['interstate_mover', 'college_grad', 'INCTOT'])

# Run logistic regression
import statsmodels.api as sm

X = df[['college_grad', 'AGE', 'INCTOT']]  # Add other variables as needed
X = sm.add_constant(X)
y = df['interstate_mover'].astype(int)

model = sm.Logit(y, X)
result = model.fit()
print(result.summary())
```

---

## 📊 R Template (Using `tidyverse` + `survey`)

```r
library(tidyverse)
library(survey)

# Load data
df <- read_csv("usa_00001.csv")

# Subset working-age population
df <- df %>%
  filter(AGE >= 25, AGE <= 64)

# Create migration variable
df <- df %>%
  mutate(interstate_mover = if_else(MIGSP != STATEFIP, 1, 0),
         college_grad = if_else(EDUC >= 101, 1, 0))  # Bachelor's or higher

# Remove rows with missing values in key vars
df_clean <- df %>%
  drop_na(interstate_mover, college_grad, INCTOT)

# Set up survey design using person weights
design <- svydesign(ids = ~1, weights = ~PERWT, data = df_clean)

# Logistic regression
model <- svyglm(interstate_mover ~ college_grad + AGE + INCTOT, 
                design = design, 
                family = quasibinomial())

summary(model)
```

---

## 🛠 Notes on Customization

### Data Columns (IPUMS)

| Variable   | Description                       |
| ---------- | --------------------------------- |
| `MIGSP`    | State 1 year ago                  |
| `STATEFIP` | Current state                     |
| `AGE`      | Age                               |
| `EDUC`     | Educational attainment            |
| `INCTOT`   | Total personal income             |
| `PERWT`    | Person weight (use for estimates) |

> You can verify these column codes in the IPUMS codebook or online variable documentation.

---

## 📥 Optional: Download with IPUMS Extract API

You can automate downloading and loading data via [IPUMS API](https://developer.ipums.org/), or you can use their website interface to select:

* **Person-level ACS PUMS**
* Variables like: `AGE`, `MIGSP`, `STATEFIP`, `EDUC`, `INCTOT`, `PERWT`

---

Let me know if you'd like:

* Code to handle **multi-year pooling**
* Geographic breakdowns using **PUMA**
* Visualization of migration flows or rates

I'm happy to expand on any part.

