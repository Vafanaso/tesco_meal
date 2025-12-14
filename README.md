# 🛒🍳 AI Budget Meal Planner – Telegram Bot

A **Telegram bot** that generates a **shopping list and meal plan** based on a user-defined **budget**, using **AI reasoning** and **real grocery prices from Tesco**.  
The bot allows users to **interactively manage their shopping list directly in Telegram** while receiving recipe and menu suggestions tailored to their budget.

---

## ✨ Features

- 💰 Budget-based grocery planning
- 🤖 AI-generated shopping list & meal plan
- 🥗 Health and preference adjustments via chat
- 🔍 Real product prices from Tesco (SerpAPI)
- 🛍️ 3–4 product options per ingredient
- 📊 AI-based product selection & price fallback
- ✅ Interactive shopping list (mark items as bought)
- 📱 Telegram UI with buttons (aiogram)
- 🗃️ Persistent storage (PostgreSQL)
- 🐳 Fully containerized with Docker

---

## 🧠 How It Works

1. The user enters a **budget** in Telegram (e.g. `600 Kč`)
2. **ChatGPT** generates:
   - A meal plan (duration depends on budget)
   - A list of required ingredients with quantities
3. Each ingredient is searched using **SerpAPI**
   - Tesco-specific search queries
   - Up to **3–4 product options** per ingredient
4. Extracted data includes:
   - Product title
   - Price
   - Snippet
   - Highlighted words snippet
5. **ChatGPT selects the best product option**
   - Cheapest or best match
   - Estimates price if search fails
6. The final shopping list is **stored in PostgreSQL**
7. The user interacts with the list in Telegram:
   - Mark products as bought
   - Review menu and recipes

## 🛠️ Tech Stack

- **Python 3.11**
- **Aiogram** (Telegram bot framework)
- **OpenAI API** (ChatGPT)
- **SerpAPI** (Google Search API)
- **PostgreSQL**
- **Docker & Docker Compose**
- **uv** (fast Python package manager)

---

## 🚧 Project Status

This project is **currently under active development**.

Features, architecture, and implementation details may change as the project evolves.  
Some functionality may be incomplete or experimental.

Contributions, suggestions, and feedback are welcome.

