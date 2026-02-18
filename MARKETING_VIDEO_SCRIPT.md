# Launch Potato - Lead Data Analyst Application
## Marketing Dashboard Walkthrough Script (3-5 Minutes)

**Goal**: Demonstrate "Analytical Rigor", "Actionable BI", and "SQL Proficiency".

---

### 1. Introduction & "Why this Dashboard?" (0:00 - 1:00)
*   **Visual**: Face camera -> Screen Share (Dashboard Home).
*   **Hook**: "Hi, I'm [Your Name]. I'm applying for the Lead Data Analyst role. Today I'm walking you through a custom **Marketing Intelligence Suite** I built to solve a critical problem: optimizing ad spend across fragmented channels."
*   **Why**: "I chose to build this because measuring ROI across Google, Facebook, and TikTok is often messy. I wanted a tool that not only reports *what happened* but helps predict *what to do next*."
*   **Tech Stack**: "I architected this using **Python**, **SQLite** (for a robust data warehouse), and **Streamlit** for the frontend."

### 2. KPIs & Actionability (1:00 - 2:30)
*   **Visual**: Point to the Top Metric Cards (ROAS, CPA).
*   **Narrative**: "At the top, we focus on the North Star metrics: **ROAS (Return on Ad Spend)** and **CPA**. Vanity metrics like 'Impressions' are secondary."
*   **The Deep Dive**: *Click on 'Campaign Deep Dive' in the sidebar.*
    *   **Action**: Hover over the Scatter Plot.
    *   **Say**: "This 'Efficiency Frontier' chart is my favorite feature. It instantly separates the winners from the losers. Campaigns in the top-left are high-efficiency; bottom-right are burning cash. This makes the data immediately actionable: kill the bottom-right, scale the top-left."

### 3. Structure & Support for Decisions (2:30 - 3:30)
*   **Visual**: Go back to **Home Page** -> Scroll to **Budget Simulator**.
*   **Narrative**: "The structure of this dashboard supports better decisions by enabling **Scenario Planning**. A static report is dead; a simulator is alive."
*   **Action**: Move the 'Facebook Budget' slider DOWN and 'Google Budget' slider UP.
    *   **Say**: "Right here, a marketing manager can simulate shifting budget from a low-ROAS channel (Facebook) to a high-ROAS one (Google). You can see the predicted revenue jump instantly. This empowers stakeholders to make data-driven budget allocations without needing to query a database."

### 4. Technical Rigor (SQL Flex) (3:30 - 4:30)
*   **Visual**: Click on **'SQL Lab'** -> **'Data Explorer'** tab.
    *   **Say**: "While the dashboard is great for executives, as an analyst, I need raw access. I built this **Data Explorer** to verify data integrity."
*   **Visual**: Click **'SQL Editor'** tab.
    *   **Action**: Run the default query (`SELECT... GROUP BY channel`).
    *   **Say**: "And for complex questions—like attribution modeling or cohort analysis—I have direct SQL access to the warehouse using CTEs and Window Functions. This ensures that the logic behind the dashboard is transparent and auditable."

### 5. Conclusion (4:30 - 5:00)
*   **Visual**: Face / Summary View.
*   **Closing**: "This project demonstrates my philosophy: Data should be clean, accessible, and above all, actionable. I'm excited to bring this full-stack approach to Launch Potato. Thanks for watching."

---

## Pre-Recording Checklist
- [ ] **Reset**: Ensure sliders are at default positions.
- [ ] **Data**: Ensure `marketing.db` is populated (630 rows).
- [ ] **Theme**: Check that "Dark Mode" looks crisp.
- [ ] **Practice**: Run through the "Simulator" click path once before recording.
