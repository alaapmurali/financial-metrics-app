# Financial Metrics

An API to calculate useful company metrics for stock options trading. Backend is built in FastAPI and frontend in React.

As someone who researches public companies deeply for my options strategy, I needed a way to measure useful metrics that my brokerage platform did not report but that could be determined using company income statements and balance sheets. So I built this API that calculates those key metrics. Inspired by strategies in Joel Greenblatt's "The Little Book That Still Beats The Market".

The API uses the EBIT/EV multiple as a better measure of earnings yield than EPS/share price, since EPS on its own is quite arbitrary--companies can change it via stock splits and buybacks. The EBIT/EV multiple is easier to understand raw earnings than EPS, since different industries can have different borrowing costs and tax rates. Overall, the earnings yield tells me whether the company is at a good price or not.

The API also uses Return on Tangible Capital (ROTC) over ROIC or ROE as a way to better measure how much each dollar earned from operating the business compares to the cost to produce that dollar (i.e. efficiency). Overall, ROTC gives me a sense of whether a company is a good, efficient company. More info here: https://www.oldschoolvalue.com/stock-valuation/the-magic-formula-return-on-capital/

Together, these measures help me find "good companies at bargain prices".

## How to run the API locally

The backend and frontend run as different services.

To run the backend, start a Python virtual env locally, install dependencies, and start a local Uvicorn server on port 3000. Make sure to create an AlphaVantage API Key and add it to a .env file with the variable name 'ALPHAVANTAGE_KEY'.

Since the app uses FastAPI, to see the API docs go to http://localhost:3000/docs in your browser.

## How to run the frontend locally

To run the frontend, install the dependencies in package.json using 'npm install' and then run 'npm run dev'. Make sure you have 'vite' installed, since it starts the frontend server.
