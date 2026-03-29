# Expense Tracker API

I'm building this expense tracker API as a learning project. 
It's designed for freelancers to track their expenses, detect 
spending patterns, and predict month-end spend.

Key Features for Freelancers
Expense Management: Add, view, edit, and delete expenses with details like amount, date, description, and category.
Client & Project Tracking: Associate expenses with specific clients or projects — great for billing, tax reporting, and understanding profitability per client/project.
Spending Visibility: See all your expenses in one place, filter by client, project, date range, or category.
Developer-Friendly: Full Swagger UI for easy exploration and testing of endpoints.
Fast & Lightweight: Built with FastAPI for quick responses and smooth development experience.

This makes it useful for freelancers who juggle multiple clients and need clear visibility into where their money is going.

Still a work in progress — building it step by step.

## What's done
- [x] Basic CRUD API with FastAPI

- [x] Real database integration
     
- [x] Projects and Clients management (link expenses to specific clients or projects)
      
- [x] Basic HTML frontend (index.html and frontend.html) for quick testing and demo
      
- [x] Clean project structure and improved code readability

Modifications Done So Far

Added support for a real database.

Implemented Projects and Clients management.

Added basic HTML frontend files (index.html and frontend.html) for easier testing and demo.

Improved overall project structure and code readability.

 Next steps: Recurring expense detection and spending predictions/insights.
 
 Clone the repository:
   ```bash
   git clone https://github.com/onukul/expense-tracker-api.git
   cd expense-tracker-api
   Install dependencies
   pip install -r requirements.txt
   Run the dev server
   uvicorn main:app --reload
