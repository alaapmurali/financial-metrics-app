import api from './api.js';

export default async function submitTicker(ticker) {
	try {
		const response = await api.get(`/${ticker}`);
		return JSON.parse(JSON.stringify(response.data));  //total_cash
	} catch (error) {
		console.error("Error fetching stock data", error);
	};
};