import React, {useState, useEffect} from 'react';
import submitTicker from '../utils.js';
import TickerForm from './AddNewTicker';

const DumpData = () => {
	const [data, setData] = useState('');
	const ticker = '';

	const fetchData = async (ticker) => {
		DumpData.ticker = ticker;
		const response = await submitTicker(ticker);
		setData(JSON.stringify(response));
	};

	// Used to watch for when the data variable updates
	useEffect(() => {
		console.log("The data variable just updated: ", data);
	}, [data]);

	return (
		<div>
			<TickerForm fetchData={fetchData} />
			<p>{ticker}: {data}</p>
		</div>
	);
};

export default DumpData;