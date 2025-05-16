
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
