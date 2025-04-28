// Utility functions
function formatCurrency(amount, currencyCode) {
    const symbols = {
        "USD": "$", "EUR": "€", "GBP": "£", "JPY": "¥",
        "EGP": "ج.م", "SAR": "ر.س", "AED": "د.إ", "KWD": "د.ك"
    };
    
    const symbol = symbols[currencyCode] || currencyCode;
    
    let formattedAmount;
    if (currencyCode === "JPY") {
        // JPY typically doesn't use decimal places
        formattedAmount = parseInt(amount).toLocaleString();
    } else {
        formattedAmount = parseFloat(amount).toLocaleString('en-US', { minimumFractionDigits: 2, maximumFractionDigits: 2 });
    }
    
    // For Arabic currencies, place the symbol at the end
    const arabicCurrencies = ["EGP", "SAR", "AED", "KWD"];
    if (arabicCurrencies.includes(currencyCode)) {
        return `${formattedAmount} ${symbol}`;
    } else {
        return `${symbol}${formattedAmount}`;
    }
}