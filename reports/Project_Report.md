\# AI-Driven E-Commerce Sales, Customer \& Business Analytics

\## Project Report



\---



\## 1. Executive Summary



This project presents an end-to-end E-Commerce Analytics solution using Python, PostgreSQL, Power BI, and Machine Learning.



The objective was to analyze sales performance, customer behavior, payment methods, reviews, delivery performance, product categories, and geographic revenue distribution.



Machine Learning was also incorporated to identify customer segments using RFM analysis and K-Means clustering, followed by a six-month revenue forecast using a Random Forest model.



The final solution transforms raw transactional data into business insights through:



Raw Data → Python → PostgreSQL → SQL → Machine Learning → Power BI → Business Recommendations



\---



\## 2. Business Problem



E-commerce businesses generate large volumes of transactional and customer data.



Without proper analytics, it can be difficult to answer questions such as:



\- Which products generate the most revenue?

\- Which regions generate the most sales?

\- How many customers return to purchase again?

\- Which customers are high-value?

\- Which customers may be at risk of becoming inactive?

\- How effective is delivery performance?

\- Which payment methods are most important?

\- What could future revenue look like?



This project addresses these questions through an integrated analytics and Machine Learning workflow.



\---



\## 3. Dataset



The project uses the Brazilian E-Commerce Public Dataset by Olist.



The dataset contains information about:



\- Customers

\- Orders

\- Order items

\- Payments

\- Reviews

\- Products

\- Sellers

\- Geolocation

\- Product category translation



\### Initial dataset sizes



| Dataset | Rows |

|---|---:|

| Customers | 99,441 |

| Orders | 99,441 |

| Order Items | 112,650 |

| Payments | 103,886 |

| Reviews | 99,224 |

| Products | 32,951 |

| Sellers | 3,095 |

| Geolocation | 1,000,163 |

| Category Translation | 71 |



\---



\## 4. Data Preparation



Python and Pandas were used for data inspection and preparation.



The following checks were performed:



\- Dataset dimensions

\- Missing values

\- Duplicate records

\- Data types

\- ID integrity

\- Date conversion

\- Revenue validation

\- Delivery calculations



\### Important Revenue Calculation



The Olist dataset does not contain a quantity column.



Therefore, item revenue was calculated as:



```python

order\_items\["revenue"] = order\_items\["price"]

