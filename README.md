# AI-Driven E-Commerce Sales, Customer \& Business Analytics

![AI E-Commerce Analytics Dashboard](screenshots/dashboard\_overview.png)



An end-to-end Data Analytics and Machine Learning project built using Python, PostgreSQL, Power BI and Scikit-learn to analyze e-commerce sales, customer behavior, operational performance and future revenue trends.



\---



\## 📌 Project Overview



This project analyzes the Brazilian E-Commerce Public Dataset by Olist.



The objective is to transform raw e-commerce data into actionable business insights using:



\- Data cleaning and exploratory data analysis

\- PostgreSQL database design and SQL analytics

\- Power BI interactive dashboards

\- RFM customer analysis

\- K-Means customer segmentation

\- Machine Learning-based revenue forecasting

\- Business recommendations



The project follows a complete analytics pipeline:



Raw Data → Python → PostgreSQL → SQL → Power BI → Machine Learning → Business Insights



\---



\## 🎯 Business Objectives



The project answers important business questions such as:



\- How much revenue is generated?

\- How are sales changing over time?

\- Which product categories generate the most revenue?

\- Which customer states contribute the most revenue?

\- Which payment methods are most commonly used?

\- How many customers are repeat customers?

\- How is delivery performance?

\- What is the customer satisfaction level?

\- Which customer segments are high-value or at-risk?

\- What can future revenue look like based on historical trends?



\---



\## 🛠️ Technology Stack



| Technology | Purpose |

|---|---|

| Python | Data cleaning, EDA and Machine Learning |

| Pandas | Data manipulation |

| NumPy | Numerical analysis |

| Matplotlib | Data visualization |

| Seaborn | Exploratory visualization |

| Scikit-learn | K-Means and Random Forest |

| PostgreSQL | Relational database and SQL analytics |

| Power BI | Interactive dashboard |

| DAX | Power BI measures and calculations |

| Excel/CSV | Data exchange and outputs |

| Git/GitHub | Version control and portfolio |



\---



\## 📂 Project Structure



```text

AI\_Ecommerce\_Analytics

│

├── data

│   └── Olist CSV datasets

│

├── python

│   ├── 01\_data\_inspection.py

│   ├── 02\_postgresql\_connection.py

│   ├── 03\_customer\_segmentation.py

│   ├── 04\_sales\_forecasting.py

│   ├── 05\_revenue\_forecast\_model.py

│   ├── 06\_random\_forest\_forecast.py

│   ├── 07\_forecast\_validation.py

│   │

│   ├── customer\_segments.csv

│   ├── rfm\_data.csv

│   ├── monthly\_sales.csv

│   ├── forecasting\_data.csv

│   ├── forecast\_features.csv

│   ├── forecast\_evaluation.csv

│   ├── random\_forest\_evaluation.csv

│   ├── forecast\_validation\_results.csv

│   └── final\_revenue\_forecast.csv

│

├── sql

│   └── SQL business analysis queries

│

├── powerbi

│   └── AI\_Ecommerce\_Analytics.pbix

│

├── screenshots

│   └── Dashboard screenshots

│

├── reports

│   └── Project reports

│

└── README.md

