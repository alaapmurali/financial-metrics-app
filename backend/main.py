import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import os
import requests
from datetime import datetime


app = FastAPI()

# The locations from where your backend FastAPI will be accessed, in this case where the frontend React app is running
origins = [
	"http://localhost:5173"
]

# Allow the app to access Origins
app.add_middleware(
	CORSMiddleware,
	allow_origins = origins,
	allow_credentials = True,
	allow_methods = ["*"],
	allow_headers = ["*"]
)

# Load API key from environment variables
load_dotenv()
alphavantage_api_key = os.getenv("ALPHAVANTAGE_KEY")


@app.get("/")
def root():
	return {"Welcome!": "This API returns financial data for stocks, starting with income statements and balance sheets."}


# This endpoint returns the annual balance sheet for a company in the last fiscal year
@app.get("/balance/{ticker}")
def getBalanceSheet(ticker: str):
	url = f"https://www.alphavantage.co/query?function=BALANCE_SHEET&symbol={ticker}&apikey={alphavantage_api_key}"
	response = requests.get(url)

	if response.ok:
		data = response.json()
		annualData = data.get("annualReports")[0]
		return annualData
	else:
		return {"Request failed with status code": response.status_code}


# This endpoint returns the annual income statement for a company in the last fiscal year
@app.get("/income/{ticker}")
def getIncomeStatement(ticker: str):
	url = f"https://www.alphavantage.co/query?function=INCOME_STATEMENT&symbol={ticker}&apikey={alphavantage_api_key}"
	response = requests.get(url)

	if response.ok:
		data = response.json()
		annualData = data.get("annualReports")[0]
		return annualData
	else:
		return {"Request failed with status code": response.status_code}


# This endpoint returns the current earnings yield for a company based on the previous fiscal year's annual reported financials
@app.get("/ey/{ticker}")
def getEarningsYield(ticker: str):
	return {"earningsYield": earningsYield(ticker)}
	

# This endpoint returns the return on tangible investment capital for a company in the previous fiscal year
@app.get("/rotc/{ticker}")
def getReturnOnTangibleCapital(ticker: str):
	return {"returnOnTangibleCapital": returnOnTangibleCapital(ticker)}



## Helper functions ##

def earningsYield(ticker: str):
	balanceData = getBalanceSheet(ticker)
	incomeData = getIncomeStatement(ticker)

	# EBIT
	ebit = getEBIT(ticker, incomeData)

	# Calculate market cap
	sharesOutstanding = getSharesOutstanding(ticker, balanceData)
	marketCap = getCurrentPrice(ticker) * sharesOutstanding

	# Total debt
	debt = getTotalDebt(ticker, balanceData)

	# Excess cash
	excessCash = getExcessCash(ticker, balanceData)

	# Enterprise value = market cap + total debt - excess cash
	ev = marketCap + debt - excessCash

	# Earnings yield = EBIT / Enterprise value * 100
	return ebit/ev*100

def getCurrentPrice(ticker: str):
	url = f"https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={ticker}&apikey={alphavantage_api_key}"
	response = requests.get(url)

	if response.ok:
		data = response.json()
		if data.get("Global Quote").get("05. price") != "None": return float(data.get("Global Quote").get("05. price"))
	else:
		return {"Request failed with status code": response.status_code}


# Calculate average yearly price by finding the average of each month's open and close from the previous calendar year, and averaging again
def getAverageYearlyPrice(ticker: str):
	url = f"https://www.alphavantage.co/query?function=TIME_SERIES_MONTHLY&symbol={ticker}&apikey={alphavantage_api_key}"
	response = requests.get(url)

	if response.ok:
		data = response.json()
		thisMonth = datetime.now().month
		previousYearIndexes = list(data.get("Monthly Time Series").keys())[thisMonth:thisMonth+12]

		monthlyAverages: [float] = []
		for month in previousYearIndexes:
			monthOpen = float(data.get("Monthly Time Series").get(month).get("1. open"))
			monthClose = float(data.get("Monthly Time Series").get(month).get("4. close"))
			monthAverage = (monthOpen + monthClose) / 2
			monthlyAverages.append(monthAverage)

		return sum(monthlyAverages)/len(monthlyAverages)
	else:
		return {"Request failed with status code": response.status_code}


def returnOnTangibleCapital(ticker: str):
	balanceData = getBalanceSheet(ticker)
	incomeData = getIncomeStatement(ticker)

	# EBIT
	ebit = getEBIT(ticker, incomeData)

	# Net Working Capital
	nwc = getCurrentAssets(ticker, balanceData) - getCurrentLiabilities(ticker, balanceData)

	# Net Fixed Assets
	nfa = getNetFixedAssets(ticker, balanceData)

	# Return on Tangible Capital = EBIT / (Net Working Capital + Net Fixed Assets)
	return ebit/(nwc+nfa)*100


def getEBIT(ticker: str, incomeData: dict):
	if incomeData.get("ebit") != "None":
		return float(incomeData.get("ebit"))
	else:
		return 0.00


def getSharesOutstanding(ticker: str, balanceData: dict):
	if balanceData.get("commonStockSharesOutstanding") != "None":
		return int(balanceData.get("commonStockSharesOutstanding"))
	else:
		return 0

def getTotalDebt(ticker:str, balanceData: dict):
	shortTermDebt = 0.00
	longTermDebt = 0.00

	if balanceData.get("shortTermDebt") != "None": shortTermDebt = float(balanceData.get("shortTermDebt"))

	if balanceData.get("longTermDebt") != "None": longTermDebt = float(balanceData.get("longTermDebt"))

	return shortTermDebt + longTermDebt

def getExcessCash(ticker: str, balanceData: dict):
	if balanceData.get("cashAndShortTermInvestments") != "None":
		return float(balanceData.get("cashAndShortTermInvestments"))
	else:
		return 0.00

def getCurrentAssets(ticker: str, balanceData:  dict):
	if balanceData.get("totalCurrentAssets") != "None":
		return float(balanceData.get("totalCurrentAssets"))
	else:
		return 0.00

def getCurrentLiabilities(ticker: str, balanceData: dict):
	if balanceData.get("totalCurrentLiabilities") != "None":
		return float(balanceData.get("totalCurrentLiabilities"))
	else:
		return 0.00

# Net Fixed Assets (NFA) can be simplified to NFA = Total Non-Current Assets – Intangibles
def getNetFixedAssets(ticker: str, balanceData: dict):
	return getNonCurrentAssets(ticker, balanceData) - getIntangibles(ticker, balanceData)

def getNonCurrentAssets(ticker: str, balanceData: dict):
	if balanceData.get("totalNonCurrentAssets") != "None":
		return float(balanceData.get("totalNonCurrentAssets"))
	else:
		return 0.00

def getIntangibles(ticker: str, balanceData: dict):
	goodwill = 0.00
	otherIntangibles = 0.00

	if balanceData.get("goodwill") != "None": goodwill = float(balanceData.get("goodwill"))
	if balanceData.get("intangibleAssetsExcludingGoodwill") != "None": otherIntangibles = float(balanceData.get("intangibleAssetsExcludingGoodwill"))

	return goodwill + otherIntangibles
