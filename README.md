🛒🍳 AI Budget Meal Planner – Telegram Bot

A Telegram bot that helps users plan groceries and meals based on a budget, using AI reasoning and real product prices from Tesco.
The bot generates a shopping list and recipes, fetches multiple real product options per ingredient, and lets users interactively manage their shopping list directly in Telegram.

✨ Features

💰 Budget-based grocery planning

🤖 AI-generated shopping list & meal plan
🔍 Real product prices from Tesco (SerpAPI)
🛍️ 3–4 product options per ingredient
📊 Price-based optimization & fallback logic
✅ Interactive shopping list (mark as bought)
📱 Telegram UI with buttons & menus
🗃️ Persistent storage (PostgreSQL)
🐳 Fully containerized with Docker
🧠 System Overview

The bot combines AI reasoning with search-based price discovery to produce realistic, budget-aware shopping lists.

High-Level Flow

User inputs budget (e.g. 600 Kč) in Telegram
ChatGPT generates:
-Meal plan
-Ingredient list
-Quantities (depends on budget)

Each ingredient is searched via SerpAPI
(Tesco-specific queries)
Up to 3–4 product options per ingredient

ChatGPT selects best option
(Cheapest / best match)

Fallback price estimation if search fails

Final product list is saved to DB

User interacts with list in Telegram
Mark items as bought
Review menu & recipes
