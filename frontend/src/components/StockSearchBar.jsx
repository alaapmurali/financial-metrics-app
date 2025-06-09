import React from 'react';
import useState from 'react';

const StockSearchBar = () {
	const [symbol, setSymbol] = useState('');

	const searchSymbol = (symbol) {

	};

	return (
		<div className="inputStock">
			<input
				type="text"
				value={symbol}
				onChange={(e) => searchSymbol(e.target.value)}
				placeholder="Enter symbol"
			/>
		</div>
	)




};