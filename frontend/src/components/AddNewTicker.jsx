import React, {useState} from 'react';
// import Text from 'react-native-web';


// This React component is to type a ticker symbol into a form and click submit.
const TickerForm = ({fetchData}) => {
	const [ticker, setTicker] = useState('');

	const handleSubmit = (event) => {
		event.preventDefault();
		if (ticker) {
			fetchData(ticker);
			setTicker('');
		};
	};

	return (
		<>	
			<form onSubmit={handleSubmit}>
				<input
					type="text"
					value={ticker}
					onChange={(e) => setTicker(e.target.value)}
					placeholder="Enter ticker symbol"
				/>
				<button type="submit">Search</button>
			</form>
		</>
	);
};

export default TickerForm;